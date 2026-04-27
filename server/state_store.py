from __future__ import annotations
import os
import json
import time
import hashlib
from typing import Any, Set

from runner.loggers import ip_to_dirname

def load_json(path: str, default: Any):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path: str, obj: Any):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def asp_logic_hash(s: str) -> str:
    s = (s or "").strip().encode("utf-8", errors="ignore")
    return hashlib.md5(s).hexdigest()[:12]

def state_path(base_out_dir: str, asp_logic: str, client_ip: str) -> str:
    h = asp_logic_hash(asp_logic)
    return os.path.join(base_out_dir, "coverage_state", f"{ip_to_dirname(client_ip)}_{h}.json")

def _normalize_case_key(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if isinstance(x, (list, tuple)):
        parts = []
        for item in x:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                parts.append(f"{item[0]}={item[1]}")
            else:
                parts.append(str(item))
        return "|".join(parts)
    if isinstance(x, dict):
        return "|".join([f"{k}={x[k]}" for k in sorted(x.keys())])
    return str(x)

def load_coverage_state(path: str) -> dict:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                st = json.load(f)
        else:
            st = {}
    except Exception:
        st = {}

    done_raw = st.get("done_case_keys", []) or []
    bad_raw = st.get("bad_case_keys", []) or []

    done = []
    for x in done_raw:
        k = _normalize_case_key(x)
        if k:
            done.append(k)

    bad = []
    for x in bad_raw:
        k = _normalize_case_key(x)
        if k:
            bad.append(k)

    return {
        "done_case_keys": done,
        "bad_case_keys": bad,
        "runs": int(st.get("runs") or 0),
    }

def save_coverage_state(path: str, st: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def case_key(case: dict[str, Any]) -> str:
    return "|".join([f"{k}={case[k]}" for k in sorted(case.keys())])

def cov_state_path(base_out_dir: str, asp_logic: str) -> str:
    h = asp_logic_hash(asp_logic)
    # 전역 1개가 아니라, 설문 로직(hash)별 1개로 분리
    return os.path.join(base_out_dir, f"coverage_state_{h}.json")

def read_coverage_trace(run_dir: str) -> dict[str, Any]:
    p = os.path.join(run_dir, "coverage_trace.json")
    return load_json(p, {})

def update_coverage_state(base_out_dir: str, asp_logic: str, trace: dict[str, Any]):
    p = cov_state_path(base_out_dir, asp_logic)
    st = load_json(p, {"visited_pages": [], "visited_edges": [], "runs": 0, "last_update": None})

    vp: Set[str] = set(st.get("visited_pages") or [])
    ve: Set[str] = set(st.get("visited_edges") or [])

    for x in trace.get("visited_pages", []) or []:
        vp.add(str(x))
    for e in trace.get("visited_edges", []) or []:
        ve.add(str(e))

    st["visited_pages"] = sorted(vp)
    st["visited_edges"] = sorted(ve)
    st["runs"] = int(st.get("runs") or 0) + 1
    st["last_update"] = int(time.time())

    save_json(p, st)
    return st
