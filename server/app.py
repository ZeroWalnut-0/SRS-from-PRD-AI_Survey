from __future__ import annotations

import ipaddress
import os
import re
import secrets
import threading
import shutil
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

from server.job_runner import run_job_in_thread
from server.models import JobState, RunRequest, ResetRequest
from server.planner import compute_plan
from server.state_store import save_coverage_state, state_path
from server.ui import UI_HTML
from runner.loggers import ADMIN_IPS, ip_to_dirname, setup_logger_dual

STATE_BY_CLIENT: Dict[str, JobState] = {}
STATE_LOCK = threading.Lock()

app = FastAPI(title="Survey AutoRunner UI", version="1.2.0")
_seen_ips_lock = threading.Lock()
_seen_ips: set[str] = set()

SESSION_COOKIE_NAME = "survey_runner_sid"
SESSION_COOKIE_MAX_AGE = 60 * 60 * 24 * 30


def _request_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _parse_trusted_proxy_networks() -> list[ipaddress._BaseNetwork]:
    raw = str(os.getenv("TRUSTED_PROXY_CIDRS", "") or "").strip()
    items = [x.strip() for x in raw.split(",") if x.strip()]
    nets: list[ipaddress._BaseNetwork] = []
    for item in items:
        try:
            nets.append(ipaddress.ip_network(item, strict=False))
        except Exception:
            continue
    return nets


TRUSTED_PROXY_NETWORKS = _parse_trusted_proxy_networks()


def _is_trusted_proxy(ip: str) -> bool:
    if not ip or ip == "unknown":
        return False
    try:
        addr = ipaddress.ip_address(ip)
    except Exception:
        return False
    return any(addr in net for net in TRUSTED_PROXY_NETWORKS)


def get_request_ip(request: Request) -> str:
    remote_ip = _request_ip(request)
    if not _is_trusted_proxy(remote_ip):
        return remote_ip

    xff = request.headers.get("x-forwarded-for", "")
    if not xff:
        return remote_ip

    for raw in [x.strip() for x in xff.split(",") if x.strip()]:
        try:
            ipaddress.ip_address(raw)
            return raw
        except Exception:
            continue
    return remote_ip


def _is_private_ip(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return False


def _valid_client_key(value: str) -> bool:
    if not value:
        return False
    if len(value) < 16 or len(value) > 128:
        return False
    return all(ch.isalnum() or ch in ("-", "_") for ch in value)


def _new_client_key() -> str:
    return secrets.token_urlsafe(24)


def get_client_key(request: Request) -> str:
    cookie_value = str(request.cookies.get(SESSION_COOKIE_NAME) or "").strip()
    if _valid_client_key(cookie_value):
        return cookie_value
    return f"ip_{get_request_ip(request).replace(':', '_').replace('.', '_')}"


@app.middleware("http")
async def client_context_middleware(request: Request, call_next):
    request_ip = get_request_ip(request)
    request.state.client_ip = request_ip
    request.state.client_key = get_client_key(request)

    if request_ip != "unknown" and _is_private_ip(request_ip):
        first = False
        with _seen_ips_lock:
            if request_ip not in _seen_ips:
                _seen_ips.add(request_ip)
                first = True
        if first:
            logger = setup_logger_dual("run_logs_pw", request_ip)
            logger.info(f"[ACCESS] internal first ip={request_ip} path={request.url.path}")

    response = await call_next(request)

    if not _valid_client_key(str(request.cookies.get(SESSION_COOKIE_NAME) or "")):
        new_key = _new_client_key()
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=new_key,
            max_age=SESSION_COOKIE_MAX_AGE,
            httponly=True,
            samesite="lax",
        )
        request.state.client_key = new_key
    return response


