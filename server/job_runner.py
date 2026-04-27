from __future__ import annotations

import os
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional

from starlette.exceptions import HTTPException

from runner import RunnerConfig, run_one
from .models import JobState
from runner.loggers import setup_logger_dual, ip_to_dirname
from .planner import compute_plan
from .asp_cases import (
    build_asp_runtime_bundle,
    extract_cases_from_asp,
    merge_case_with_guards,
)
from runner.verifier import WordingVerifier
from .state_store import (
    load_json,
    save_json,
    state_path,
    load_coverage_state,
    save_coverage_state,
    _normalize_case_key,
    case_key,
)

_STATE_FILE_LOCKS: dict[str, threading.Lock] = {}
_STATE_FILE_LOCKS_GUARD = threading.Lock()
_ACTIVE_RUN_KEYS: set[str] = set()
_ACTIVE_RUN_KEYS_GUARD = threading.Lock()


def _lock_for_state_path(path: str) -> threading.Lock:
    with _STATE_FILE_LOCKS_GUARD:
        lock = _STATE_FILE_LOCKS.get(path)
        if lock is None:
            lock = threading.Lock()
            _STATE_FILE_LOCKS[path] = lock
        return lock


def _normalize_stop_page(x: Optional[str]) -> Optional[str]:
    if not x:
        return None
    s = str(x).strip()
    if not s:
        return None
    if not s.lower().endswith(".asp"):
        s += ".asp"
    return s


def build_cfg(req, case_overrides: Optional[dict[str, Any]] = None) -> RunnerConfig:
    url = getattr(req, "test_url", "")
    if url and not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    cfg = RunnerConfig(
        start_url=url,
        n_responses=1,
        max_steps_per_response=req.max_steps_per_response,
        min_delay_sec=req.min_delay_sec,
        max_delay_sec=req.max_delay_sec,
        out_dir=req.out_dir,
        headless=req.headless,
        navigation_timeout_ms=req.navigation_timeout_ms,
        execution_timeout_sec=getattr(req, "execution_timeout_sec", 600),
        checkbox_select_all=req.checkbox_select_all,
        rank_select_all=getattr(req, "rank_select_all", False),
        rank_pick_min=getattr(req, "rank_pick_min", 1),
        rank_pick_max=getattr(req, "rank_pick_max", 0),
        stop_at_page=_normalize_stop_page(getattr(req, "stop_at_page", None)),
        stop_hold_max_seconds=getattr(req, "stop_hold_max_seconds", None),
        pre_next_click_delay_ms=getattr(req, "pre_next_click_delay_ms", 25),
        apply_next_constraints_before_click=getattr(req, "apply_next_constraints_before_click", False),
        log_submit_state=getattr(req, "log_submit_state", False),
    )
    setattr(cfg, "other_text_default", req.other_text_default)
    if case_overrides is not None:
        setattr(cfg, "case_overrides", case_overrides)
    return cfg


