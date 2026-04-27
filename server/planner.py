from __future__ import annotations
from typing import Any

from .state_store import (
    load_json, save_json,
    state_path, load_coverage_state,
    _normalize_case_key, case_key
)
from .asp_cases import extract_cases_from_asp, extract_screen_guards_from_asp, merge_case_with_guards

def compute_plan(req, client_ip: str) -> dict[str, Any]:
    base_out_dir = req.out_dir or "run_logs_pw"
    mode = (req.mode or "random").lower()

    cases: list[dict[str, Any]] = []
    st_path = state_path(base_out_dir, req.asp_logic, client_ip)

    if mode == "coverage" and req.persist_state:
        try:
            raw = load_json(st_path, None)
            if isinstance(raw, dict):
                raw_done = raw.get("done_case_keys", []) or []
                raw_bad  = raw.get("bad_case_keys", []) or []

                if not isinstance(raw_done, list):
                    raw_done = [raw_done]
                if not isinstance(raw_bad, list):
                    raw_bad = [raw_bad]

                if any(isinstance(x, (list, dict, tuple)) for x in (raw_done + raw_bad)):
                    bak = st_path + f".bak_{int(__import__('time').time())}"
                    save_json(bak, raw)
        except Exception:
            pass

        st = load_coverage_state(st_path)
    else:
        st = {"done_case_keys": [], "bad_case_keys": [], "runs": 0}

    done_raw = st.get("done_case_keys", []) or []
    bad_raw  = st.get("bad_case_keys", []) or []

    done_keys: set[str] = { _normalize_case_key(x) for x in done_raw if _normalize_case_key(x) }
    bad_keys:  set[str] = { _normalize_case_key(x) for x in bad_raw  if _normalize_case_key(x) }

    extracted_total = 0
    guards = {}

    if mode == "coverage":
        try:
            cases = extract_cases_from_asp(
                req.asp_logic,
                max_cases=req.max_cases,
                include_default_paths=req.include_default_paths,
                include_screen_cases=req.include_screen_cases,
            )
            extracted_total = len(cases)

            guards = extract_screen_guards_from_asp(req.asp_logic)
            if guards:
                merged_cases = []
                for c in cases:
                    merged_cases.append(merge_case_with_guards(c, guards))
                cases = merged_cases

            if not cases and guards:
                cases = [guards]
                extracted_total = 1

        except Exception as e:
            # ✅ Traceback/내부예외는 숨기고, UI/사용자용 메시지로 치환
            raise ValueError(
                "ASP Logic 형식이 맞지 않습니다. (Case/If 구조 또는 괄호/따옴표 등을 확인하세요.)"
            ) from e

        filtered = []
        for c in cases:
            k = case_key(c)
            if k in done_keys or k in bad_keys:
                continue
            filtered.append(c)
        cases = filtered

    if mode != "coverage":
        run_total = req.repeat
    else:
        if req.auto_until_done:
            run_total = min(len(cases), max(1, int(req.max_total_runs or 200)))
        else:
            run_total = min(len(cases), req.repeat) if cases else req.repeat

    if mode == "coverage":
        if run_total < 0:
            run_total = 0
    else:
        if run_total <= 0:
            run_total = 1

    return {
        "mode": mode,
        "planned_total": int(run_total),
        "extracted_cases": int(extracted_total),
        "remaining_cases": int(len(cases)),
        "done_cases": int(len(done_keys)),
        "bad_cases": int(len(bad_keys)),
        "guards": guards,
        "state_path": st_path,
    }