def _find_latest_failure_file(out_dir: str, client_key: str) -> str | None:
    client_dir = os.path.join(out_dir, "clients", ip_to_dirname(client_key))
    if not os.path.isdir(client_dir):
        return None
    candidates: list[tuple[float, str]] = []
    for root, _dirs, files in os.walk(client_dir):
        for fn in files:
            low = fn.lower()
            if "fail" not in low or not low.endswith(".html"):
                continue
            path = os.path.join(root, fn)
            try:
                mtime = os.path.getmtime(path)
            except Exception:
                mtime = 0.0
            candidates.append((mtime, path))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def _filter_user_logs(lines: list[str]) -> list[str]:
    # 상세 로그는 제외하고 문항 응답 및 주요 상태만 선별 (일반 사용자용)
    patterns = [
        r"radio",
        r"checkbox",
        r"select",
        r"input\(",
        r"textarea",
        r"canvas",
        r"rank",
        r"START",
        r"COMPLETED",
        r"step=\d+",
        r"validation alert detected",
    ]
    combined = re.compile("|".join(patterns), re.IGNORECASE)
    
    res = []
    for line in lines:
        if not combined.search(line):
            continue
            
        # 정제 (타임스탬프 등 제거 및 문구 간소화)
        # 1) 로그 레벨 및 타임스탬프 제거: "2026-04-20 01:00:00,000 | INFO | message" -> "message"
        cleaned = re.sub(r"^[0-9- :,|]+ (INFO|WARNING|ERROR|DEBUG) \| ", "", line)
        
        # 2) 문항 응답 유형 간소화 (radio(required) -> radio 등)
        cleaned = re.sub(r"radio\(.*?\):", "radio:", cleaned)
        cleaned = re.sub(r"checkbox\(.*?\):", "checkbox:", cleaned)
        cleaned = re.sub(r"input\(.*?\):", "input:", cleaned)
        
        # 3) 불필요한 파라미터 괄호 제거 (min=..., max=...)
        cleaned = re.sub(r" \(min=.*?, max=.*?\)", "", cleaned)
        
        # 4) 페이지 이동 간소화: [0] step=0 Q1 -> Q2 (expected_next=... url=...) -> [0] Q1 -> Q2
        cleaned = re.sub(r"\[(\d+)\] step=\d+ (.*?) -> (.*?) \(.*?\)", r"[\1] \2 -> \3", cleaned)
        
        # 5) 기술적 로그 추가 제외 (next_runtime 등)
        if "next_runtime" in cleaned or "next_trigger" in cleaned:
            continue
            
        res.append(cleaned)
    return res


def tail_file(path: str, max_lines: int = 250) -> list[str]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "rb") as f:
            data = f.read()
        text = data.decode("utf-8", errors="replace")
        return text.splitlines()[-max_lines:]
    except Exception:
        return []


def _short_error(err: Optional[str]) -> Optional[str]:
    if not err:
        return err
    e = str(err)
    needles = [
        "Target closed",
        "TargetClosedError",
        "Browser closed",
        "Page closed",
        "has been closed",
        "Navigation failed because page was closed",
        "Protocol error",
        "Execution context was destroyed",
        "Most likely the page has been closed",
    ]
    if any(n.lower() in e.lower() for n in needles):
        return "창닫음"
    first_line = e.splitlines()[0].strip()
    if len(first_line) > 140:
        first_line = first_line[:140] + "..."
    return first_line


def _state_for_request(request: Request) -> JobState | None:
    client_key = getattr(request.state, "client_key", get_client_key(request))
    with STATE_LOCK:
        return STATE_BY_CLIENT.get(client_key)


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(UI_HTML)


@app.post("/api/plan")
def api_plan(req: RunRequest, request: Request):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    client_ip = getattr(request.state, "client_ip", get_request_ip(request))
    try:
        plan = compute_plan(req, client_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="ASP Logic 형식이 맞지 않습니다. (parse failed)")
    return JSONResponse({"ok": True, "client_ip": client_ip, "client_key": client_key, "plan": plan})


@app.post("/api/run")
def api_run(req: RunRequest, request: Request):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    client_ip = getattr(request.state, "client_ip", get_request_ip(request))
    with STATE_LOCK:
        st = STATE_BY_CLIENT.get(client_key)
        if st and getattr(st, "running", False):
            raise HTTPException(status_code=409, detail="Already running for this client session.")
        st = JobState()
        st.reset_for_start(JobState.make_job_id(), req.out_dir or "run_logs_pw")
        st.running = False
        st.stop_requested = False
        st.error = None
        st.progress = 0
        st.message = "starting"
        st.asp_logic = req.asp_logic
        st.out_dir = req.out_dir or "run_logs_pw"
        st.ref_doc_path = req.ref_doc_path
        st.concurrency = int(getattr(req, "concurrency", 5) or 5)
        st.execution_timeout_sec = int(getattr(req, "execution_timeout_sec", 3600) or 3600)
        STATE_BY_CLIENT[client_key] = st

    t = threading.Thread(target=run_job_in_thread, args=(req, client_key, st), daemon=True)
    t.start()
    return {"ok": True, "client_ip": client_ip, "client_key": client_key}


@app.post("/api/stop")
def api_stop(request: Request):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    client_ip = getattr(request.state, "client_ip", get_request_ip(request))
    with STATE_LOCK:
        st = STATE_BY_CLIENT.get(client_key)
        if not st:
            return {"ok": True, "stopped": False, "reason": "no state", "client_ip": client_ip, "client_key": client_key}
        st.stop_requested = True
        st.message = "stop requested"
    return {"ok": True, "stopped": True, "client_ip": client_ip, "client_key": client_key}