def _prepare_coverage_cases(req, logger, done_keys: set[str], bad_keys: set[str]) -> tuple[list[dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    guards: Optional[Dict[str, Any]] = None
    check_count_rules: Optional[Dict[str, Any]] = None

    runtime_bundle: Dict[str, Any] = {}
    if req.asp_logic and req.asp_logic.strip():
        try:
            runtime_bundle = build_asp_runtime_bundle(req.asp_logic)
        except Exception as e:
            logger.warning(f"[asp_bundle] build failed: {e}")
            runtime_bundle = {}

    raw_guards = runtime_bundle.get("guards") if isinstance(runtime_bundle, dict) else None
    if isinstance(raw_guards, dict) and raw_guards:
        guards = raw_guards
        logger.info(f"[guards] loaded: {guards}")

    raw_rules = runtime_bundle.get("check_count_rules") if isinstance(runtime_bundle, dict) else None
    if isinstance(raw_rules, dict) and raw_rules:
        check_count_rules = raw_rules
        logger.info(f"[check_rules] loaded: {check_count_rules}")

    cases: list[dict[str, Any]] = []
    if (req.mode or "random").lower() == "coverage":
        try:
            cases = extract_cases_from_asp(
                req.asp_logic,
                max_cases=req.max_cases,
                include_default_paths=req.include_default_paths,
                include_screen_cases=req.include_screen_cases,
            )
            if guards:
                cases = [merge_case_with_guards(c, guards) for c in cases]
                logger.info(f"[coverage] guards applied: {guards}")
            if check_count_rules:
                for c in cases:
                    if isinstance(c, dict):
                        c["__CHECK_COUNT_RULES__"] = check_count_rules
            if not cases and guards:
                cases = [dict(guards)]
                logger.info(f"[coverage] no cases from asp. using guards only as single case: {guards}")
            filtered: list[dict[str, Any]] = []
            seen: set[str] = set()
            for c in cases:
                k = case_key(c)
                if k in done_keys or k in bad_keys or k in seen:
                    continue
                seen.add(k)
                filtered.append(c)
            cases = filtered
        except Exception as e:
            raise ValueError("ASP Logic 형식이 맞지 않습니다. (Case/If 구조 또는 괄호/따옴표 등을 확인하세요.)") from e
        logger.info(
            f"[coverage] extracted={len(cases)} (max_cases={req.max_cases}) done={len(done_keys)} bad={len(bad_keys)} state={'ON' if req.persist_state else 'OFF'}"
        )
    return cases, guards, check_count_rules


def _augment_overrides(mode: str, overrides: Optional[Dict[str, Any]], guards: Optional[Dict[str, Any]], check_count_rules: Optional[Dict[str, Any]], include_screen_cases: bool) -> Optional[Dict[str, Any]]:
    case_overrides = dict(overrides) if isinstance(overrides, dict) else (dict(guards) if (mode == "random" and guards) else None)

    should_apply_check_count_rules = bool(
        check_count_rules and (
            mode == "random" or (mode == "coverage" and not bool(include_screen_cases))
        )
    )
    if should_apply_check_count_rules:
        if case_overrides is None:
            case_overrides = {}
        case_overrides["__CHECK_COUNT_RULES__"] = check_count_rules

    cond_num_rules = []
    try:
        if guards and isinstance(guards, dict):
            cond_num_rules = guards.get("__COND_NUM_RULES__", []) or []
            if not isinstance(cond_num_rules, list):
                cond_num_rules = []
    except Exception:
        cond_num_rules = []

    if cond_num_rules:
        if case_overrides is None:
            case_overrides = {}
        case_overrides["__COND_NUM_RULES__"] = cond_num_rules

    return case_overrides


def _run_one_task(req, logger, client_base_dir: str, mode: str, run_no: int, case_overrides: Optional[Dict[str, Any]], check_stop=None, verifier=None) -> tuple[bool, str, Optional[Dict[str, Any]]]:
    if mode == "coverage" and case_overrides:
        run_dir = os.path.join(client_base_dir, f"case_{run_no:03d}")
    else:
        run_dir = os.path.join(client_base_dir, f"run_{run_no:03d}")
    os.makedirs(run_dir, exist_ok=True)

    cfg = build_cfg(req, case_overrides=case_overrides)
    setattr(cfg, "out_dir", run_dir)
    if check_stop:
        setattr(cfg, "is_stop_requested", check_stop)

    if mode == "coverage" and case_overrides:
        logger.info(f"[coverage] {run_no} out_dir={run_dir} key={case_key(case_overrides)} overrides={case_overrides}")
    elif mode == "random":
        logger.info(f"[random] {run_no} out_dir={run_dir} guards(case_overrides)={case_overrides}")

    ok = bool(run_one(cfg, logger, run_no, verifier=verifier))
    return ok, run_dir, case_overrides


def run_job_in_thread(req, client_ip: str, STATE: JobState):
    logger = None
    active_run_key: Optional[str] = None
    try:
        with STATE.lock:
            STATE.running = True
            STATE.stop_requested = False
            STATE.error = None
            STATE.message = "running"
            STATE.concurrency = int(max(1, min(10, int(getattr(req, "concurrency", 5) or 5))))
            STATE.execution_timeout_sec = int(getattr(req, "execution_timeout_sec", 600) or 600)

        base_out_dir = req.out_dir or "run_logs_pw"
        os.makedirs(base_out_dir, exist_ok=True)
        ip_dir = ip_to_dirname(client_ip)
        client_base_dir = os.path.join(base_out_dir, "clients", ip_dir)
        os.makedirs(client_base_dir, exist_ok=True)
        logger = setup_logger_dual(base_out_dir, client_ip)

        if req.asp_logic and req.asp_logic.strip():
            try:
                with open(os.path.join(client_base_dir, "asp_logic.txt"), "w", encoding="utf-8") as f:
                    f.write(req.asp_logic)
            except Exception:
                pass

        verifier = None
        if getattr(req, "ref_doc_path", None) and os.path.exists(req.ref_doc_path):
            try:
                verifier = WordingVerifier(req.ref_doc_path)
                logger.info(f"[verifier] initialized with {req.ref_doc_path}")
            except Exception as e:
                logger.error(f"[verifier] init failed: {e}")

        mode = (req.mode or "random").lower()
        tie_break = (req.tie_break or "stable").lower()
        st_path = state_path(base_out_dir, req.asp_logic, client_ip)
        state_file_lock = _lock_for_state_path(st_path)
        active_run_key = f"{client_ip}|{st_path}|{mode}"

        with _ACTIVE_RUN_KEYS_GUARD:
            if active_run_key in _ACTIVE_RUN_KEYS:
                raise HTTPException(status_code=409, detail="동일 사용자/상태 파일 기준으로 이미 실행 중입니다.")
            _ACTIVE_RUN_KEYS.add(active_run_key)

        if mode == "coverage" and req.persist_state:
            with state_file_lock:
                try:
                    raw = load_json(st_path, None)
                    if isinstance(raw, dict):
                        raw_done = raw.get("done_case_keys", []) or []
                        raw_bad = raw.get("bad_case_keys", []) or []
                        if not isinstance(raw_done, list):
                            raw_done = [raw_done]
                        if not isinstance(raw_bad, list):
                            raw_bad = [raw_bad]
                        if any(isinstance(x, (list, dict, tuple)) for x in (raw_done + raw_bad)):
                            bak = st_path + f".bak_{int(time.time())}"
                            save_json(bak, raw)
                            logger.warning(f"[coverage] legacy state detected. backup={bak}")
                except Exception:
                    pass
                st = load_coverage_state(st_path)
        else:
            st = {"done_case_keys": [], "bad_case_keys": [], "runs": 0}

        done_keys: set[str] = {_normalize_case_key(x) for x in (st.get("done_case_keys", []) or []) if _normalize_case_key(x)}
        bad_keys: set[str] = {_normalize_case_key(x) for x in (st.get("bad_case_keys", []) or []) if _normalize_case_key(x)}

        if mode == "coverage" and not (req.asp_logic and req.asp_logic.strip()):
            raise ValueError("Coverage 모드에서는 ASP Logic이 필수입니다.")

        cases, guards, check_count_rules = _prepare_coverage_cases(req, logger, done_keys, bad_keys)
        plan = compute_plan(req, client_ip)

        if mode == "random":
            run_total = max(1, int(req.repeat or 1))
            tasks: list[tuple[int, Optional[Dict[str, Any]]]] = []
            for i in range(1, run_total + 1):
                tasks.append((i, _augment_overrides(mode, None, guards, check_count_rules, bool(getattr(req, "include_screen_cases", False)))))
            remaining_cases = 0
        else:
            if plan["mode"] == "coverage" and int(plan["planned_total"]) == 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"No remaining cases. extracted={plan['extracted_cases']} remaining={plan['remaining_cases']} done={plan['done_cases']} bad={plan['bad_cases']} state={plan['state_path']}"
                    ),
                )
            run_total = int(plan["planned_total"])
            tasks = []
            pool = list(cases)
            for i in range(1, run_total + 1):
                if not pool:
                    break
                picked = pool.pop(random.randrange(0, len(pool))) if tie_break == "random" else pool.pop(0)
                tasks.append((i, _augment_overrides(mode, picked, guards, check_count_rules, bool(getattr(req, "include_screen_cases", False)))))
            remaining_cases = len(pool)

        total_tasks = len(tasks)
        with STATE.lock:
            STATE.mode = mode
            STATE.planned_total = total_tasks
            STATE.current_run = 0
            STATE.remaining_cases = remaining_cases if mode == "coverage" else 0
            STATE.progress = 0
            STATE.message = "running"

        if total_tasks <= 0:
            with STATE.lock:
                STATE.finish(True, None)
            return

        ok_all = True
        completed = 0
        max_workers = max(1, min(int(getattr(req, "concurrency", 5) or 5), 10, total_tasks))
        logger.info(f"[parallel] workers={max_workers} timeout_sec={int(getattr(req, 'execution_timeout_sec', 600) or 600)} total={total_tasks}")

        futures = {}
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="survey-run") as executor:
            for run_no, case_overrides in tasks:
                with STATE.lock:
                    if STATE.stop_requested:
                        break

                def _check_stop():
                    with STATE.lock:    
                        return STATE.stop_requested
                fut = executor.submit(_run_one_task, req, logger, client_base_dir, mode, run_no, case_overrides, _check_stop, verifier)
                futures[fut] = (run_no, case_overrides)

            for fut in as_completed(futures):
                run_no, case_overrides = futures[fut]
                try:
                    ok, run_dir, case_overrides = fut.result()
                except Exception:
                    ok = False
                    run_dir = ""
                    logger.exception(f"[parallel] worker failed run={run_no}")

                ok_all = ok_all and ok
                completed += 1

                try:
                    from .state_store import read_coverage_trace, update_coverage_state
                    trace = read_coverage_trace(run_dir)
                    if isinstance(trace, dict) and trace:
                        update_coverage_state(base_out_dir, req.asp_logic or "", trace)
                except Exception:
                    pass

                if mode == "coverage" and case_overrides:
                    k = case_key(case_overrides)
                    with state_file_lock:
                        if ok:
                            done_keys.add(k)
                            logger.info(f"[coverage] OK key={k}")
                        else:
                            bad_keys.add(k)
                            logger.warning(f"[coverage] FAIL -> blacklist key={k}")
                        if req.persist_state:
                            st["done_case_keys"] = sorted(done_keys)
                            st["bad_case_keys"] = sorted(bad_keys)
                            st["runs"] = int(st.get("runs", 0)) + 1
                            save_coverage_state(st_path, st)

                with STATE.lock:
                    STATE.current_run = completed
                    if mode == "coverage":
                        STATE.remaining_cases = max(0, total_tasks - completed)
                    STATE.progress = int((completed / max(1, total_tasks)) * 100)
                    STATE.message = f"running ({completed}/{total_tasks})"
                    stop_requested = STATE.stop_requested

                logger.info(f"run {run_no}/{total_tasks} DONE ok={ok}")

                if stop_requested:
                    for pending in futures:
                        pending.cancel()
                    ok_all = False
                    logger.info("STOP requested by user.")
                    break

        if verifier:
            try:
                report_path = verifier.generate_html_report(client_base_dir)
                logger.info(f"[verifier] report generated: {report_path}")
            except Exception as e:
                logger.error(f"[verifier] report generation failed: {e}")

        with STATE.lock:
            if STATE.stop_requested:
                STATE.finish(False, "STOP requested")
            else:
                STATE.finish(ok_all, None if ok_all else "One or more runs failed.")

    except Exception as e:
        msg = str(e) if e is not None else ""
        low = msg.lower()
        user_closed = (
            ("target closed" in low)
            or ("browser closed" in low)
            or ("page closed" in low)
            or ("context or browser has been closed" in low)
            or ("창닫음" in msg)
        )
        try:
            if logger:
                if user_closed:
                    logger.warning("사용자가 브라우저를 닫음.")
                else:
                    logger.exception("[job_runner] failed")
        except Exception:
            pass

        if isinstance(e, ValueError):
            user_msg = msg[:300] if msg else "ASP Logic 오류가 발생했습니다."
        elif isinstance(e, HTTPException):
            d = e.detail if isinstance(e.detail, str) else str(e.detail)
            user_msg = d[:300]
        elif user_closed:
            user_msg = "사용자가 브라우저를 닫음."
        else:
            user_msg = msg[:300] if msg else "실행 중 오류가 발생했습니다."

        try:
            with STATE.lock:
                STATE.finish(False, user_msg)
        except Exception:
            pass

    finally:
        try:
            with STATE.lock:
                STATE.running = False
        except Exception:
            pass
        if active_run_key:
            with _ACTIVE_RUN_KEYS_GUARD:
                _ACTIVE_RUN_KEYS.discard(active_run_key)