@app.get("/api/status")
def api_status(request: Request):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    client_ip = getattr(request.state, "client_ip", get_request_ip(request))
    with STATE_LOCK:
        st = STATE_BY_CLIENT.get(client_key)
    if not st:
        return {
            "ok": True,
            "client_ip": client_ip,
            "client_key": client_key,
            "running": False,
            "message": "no state",
            "mode": "",
            "planned_total": 0,
            "current_run": 0,
            "remaining_cases": 0,
            "progress": 0,
            "stop_requested": False,
            "error": None,
            "concurrency": 5,
            "execution_timeout_sec": 3600,
        }
    return {
        "ok": True,
        "client_ip": client_ip,
        "client_key": client_key,
        "running": bool(getattr(st, "running", False)),
        "stop_requested": bool(getattr(st, "stop_requested", False)),
        "progress": int(getattr(st, "progress", 0) or 0),
        "message": getattr(st, "message", ""),
        "mode": getattr(st, "mode", ""),
        "planned_total": int(getattr(st, "planned_total", 0) or 0),
        "current_run": int(getattr(st, "current_run", 0) or 0),
        "remaining_cases": int(getattr(st, "remaining_cases", 0) or 0),
        "error": getattr(st, "error", None),
        "concurrency": int(getattr(st, "concurrency", 5) or 5),
        "execution_timeout_sec": int(getattr(st, "execution_timeout_sec", 3600) or 3600),
    }


@app.post("/api/reset_state")
def api_reset_state(req: ResetRequest, request: Request):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    if not req.asp_logic.strip():
        return JSONResponse({"ok": False, "detail": "초기화할 ASP 로직(상태)이 없습니다."})
        
    base_out_dir = req.out_dir or "run_logs_pw"
    st_path = state_path(base_out_dir, req.asp_logic, client_key)
    st0 = {"done_case_keys": [], "bad_case_keys": [], "runs": 0}
    save_coverage_state(st_path, st0)
    return JSONResponse({"ok": True, "state_path": st_path, "reset": st0})


@app.get("/api/logs", response_class=PlainTextResponse)
def api_logs(request: Request, out_dir: Optional[str] = None):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    client_ip = getattr(request.state, "client_ip", get_request_ip(request))
    is_admin = client_ip in ADMIN_IPS
    st = _state_for_request(request)
    base_out_dir = out_dir or (getattr(st, "out_dir", None) if st else None) or "run_logs_pw"
    if is_admin:
        path = os.path.join(base_out_dir, "run_all.log")
    else:
        path = os.path.join(base_out_dir, "clients", ip_to_dirname(client_key), "run.log")
    lines = tail_file(path)
    if not is_admin:
        lines = _filter_user_logs(lines)
    return PlainTextResponse("\n".join(lines))


@app.get("/api/latest_failure")
def api_latest_failure(request: Request, out_dir: Optional[str] = None):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    st = _state_for_request(request)
    base_out_dir = out_dir or (getattr(st, "out_dir", None) if st else None) or "run_logs_pw"
    p = _find_latest_failure_file(base_out_dir, client_key)
    return {
        "ok": True,
        "found": bool(p),
        "path": p or "",
        "base_out_dir": base_out_dir,
        "client_key": client_key,
    }


@app.get("/api/latest_failure_view", response_class=HTMLResponse)
def api_latest_failure_view(request: Request, out_dir: Optional[str] = None):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    st = _state_for_request(request)
    base_out_dir = out_dir or (getattr(st, "out_dir", None) if st else None) or "run_logs_pw"
    p = _find_latest_failure_file(base_out_dir, client_key)
    if not p:
        raise HTTPException(status_code=404, detail="No failure html found")
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return HTMLResponse(f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=_short_error(str(e)) or "read failed")

@app.post("/api/upload_doc")
def api_upload_doc(file: UploadFile = File(...), request: Request = None):
    # Save uploaded file
    try:
        out_dir = "run_logs_pw/docs"
        os.makedirs(out_dir, exist_ok=True)
        file_path = os.path.join(out_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"ok": True, "path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.get("/api/wording_report", response_class=HTMLResponse)
def api_wording_report(request: Request, out_dir: Optional[str] = None):
    client_key = getattr(request.state, "client_key", get_client_key(request))
    st = _state_for_request(request)
    base_out_dir = out_dir or (getattr(st, "out_dir", None) if st else None) or "run_logs_pw"
    
    # 보고서는 해당 클라이언트 디렉토리에 저장됩니다
    report_path = os.path.join(base_out_dir, "clients", ip_to_dirname(client_key), "diff_report.html")
    
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="No wording report found")
        
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
