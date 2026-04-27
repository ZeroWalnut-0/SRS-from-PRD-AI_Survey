from __future__ import annotations
import re
import random
import logging
from typing import Any, Dict, Optional, Tuple, List, Set
from collections import defaultdict

from playwright.sync_api import Page

from .config import RunnerConfig
from .form_parse import parse_form_fields
from .overrides import apply_overrides_first
from .rank import detect_rank_question_from_var, fill_rank_question_dynamic
from .other_fill import get_selected_values, fill_T_inputs_for_selected, sync_other_inputs_for_base
from .generators import choose_select_value, generate_tel_digits, generate_number, generate_email, generate_text
from .dom_actions import can_set_value, set_checked, set_value
from .utils import click_gap


def _is_context_destroyed_error(exc: Exception) -> bool:
    msg = str(exc or "")
    lowered = msg.lower()
    return (
        "execution context was destroyed" in lowered
        or "cannot find context with specified id" in lowered
        or "most likely because of a navigation" in lowered
        or "target page, context or browser has been closed" in lowered
    )


def _safe_page_evaluate(page: Page, expression: str, arg: Any = None, default: Any = None) -> Any:
    try:
        if arg is None:
            return page.evaluate(expression)
        return page.evaluate(expression, arg)
    except Exception as e:
        if _is_context_destroyed_error(e):
            return default
        raise


def _norm_sort_vals(vals: list[str]) -> list[str]:
    # 문항 응답 코드(숫자 문자열)를 숫자 순서대로 정렬 (1, 10, 2 -> 1, 2, 10)
    return sorted(vals, key=lambda x: int(x) if str(x).isdigit() else x)


def _click_step_next_if_present(page: Page, qname: str, logger: logging.Logger, cfg: RunnerConfig) -> bool:
    base = str(qname or "").strip()
    if not base:
        return False

    prefix = base.split("_", 1)[0].strip() or base
    candidates = [
        f"btn{prefix}Next",
        f"btn{base}Next",
        f"btn_{prefix}_Next",
        f"btn_{base}_Next",
    ]

    clicked = False
    for cid in candidates:
        try:
            clicked = bool(_safe_page_evaluate(
                page,
                """(cid) => {
                  const el = document.getElementById(cid);
                  if (!el) return false;

                  function isVisible(node) {
                    if (!node) return false;
                    try {
                      const cs = window.getComputedStyle(node);
                      if (!cs) return false;
                      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.pointerEvents === 'none') return false;
                    } catch (e) {}
                    try {
                      const r = node.getBoundingClientRect();
                      if (!r || r.width <= 0 || r.height <= 0) return false;
                    } catch (e) {}
                    return true;
                  }

                  if (el.disabled === true) return false;
                  if (!isVisible(el)) return false;

                  try { el.click(); return true; } catch (e) {}
                  try {
                    el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                    el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                    el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                    return true;
                  } catch (e) {}
                  return false;
                }""",
                cid,
                False,
            ))
        except Exception as e:
            logger.debug(f"step-next click check failed: qname={qname} cid={cid} err={e}")
            clicked = False

        if clicked:
            logger.info(f"step-next clicked: qname={qname} button={cid}")
            # 단순 대기가 아닌, DOM 변화나 URL 변화를 감지하는 'Smart Wait' 도입 고려
            try:
                page.wait_for_timeout(getattr(cfg, "step_next_wait_ms", 100))
            except Exception:
                pass
            return True

    return False

def _is_selector_enabled(page: Page, selector: str) -> bool:
    try:
        return can_set_value(page, selector)
    except Exception:
        return False




def _extract_field_context(page: Page, name: str, tag: str = "input", iid: Optional[str] = None) -> str:
    selector = f'{tag}[name="{name}"]' if tag in ("input", "textarea", "select") else name
    try:
        return str(_safe_page_evaluate(
            page,
            r"""(args) => {
              const [sel, iid] = args;
              const el = document.querySelector(sel);
              if (!el) return '';
              const parts = [];
              const push = (v) => {
                const s = String(v || '').replace(/\s+/g, ' ').trim();
                if (s) parts.push(s);
              };

              push(el.getAttribute('placeholder'));
              push(el.getAttribute('title'));
              push(el.getAttribute('aria-label'));
              push(el.getAttribute('data-label'));
              if (iid) {
                const lb = document.querySelector(`label[for="${iid}"]`);
                if (lb) push(lb.innerText || lb.textContent || '');
                const td = document.getElementById('TD_' + iid);
                if (td) push(td.innerText || td.textContent || '');
              }
              const wrap = el.closest('label, td, th, tr, li, .row, .form-group, .question, .q-title, .qtext, .conts, .title');
              if (wrap) push(wrap.innerText || wrap.textContent || '');
              return parts.join(' | ').slice(0, 500);
            }""",
            [selector, iid or ""],
            "",
        ) or "")
    except Exception:
        return ""


def _is_name_enabled(page: Page, name: str, tag: str = "input") -> bool:
    if tag == "textarea":
        selector = f'textarea[name="{name}"]'
    elif tag == "select":
        selector = f'select[name="{name}"]'
    else:
        selector = f'input[name="{name}"]'
    return _is_selector_enabled(page, selector)



def _ensure_radio_selected(page: Page, qname: str, pick: str, logger: logging.Logger, tag: str = "") -> bool:
    """
    1) 현재 checked value 확인
    2) 원하는 pick이 아니면:
       - 매트릭스형: TD_<input.id> 또는 closest(td) 클릭 시도
       - 그래도 안되면 input.click() 시도
    """
    try:
        pick_s = str(pick)

        def _get_checked() -> str:
            return _safe_page_evaluate(
                page,
                """(qname) => {
                  const el = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
                  if(!el) return "";
                  const v = (el.getAttribute("value") || "");
                  return (v !== "" ? v : (el.value || ""));
                }""",
                qname,
                "",
            ) or ""

        ok = _safe_page_evaluate(
            page,
            """([qname, pick]) => {
              let el = document.querySelector(`input[type=\"radio\"][name=\"${qname}\"][value=\"${pick}\"]`);

              if(!el){
                const els = Array.from(document.querySelectorAll(`input[type=\"radio\"][name=\"${qname}\"]`));
                el = els.find(e => {
                  if(!e) return false;
                  const av = (e.getAttribute(\"value\") || "");
                  const pv = (e.value || "");
                  return av === pick || pv === pick;
                }) || null;
              }
              if(!el) return false;

              const id = el.id || "";
              let td = null;
              if(id) td = document.getElementById("TD_" + id);
              if(!td) td = el.closest("td, li, div.form-check");
              if(td){
                try { td.dispatchEvent(new MouseEvent("mousedown", {bubbles:true})); } catch(e){}
                try { td.dispatchEvent(new MouseEvent("mouseup", {bubbles:true})); } catch(e){}
                try { td.dispatchEvent(new MouseEvent("click", {bubbles:true})); } catch(e){}
              } else {
                try { el.click(); } catch(e){}
              }

              el.checked = true;

              try { el.dispatchEvent(new Event("input", {bubbles:true})); } catch(e) {}
              try { el.dispatchEvent(new Event("change", {bubbles:true})); } catch(e) {}

              const checked = document.querySelector(`input[type=\"radio\"][name=\"${qname}\"]:checked`);
              if(!checked) return false;

              const av = (checked.getAttribute("value") || "");
              const pv = (checked.value || "");
              return (av === pick) || (pv === pick);
            }""",
            [qname, pick_s],
            False,
        )

        cur2 = _get_checked()
        if str(cur2) != pick_s:
            logger.warning(f"radio ensure failed{(':'+tag) if tag else ''}: {qname} wanted={pick_s} got={cur2}")
            return False

        return bool(ok)
    except Exception as e:
        logger.warning(f"radio ensure exception{(':'+tag) if tag else ''}: {qname} pick={pick} err={e}")
        return False


def _ensure_radio_selected_by_index(page: Page, name: str, target_index: int, logger: logging.Logger, tag: str = "") -> tuple[bool, str]:
    try:
        picked = _safe_page_evaluate(
            page,
            """([qname, targetIndex]) => {
              const els = Array.from(document.querySelectorAll(`input[type="radio"][name="${qname}"]`));
              const enabled = els.filter(e => e && e.disabled !== true);
              const idx = Number(targetIndex || 0);
              const el = enabled[idx] || null;
              if (!el) return { ok: false, value: '' };

              const clickNode = (node) => {
                if (!node) return false;
                try { node.click(); return true; } catch (e) {}
                try {
                  node.dispatchEvent(new MouseEvent('mousedown', { bubbles:true }));
                  node.dispatchEvent(new MouseEvent('mouseup', { bubbles:true }));
                  node.dispatchEvent(new MouseEvent('click', { bubbles:true }));
                  return true;
                } catch (e) {}
                return false;
              };

              const id = String(el.getAttribute('id') || '');
              let td = null;
              if (id) td = document.getElementById('TD_' + id);
              if (!td) td = el.closest('td');

              if (!clickNode(td)) clickNode(el);

              el.checked = true;

              try { el.dispatchEvent(new Event('input', { bubbles:true })); } catch (e) {}
              try { el.dispatchEvent(new Event('change', { bubbles:true })); } catch (e) {}

              const checked = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
              if (!checked) return { ok: false, value: '' };

              const av = String(checked.getAttribute('value') || '').trim();
              const pv = String(checked.value || '').trim();
              return { ok: true, value: av || pv };
            }""",
            [name, int(target_index)],
            {"ok": False, "value": ""},
        ) or {}
        ok = bool(picked.get("ok"))
        value = str(picked.get("value") or "").strip()
        if not ok:
            logger.warning(f"radio ensure failed{(':'+tag) if tag else ''}: {name} index={target_index} got=")
        return ok, value
    except Exception as e:
        logger.warning(f"radio ensure exception{(':'+tag) if tag else ''}: {name} index={target_index} err={e}")
        return False, ""


def _safe_int(x: Optional[str]) -> Optional[int]:
    try:
        if x is None:
            return None
        s = str(x).strip()
        if s == "":
            return None
        return int(float(s))
    except Exception:
        return None


def _pick_input_value_with_constraints(
    name: str,
    info: Dict[str, Any],
    cmin: Optional[int],
    cmax: Optional[int],
) -> Optional[str]:
    """
    ASP SCREEN 로직에서 추출된 __NUM_CONSTRAINTS__를
    일반 input(text/tel/number)에도 적용하기 위한 값 선택.

    규칙:
    - min/max 둘 다 있으면 범위 안에서 랜덤
    - min만 있으면 [min ~ 안전상한] 범위에서 랜덤
    - max만 있으면 [1 ~ max] 범위에서 랜덤
    """
    # HTML min/max 속성을 고려한 최종 제약 조건 결정
    rmin = cmin if cmin is not None else info.get("min")
    rmax = cmax if cmax is not None else info.get("max")

    if rmin is None and rmax is None:
        return None

    cmin, cmax = rmin, rmax # 기존 로직 호환을 위해 재할당

    maxlen = info.get("maxlength")
    ml: Optional[int] = None
    try:
        if maxlen is not None and str(maxlen).strip() != "":
            ml = int(maxlen)
    except Exception:
        ml = None

    def _cap_by_maxlen(default_cap: int = 9999) -> int:
        if ml is None or ml <= 0:
            return default_cap
        try:
            return min(default_cap, (10 ** ml) - 1)
        except Exception:
            return default_cap

    if cmin is not None and cmax is not None:
        lo = int(cmin)
        hi = int(cmax)
        if hi < lo:
            hi = lo
        val_num = random.randint(lo, hi)

    elif cmin is not None:
        lo = int(cmin)
        nm = (name or "").upper()

        if nm.endswith("_1") and lo >= 1900:
            hi = max(lo, 2026)
        elif ml == 2:
            hi = min(_cap_by_maxlen(99), lo + 20)
        elif ml == 3:
            hi = min(_cap_by_maxlen(999), lo + 100)
        elif ml == 4:
            hi = min(_cap_by_maxlen(9999), lo + 300)
        else:
            hi = min(_cap_by_maxlen(9999), lo + 100)

        if hi < lo:
            hi = lo

        val_num = random.randint(lo, hi)

    else:
        hi = int(cmax)
        if hi < 1:
            hi = 1
        lo = 1
        if hi < lo:
            hi = lo
        val_num = random.randint(lo, hi)

    val = str(val_num)

    try:
        if ml is not None and ml > 0 and len(val) > ml:
            val = val[:ml]
    except Exception:
        pass

    return val


def _get_override_choice_rule(cfg: RunnerConfig, name: str) -> Any:
    try:
        ov = getattr(cfg, "case_overrides", None) or {}
        if isinstance(ov, dict):
            return ov.get(name)
    except Exception:
        pass
    return None


def _filter_choice_values(values: List[str], override_rule: Any) -> Tuple[List[str], Optional[str]]:
    vals = [str(v).strip() for v in (values or []) if str(v).strip() not in ("", "0")]
    if not vals:
        return [], None
    if override_rule is None:
        return vals, None
    rule = str(override_rule).strip()
    if not rule:
        return vals, None
    if rule.startswith("__NEQSET__:"):
        excluded = {x.strip() for x in rule[len("__NEQSET__:"):].split(",") if x.strip()}
        return [v for v in vals if v not in excluded], None
    if rule.startswith("__NEQ__:"):
        excluded = rule[len("__NEQ__:"):].strip()
        return [v for v in vals if v != excluded], None
    if rule in vals:
        return vals, rule
    return vals, None


def _pick_input_value_with_conditional_rules(
    page: Page,
    name: str,
    rules: List[Dict[str, Any]],
) -> Optional[str]:
    """
    __COND_NUM_RULES__에서 target=name인 조건부 숫자 규칙을 찾아
    when 조건이 만족될 때 랜덤 값을 반환한다.
    """
    if not rules:
        return None

    for rule in rules:
        when = rule.get("when", {}) or {}
        target = str(rule.get("target") or "").strip()
        if target != name:
            continue

        matched = True
        for wk, wv in when.items():
            try:
                cur = page.locator(f'[name="{wk}"]').first.input_value().strip()
            except Exception:
                cur = ""
            if str(cur) != str(wv):
                matched = False
                break

        if not matched:
            continue

        rmin = rule.get("min")
        rmax = rule.get("max")

        try:
            if rmin is not None and rmax is not None:
                lo = int(rmin)
                hi = int(rmax)
                if hi < lo:
                    hi = lo
                return str(random.randint(lo, hi))

            if rmin is not None:
                lo = int(rmin)
                hi = lo + 100
                if hi < lo:
                    hi = lo
                return str(random.randint(lo, hi))

            if rmax is not None:
                hi = int(rmax)
                if hi < 1:
                    hi = 1
                return str(random.randint(1, hi))
        except Exception:
            continue

    return None


def _get_checkbox_limits_from_hidden(
    meta: Dict[str, Any], qname: str, enum_len: int
) -> Tuple[int, int, bool, bool, Dict[str, Any]]:
    """
    qname 예: "Q4"
    hidden:
      - "MIQ4CNT" : 최소 선택수 (0 또는 없음이면 1개 이상으로 해석)
      - "MQ4CNT"  : 최대 선택수 (0 또는 없음이면 제한 없음으로 해석)

    반환:
      (min_pick, max_pick, found_min, found_max, debug_info)
    """
    hidden = meta.get("hidden", {}) or {}

    min_key = f"MI{qname}CNT"
    max_key = f"M{qname}CNT"

    raw_min = hidden.get(min_key)
    raw_max = hidden.get(max_key)

    found_min = (min_key in hidden) and (str(raw_min).strip() != "")
    found_max = (max_key in hidden) and (str(raw_max).strip() != "")

    mi = _safe_int(raw_min)
    ma = _safe_int(raw_max)

    min_pick = mi if (mi is not None and mi >= 1) else 1
    max_pick = ma if (ma is not None and ma >= 1) else enum_len

    if enum_len <= 0:
        min_pick = 0
        max_pick = 0
    else:
        if min_pick > enum_len:
            min_pick = enum_len
        if max_pick > enum_len:
            max_pick = enum_len
        if max_pick < min_pick:
            max_pick = min_pick

    dbg = {
        "min_key": min_key,
        "max_key": max_key,
        "raw_min": raw_min,
        "raw_max": raw_max,
        "mi": mi,
        "ma": ma,
        "found_min": found_min,
        "found_max": found_max,
        "resolved_min": min_pick,
        "resolved_max": max_pick,
        "enum_len": enum_len,
    }
    return min_pick, max_pick, found_min, found_max, dbg



def _looks_like_phone_field(name: str, iid: Optional[str], context_text: str = "") -> bool:
    blob = f"{name or ''} {iid or ''} {context_text or ''}".lower()
    return bool(re.search(r"(mobile|phone|hand|hp|cell|tel|연락처|휴대폰|핸드폰|전화)", blob))


def _pick_reasonable_numeric_input_value(
    name: str,
    info: Dict[str, Any],
    context_text: str = "",
    min_v: Optional[int] = None,
    max_v: Optional[int] = None,
) -> str:
    maxlen = info.get("maxlength")
    try:
        ml = int(maxlen) if maxlen is not None and str(maxlen).strip() != "" else None
    except Exception:
        ml = None

    if min_v is None:
        min_v = 1
    if max_v is None:
        if ml is not None and ml > 0:
            max_v = min((10 ** ml) - 1, 999 if ml <= 4 else (10 ** ml) - 1)
        else:
            max_v = 999

    lo = int(min_v)
    hi = int(max_v)
    if hi < lo:
        hi = lo

    ctx = str(context_text or "").lower()
    nm = str(name or "").lower()

    # 연도처럼 보이면 최근 과거 연도로 제한
    is_year = False
    if ml == 4 and (re.search(r"(year|년도|연식|출생|생년|since)", ctx) or nm.endswith("_year") or nm == "yy" or nm.startswith("year")):
        lo = max(lo, 1900)
        hi = min(hi, 2015)
        if hi < lo:
            hi = lo
        is_year = True

    # 금액/횟수류 짧은 numeric 입력은 과도한 값 방지
    if not is_year and ml is not None and ml <= 4 and not _looks_like_phone_field(name, info.get("id"), context_text):
        hi = min(hi, 1000 if ml >= 4 else (10 ** ml) - 1)
        lo = max(lo, 1)
        if hi < lo:
            hi = lo

    return str(random.randint(lo, hi))


def _detect_numeric_series_groups(
    meta: Dict[str, Any],
    page: Page,
) -> Dict[str, List[str]]:
    inputs_meta = meta.get("inputs_meta", {}) or {}
    checks = meta.get("checks", {}) or {}
    suffix_pat = re.compile(r"^([A-Za-z][A-Za-z0-9]*)_(\d+)$")

    grouped: Dict[str, List[Tuple[int, str]]] = {}
    for name, info in inputs_meta.items():
        m = suffix_pat.match(str(name))
        if not m:
            continue
        itype = str((info or {}).get("type") or "").lower()
        if itype not in ("tel", "number", "text"):
            continue
        base = m.group(1)
        idx = int(m.group(2))
        grouped.setdefault(base, []).append((idx, name))

    out: Dict[str, List[str]] = {}
    for base, pairs in grouped.items():
        if len(pairs) < 2:
            continue
        pairs.sort(key=lambda x: x[0])
        names = [nm for _, nm in pairs]

        # *_NONE 동반 구조면 숫자형 계단/가격 문항으로 간주
        none_count = sum(1 for nm in names if f"{nm}_NONE" in checks)
        if none_count >= max(1, len(names) // 2):
            out[base] = names
            continue

        # 전부 짧은 길이 + 실제 enabled input이면 일반 숫자 series로도 허용
        short_numeric = True
        for nm in names:
            info = inputs_meta.get(nm, {}) or {}
            ml = info.get("maxlength")
            try:
                ml = int(ml) if ml is not None and str(ml).strip() != "" else None
            except Exception:
                ml = None
            if ml is not None and ml > 6:
                short_numeric = False
                break
        if short_numeric:
            out[base] = names

    return out


def _fill_numeric_series_groups(
    page: Page,
    meta: Dict[str, Any],
    groups: Dict[str, List[str]],
    num_cons: Dict[str, Any],
    logger: logging.Logger,
) -> Set[str]:
    handled: Set[str] = set()
    inputs_meta = meta.get("inputs_meta", {}) or {}
    checks = meta.get("checks", {}) or {}

    for base, names in groups.items():
        enabled_names: List[str] = []
        active_none_names: Set[str] = set()

        for nm in names:
            none_nm = f"{nm}_NONE"
            if none_nm in checks:
                try:
                    is_none = bool(_safe_page_evaluate(
                        page,
                        """(qname) => {
                          const el = document.querySelector(`input[type="checkbox"][name="${qname}"]`);
                          return !!(el && el.checked);
                        }""",
                        none_nm,
                        False,
                    ))
                except Exception:
                    is_none = False
                if is_none:
                    active_none_names.add(nm)
                    continue

            if _is_name_enabled(page, nm, tag="input"):
                enabled_names.append(nm)

        if len(enabled_names) < 2:
            continue

        prev_val: Optional[int] = None
        for i, nm in enumerate(enabled_names):
            info = inputs_meta.get(nm, {}) or {}
            context_text = _extract_field_context(page, nm, tag="input", iid=info.get("id"))

            # HTML min/max 속성 파싱 결과와 설정 파일 제약 조건 결합
            cmin_rule = num_cons.get(nm) if isinstance(num_cons, dict) else None
            cmin = cmin_rule.get("min") if isinstance(cmin_rule, dict) and cmin_rule.get("min") is not None else None
            cmax = cmin_rule.get("max") if isinstance(cmin_rule, dict) and cmin_rule.get("max") is not None else None

            hmin = info.get("min")
            hmax = info.get("max")

            lo = int(cmin) if cmin is not None else (int(hmin) if hmin is not None else 1)
            hi = int(cmax) if cmax is not None else (int(hmax) if hmax is not None else None)

            if prev_val is not None:
                lo = max(lo, prev_val)

            remaining = len(enabled_names) - i - 1
            if hi is None:
                hi = min(max(lo, prev_val or lo) + max(20, remaining * 50), 1000)
            else:
                hi = int(hi)

            if hi < lo:
                hi = lo

            val = _pick_reasonable_numeric_input_value(
                name=nm,
                info=info,
                context_text=context_text,
                min_v=lo,
                max_v=hi,
            )
            ok = set_value(page, f'input[name="{nm}"]', val)
            if ok:
                handled.add(nm)
                prev_val = int(float(val))
                logger.info(f"input(series): {nm}={val} base={base}")
            else:
                logger.info(f"input(series skip disabled/runtime): {nm}")

    return handled


def _detect_radio_series_groups(meta: Dict[str, Any]) -> Dict[str, List[str]]:
    radios = meta.get("radios", {}) or {}
    suffix_pat = re.compile(r"^([A-Za-z][A-Za-z0-9]*)_(\d+)$")

    grouped: Dict[str, List[Tuple[int, str]]] = {}
    enum_map: Dict[str, List[str]] = {}

    for name, enum in radios.items():
        m = suffix_pat.match(str(name))
        if not m:
            continue
        vals = [str(v).strip() for v in (enum or []) if str(v).strip() != ""]
        if len(vals) < 2:
            continue
        base = m.group(1)
        idx = int(m.group(2))
        grouped.setdefault(base, []).append((idx, name))
        enum_map[name] = vals

    out: Dict[str, List[str]] = {}
    for base, pairs in grouped.items():
        if len(pairs) < 3:
            continue
        pairs.sort(key=lambda x: x[0])
        names = [nm for _, nm in pairs]

        first_vals = enum_map.get(names[0], [])
        if len(first_vals) < 2:
            continue

        same_domain = True
        first_set = set(first_vals)
        for nm in names[1:]:
            cur_vals = enum_map.get(nm, [])
            if set(cur_vals) != first_set:
                same_domain = False
                break

        if same_domain:
            out[base] = names

    return out


def _spread_radio_series_values(
    page: Page,
    meta: Dict[str, Any],
    groups: Dict[str, List[str]],
    cfg: RunnerConfig,
    logger: logging.Logger,
) -> Set[str]:
    handled: Set[str] = set()
    radios = meta.get("radios", {}) or {}

    for base, names in groups.items():
        enabled_names: List[str] = []
        value_lists: Dict[str, List[str]] = {}

        for nm in names:
            already_checked = _safe_page_evaluate(
                page,
                """(qname) => {
                  const el = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
                  return el ? String(el.getAttribute("value") || el.value || "").trim() : "";
                }""",
                nm,
                "",
            ) or ""
            if already_checked:
                handled.add(nm)
                selvals = get_selected_values(page, nm)
                fill_T_inputs_for_selected(page, meta, nm, selvals, cfg, logger)
                continue

            info = _safe_page_evaluate(
                page,
                """(qname) => {
                  const els = Array.from(document.querySelectorAll(`input[type="radio"][name="${qname}"]`));
                  const enabled = els.filter(e => e && e.disabled !== true);
                  return enabled.map(e => {
                    const av = String(e.getAttribute("value") || "").trim();
                    const pv = String(e.value || "").trim();
                    return av || pv;
                  }).filter(v => String(v || "").trim() !== "");
                }""",
                nm,
                [],
            ) or []

            vals = [str(v).strip() for v in info if str(v).strip() != ""]
            if len(vals) < 2:
                continue

            override_rule = _get_override_choice_rule(cfg, nm)
            vals, forced_pick = _filter_choice_values(vals, override_rule)
            if forced_pick is not None:
                vals = [forced_pick]
            if not vals:
                continue

            enabled_names.append(nm)
            value_lists[nm] = vals

        if len(enabled_names) < 3:
            continue

        common_vals = None
        for nm in enabled_names:
            cur = value_lists.get(nm, [])
            cur_set = list(dict.fromkeys(cur))
            if common_vals is None:
                common_vals = cur_set
            else:
                common_vals = [v for v in common_vals if v in set(cur_set)]

        if not common_vals or len(common_vals) < 2:
            continue

        common_vals = list(common_vals)
        random.shuffle(common_vals)

        freq: Dict[str, int] = defaultdict(int)
        for idx, nm in enumerate(enabled_names):
            try:
                is_missing = not bool(page.evaluate(
                    """(n) => !!document.querySelector(`[name="${n}"], [name^="${n}_"]`)""",
                    nm
                ))
            except Exception:
                is_missing = True
            
            if is_missing:
                logger.warning(f"Field '{nm}' is missing (possibly auto-advanced). Aborting radio series loop.")
                break

            ordered = sorted(
                value_lists.get(nm, []),
                key=lambda v: (freq.get(v, 0), common_vals.index(v) if v in common_vals else 9999, random.random()),
            )

            chosen_pick: Optional[str] = None
            for pick in ordered:
                sel = f'input[type="radio"][name="{nm}"][value="{pick}"]'
                ok = bool(set_checked(page, sel, True))
                if ok:
                    # set_checked 성공 → TD onclick만 경량으로 발생 (page.evaluate 1회, 검증 개르업)
                    _safe_page_evaluate(
                        page,
                        """([qname, pick]) => {
                          let el = document.querySelector(`input[type="radio"][name="${qname}"][value="${pick}"]`);
                          if (!el) return;
                          const id = el.id || "";
                          let td = id ? document.getElementById("TD_" + id) : null;
                          if (!td) td = el.closest("td, li, div.form-check");
                          if (td) {
                            try { td.dispatchEvent(new MouseEvent("click", {bubbles:true})); } catch(e) {}
                          }
                          try { el.dispatchEvent(new Event("change", {bubbles:true})); } catch(e) {}
                        }""",
                        [nm, str(pick)],
                        None,
                    )
                    chosen_pick = str(pick)
                    break
                # set_checked 실패 → full ensure 시도 (TD 클릭 + 검증 포함)
                ok = _ensure_radio_selected(page, nm, str(pick), logger, tag="series")
                if ok:
                    chosen_pick = str(pick)
                    break

            if chosen_pick is None:
                for ordinal_idx in range(len(value_lists.get(nm, []))):
                    ok_idx, actual_pick = _ensure_radio_selected_by_index(page, nm, ordinal_idx, logger, tag="series-index")
                    if ok_idx:
                        chosen_pick = str(actual_pick or "").strip()
                        if chosen_pick:
                            break

            if chosen_pick is None:
                logger.warning(f"radio(series): {nm} base={base} all candidates failed={ordered}")
                continue

            handled.add(nm)
            freq[str(chosen_pick)] += 1
            logger.info(f"radio(series): {nm}={chosen_pick} base={base} freq={dict(freq)}")

            selvals = get_selected_values(page, nm)
            fill_T_inputs_for_selected(page, meta, nm, selvals, cfg, logger)
            _click_step_next_if_present(page, nm, logger, cfg)

            try:
                page.wait_for_timeout(50)  # 300ms → 50ms: 고정 대기 축소 (n행 매트릭스 로우로 인한 성능 개선)
            except Exception:
                pass

    return handled


def autofill_page_by_dom(page: Page, cfg: RunnerConfig, logger: logging.Logger) -> Dict[str, Any]:
    # 0) 알림창(Dialog) 핸들러 설정
    if not getattr(page, "_dialog_handler_attached", False):
        def handle_dialog(dialog):
            try:
                msg = dialog.message
                logger.warning(f"browser-dialog detected: type={dialog.type} message={msg}")
                if any(kw in msg for kw in ["성공", "업로드", "등록되었습니다", "완료"]):
                    logger.info(f"browser-dialog: dismissing success alert: {msg}")
                else:
                    if not hasattr(cfg, "_last_validation_alert"):
                        setattr(cfg, "_last_validation_alert", [])
                    getattr(cfg, "_last_validation_alert").append(msg)
                
                # 이미 다른 리스너에 의해 처리된 경우를 방지
                dialog.accept()
            except Exception as e:
                pass

        page.on("dialog", handle_dialog)
        setattr(page, "_dialog_handler_attached", True)

    # 1) 폼 정보 추출 (Iframe 포함)
    html = page.content()
    meta = parse_form_fields(html)
    
    # 모든 프레임을 순환하며 추가 문항 및 메타데이터 병합
    for frame in page.frames:
        if frame == page.main_frame:
            continue
        try:
            f_html = frame.content()
            f_meta = parse_form_fields(f_html)
            if f_meta.get("has_form"):
                # 메타데이터 병합 (기본 페이지 데이터 우선)
                for k in ["radios", "checks", "selects", "hidden", "inputs_meta"]:
                    if k in f_meta:
                        for key, val in f_meta[k].items():
                            if key not in meta.get(k, {}):
                                meta.setdefault(k, {})[key] = val
                if "textareas" in f_meta:
                    meta.setdefault("textareas", []).extend([t for t in f_meta["textareas"] if t not in meta["textareas"]])
                if "canvases" in f_meta:
                    meta.setdefault("canvases", []).extend([c for c in f_meta["canvases"] if c not in meta["canvases"]])
        except Exception:
            pass

    if not meta.get("has_form"):
        logger.info("No <form> found (even in frames).")
        return {"ok": False, "reason": "no_form"}

    # 2) 전체 필드 컨텍스트 일괄 추출 (성능 개선)
    all_names = list(meta.get("inputs_meta", {}).keys()) + list(meta.get("radios", {}).keys()) + \
                list(meta.get("checks", {}).keys()) + list(meta.get("selects", {}).keys())
    
    ctx_map = page.evaluate(
        """(names) => {
            const out = {};
            const pickText = (el) => {
                if (!el) return "";
                const wrap = el.closest('label, td, th, tr, li, .row, .form-group, .question, .q-title, .qtext, .conts, .title');
                return (wrap ? (wrap.innerText || wrap.textContent || "") : "").replace(/\\s+/g, " ").trim().slice(0, 500);
            };
            for (const n of names) {
                const el = document.querySelector(`[name="${n}"], [id="${n}"]`);
                if (el) out[n] = pickText(el);
            }
            return out;
        }""",
        list(set(all_names))
    ) or {}

    handled = apply_overrides_first(page, meta, cfg, logger)
    inputs_meta = meta.get("inputs_meta", {})
    series_handled: Set[str] = set()

    def _is_missing(qname: str) -> bool:
        if not qname: return False
        try:
            return not bool(page.evaluate(
                """(n) => !!document.querySelector(`[name="${n}"], [name^="${n}_"]`)""",
                qname
            ))
        except Exception:
            return True

    def _is_consent_question(qname: str) -> bool:
        # 일괄 추출된 컨텍스트 맵 사용
        context = (ctx_map.get(qname) or "").lower()
        qname_low = qname.lower()
        keywords = ["agree", "consent", "동의", "승인", "수락", "개인정보", "활용"]
        return any(kw in qname_low or kw in context for kw in keywords)

    def _is_positive_value(val: str, label: str) -> bool:
        v = str(val).upper()
        l = str(label or "").lower()
        # 값 자체가 긍정형인 경우 (Y, 1, YES)
        if v in ("Y", "1", "YES"):
            return True
        # 라벨에 긍정형 키워드가 포함된 경우
        if any(kw in l for kw in ["동의함", "동의합니다", "동의", "수락", "yes", "agree"]):
            # 부정형 키워드가 섞여있지 않은지도 확인 (예: '동의하지 않음')
            if "안함" in l or "않음" in l or "부동의" in l or "no" in l or "하지" in l:
                return False
            return True
        return False

    def _get_user_name_from_page() -> str:
        # 성함 입력 필드 찾기 (NAME, NAME1, NAME2, 성함, 성명 등)
        return page.evaluate(
            """() => {
                const names = ['NAME', 'NAME1', 'NAME2', 'userName', 'p_name', 'nm', 'P_Nm'];
                for (const n of names) {
                    const el = document.querySelector(`input[name="${n}"], input[id="${n}"]`);
                    if (el && el.value && el.value.trim().length > 0) return el.value.trim();
                }
                const allInps = Array.from(document.querySelectorAll('input[type="text"]'));
                for (const el of allInps) {
                    const lab = (el.getAttribute('placeholder') || '' + (el.getAttribute('title') || '')).toLowerCase();
                    if (lab.includes('성명') || lab.includes('성함') || lab.includes('이름')) {
                        if (el.value && el.value.trim().length > 0) return el.value.trim();
                    }
                    const wrap = el.closest('label, td, th, tr, li, .row, .form-group');
                    if (wrap && (wrap.innerText || '').toLowerCase().match(/(성명|성함|이름)/)) {
                        if (el.value && el.value.trim().length > 0) return el.value.trim();
                    }
                }
                return '';
            }"""
        ) or ""


    # 0) Rank 먼저 처리
    rk = detect_rank_question_from_var(meta)
    if rk:
        base = rk["base"]
        need = rk["need"]
        picks = fill_rank_question_dynamic(page, base, need, cfg, logger)
        if picks:
            fill_T_inputs_for_selected(page, meta, base, set(picks), cfg, logger)
        return {"ok": True, "rank": rk}

    # 숫자 제약
    num_cons: Dict[str, Any] = {}
    cond_num_rules: List[Dict[str, Any]] = []

    try:
        ov = getattr(cfg, "case_overrides", None) or {}
        if isinstance(ov, dict):
            cond_num_rules = ov.get("__COND_NUM_RULES__", []) or []
            if not isinstance(cond_num_rules, list):
                cond_num_rules = []
    except Exception:
        cond_num_rules = []

    try:
        ov = getattr(cfg, "case_overrides", None) or {}
        if isinstance(ov, dict):
            num_cons = ov.get("__NUM_CONSTRAINTS__", {}) or {}
            if not isinstance(num_cons, dict):
                num_cons = {}
    except Exception:
        num_cons = {}

    # 1) radio series groups 먼저 균형 분산 응답
    radio_series_groups = _detect_radio_series_groups(meta)
    radio_series_handled = _spread_radio_series_values(page, meta, radio_series_groups, cfg, logger)

    # 2) radio (required)
    for name, enum in meta.get("radios", {}).items():
        if name in handled or name in series_handled or name in radio_series_handled:
            continue

        if _is_missing(name):
            logger.warning(f"Field '{name}' is missing (possibly auto-advanced). Aborting autofill to press Next.")
            return {"ok": True, "reason": "auto_advanced"}


        # 이미 선택된 값이 있으면 페이지 JS가 맞춰둔 상태를 유지
        already_checked = _safe_page_evaluate(
            page,
            """(qname) => {
            const el = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
            return el ? String(el.value || "").trim() : "";
            }""",
            name,
            "",
        ) or ""

        if already_checked:
            logger.info(f"radio(required): {name} keep existing checked={already_checked}")
            # 이미 checked라도 setRadioValue() 같은 커스텀 onclick이 수행되도록 TD 클릭 발생
            _ensure_radio_selected(page, name, already_checked, logger, tag="required-keep")
            selvals = get_selected_values(page, name)
            fill_T_inputs_for_selected(page, meta, name, selvals, cfg, logger)
            continue

        info = _safe_page_evaluate(
            page,
            """(qname) => {
            const els = Array.from(document.querySelectorAll(`input[type="radio"][name="${qname}"]`));
            const enabled = els.filter(e => e && e.disabled !== true);
            return enabled.map(e => ({
                hasValueAttr: e.hasAttribute("value"),
                attrValue: e.getAttribute("value"),
                propValue: e.value,
                finalValue: (e.hasAttribute("value") && (e.getAttribute("value")||"")!=="") ? e.getAttribute("value") : (e.value||"")
            }));
            }""",
            name,
            [],
        ) or []

        if not info:
            logger.info(f"radio(required): {name} no enabled radios -> skip")
            continue

        cons = num_cons.get(name) if isinstance(num_cons, dict) else None
        cmin = cons.get("min") if isinstance(cons, dict) and cons.get("min") is not None else None
        cmax = cons.get("max") if isinstance(cons, dict) and cons.get("max") is not None else None

        vals_all: List[Dict[str, str]] = []
        for x in info:
            fv = str(x.get("finalValue") or "").strip()
            if fv:
                # 라벨 정보 확보 (동의 여부 판별용)
                label = page.evaluate(
                    """([qname, val]) => {
                        const el = document.querySelector(`input[type="radio"][name="${qname}"][value="${val}"]`);
                        if (!el) return '';
                        const id = el.id || '';
                        if (id) {
                            const lb = document.querySelector(`label[for="${id}"]`);
                            if (lb) return lb.innerText || lb.textContent || '';
                        }
                        const wrap = el.closest('label');
                        if (wrap) return wrap.innerText || wrap.textContent || '';
                        return '';
                    }""",
                    [name, fv]
                ) or ""
                vals_all.append({"v": fv, "label": label})

        vals = [x["v"] for x in vals_all]

        # '동의' 유형 질문인 경우 긍정적 답변 우선순위 부여
        is_consent = _is_consent_question(name)
        positive_vals = [x["v"] for x in vals_all if _is_positive_value(x["v"], x["label"])]
        
        override_rule = _get_override_choice_rule(cfg, name)
        # forced_pick이 있으면 그것을 따르고, 없으면 positive_vals가 있을 때 그 중에서 선택 시도
        vals_filtered, forced_pick = _filter_choice_values(vals, override_rule)

        if forced_pick is None and is_consent and positive_vals:
            # 필터링된 결과값 중에서 긍정적인 답변이 있는지 확인
            available_positives = [v for v in vals_filtered if v in positive_vals]
            if available_positives:
                forced_pick = random.choice(available_positives)
                logger.info(f"radio(consent-heuristic): {name} choosing positive option {forced_pick}")

        if (cmin is not None) or (cmax is not None):
            numeric_vals = [v for v in vals if v.isdigit()]
            if numeric_vals:
                if cmin is not None:
                    numeric_vals = [v for v in numeric_vals if int(v) >= int(cmin)]
                if cmax is not None:
                    numeric_vals = [v for v in numeric_vals if int(v) <= int(cmax)]
                if numeric_vals:
                    vals = numeric_vals

        if vals:
            pick = forced_pick if forced_pick is not None else random.choice(vals)
            sel = f'input[type="radio"][name="{name}"][value="{pick}"]'
            set_checked(page, sel, True)
            _ensure_radio_selected(page, name, str(pick), logger, tag="required")
            logger.info(f"radio(required): {name}={pick} (min={cmin}, max={cmax})")
        else:
            _safe_page_evaluate(
                page,
                """(qname) => {
                const els = Array.from(document.querySelectorAll(`input[type="radio"][name="${qname}"]`));
                const first = els.find(e => e && e.disabled !== true);
                if (first) first.click();
                }""",
                name,
                None,
            )
            logger.info(f"radio(required): {name} picked first enabled (no usable value)")

        checked = _safe_page_evaluate(
            page,
            """(qname) => {
            const el = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
            return el ? true : false;
            }""",
            name,
            False,
        )
        if not checked:
            if vals:
                pick = forced_pick if forced_pick is not None else random.choice(vals)
                sel = f'input[type="radio"][name="{name}"][value="{pick}"]'
                set_checked(page, sel, True)
                _ensure_radio_selected(page, name, str(pick), logger, tag="required-retry")
                logger.info(f"radio(required): {name} re-try by value={pick} (min={cmin}, max={cmax})")
            else:
                _safe_page_evaluate(
                    page,
                    """(qname) => {
                    const els = Array.from(document.querySelectorAll(`input[type="radio"][name="${qname}"]`));
                    const first = els.find(e => e && e.disabled !== true);
                    if (first) first.click();
                    }""",
                    name,
                    None,
                )
            checked2 = _safe_page_evaluate(
                page,
                """(qname) => !!document.querySelector(`input[type="radio"][name="${qname}"]:checked`)""",
                name,
                False,
            )
            logger.info(f"radio(required): {name} re-try checked={checked2}")

        selvals = get_selected_values(page, name)
        fill_T_inputs_for_selected(page, meta, name, selvals, cfg, logger)
        _click_step_next_if_present(page, name, logger, cfg)
        try:
            page.wait_for_timeout(50)  # 300ms → 50ms: 단일 라디오 불필요한 대기 축소
        except Exception:
            pass


    # 2) checkbox
    hidden = meta.get("hidden", {}) or {}
    suffix_pat = re.compile(r"^(.+)_([0-9]+)$")

    suffix_groups: Dict[str, Dict[str, Any]] = {}
    checks_dict = meta.get("checks", {}) or {}
    for full_name, enum in checks_dict.items():
        if full_name.endswith("_NONE"):
            logger.info(f"checkbox(skip): {full_name} endswith _NONE")
            continue

        m = suffix_pat.match(full_name)
        if not m:
            continue
        base = m.group(1)

        if (f"{base}CNT" not in hidden) and (f"MI{base}CNT" not in hidden) and (f"M{base}CNT" not in hidden):
            continue

        if not enum:
            continue

        suffix_groups.setdefault(base, {"members": [], "values": [], "enum_by_member": {}})
        suffix_groups[base]["members"].append(full_name)

        for v in enum:
            suffix_groups[base]["values"].append(str(v))
        suffix_groups[base]["enum_by_member"][full_name] = [str(v) for v in enum]

    def _suffix_num(nm: str) -> int:
        mm = suffix_pat.match(nm)
        return int(mm.group(2)) if mm else 0

    for base in suffix_groups:
        suffix_groups[base]["members"].sort(key=_suffix_num)
        try:
            suffix_groups[base]["values"] = sorted(list(set(suffix_groups[base]["values"])), key=lambda x: int(x))
        except Exception:
            suffix_groups[base]["values"] = list(dict.fromkeys(suffix_groups[base]["values"]))

    if not hasattr(cfg, "_exclusive_blacklist"):
        setattr(cfg, "_exclusive_blacklist", defaultdict(set))
    _exclusive_blacklist = getattr(cfg, "_exclusive_blacklist")

    if not hasattr(cfg, "_disable_sideeffect_blacklist"):
        setattr(cfg, "_disable_sideeffect_blacklist", defaultdict(set))
    _disable_sideeffect_blacklist = getattr(cfg, "_disable_sideeffect_blacklist")

    def _disabled_controls_snapshot(exclude_qname: str) -> set[str]:
        return set(
            page.evaluate(
                """([exclude]) => {
                function key(el){
                    const tag = (el.tagName||"").toLowerCase();
                    const t = (el.getAttribute("type")||"").toLowerCase();
                    const id = el.getAttribute("id") || "";
                    const nm = el.getAttribute("name") || "";
                    const v  = el.getAttribute("value") || "";
                    return `${tag}:${t}:${id}:${nm}:${v}`;
                }

                function isDisabledLike(node){
                    if(!node) return true;
                    if (node.disabled === true) return true;

                    let cur = node;
                    while(cur){
                      if (cur.getAttribute && cur.getAttribute("aria-disabled") === "true") return true;
                      if (cur.classList && cur.classList.contains("disabled")) return true;
                      cur = cur.parentElement;
                    }

                    try {
                      const cs = window.getComputedStyle(node);
                      if (cs && cs.pointerEvents === "none") return true;
                    } catch(e) {}

                    return false;
                }

                const els = Array.from(document.querySelectorAll("input,select,textarea,button"));
                const out = [];
                for(const el of els){
                    if(!el) continue;
                    const nm = el.getAttribute("name") || "";
                    if(exclude && nm === exclude) continue;

                    if(isDisabledLike(el)){
                      out.push(key(el));
                    }
                }
                return out;
                }""",
                [exclude_qname],
            )
        )

    def _check_causes_new_disabled(qname: str, v: str) -> tuple[bool, list[str]]:
        before = _disabled_controls_snapshot(qname)

        sel = f'input[type="checkbox"][name="{qname}"][value="{v}"]'
        ok = set_checked(page, sel, True)
        click_gap(cfg)

        if not ok:
            return True, ["__CHECK_FAILED__"]

        page.wait_for_timeout(15)

        after = _disabled_controls_snapshot(qname)
        new_disabled = sorted(list(after - before))
        if new_disabled:
            set_checked(page, sel, False)
            click_gap(cfg)
            page.wait_for_timeout(10)
            return True, new_disabled

        return False, []

    scope = getattr(cfg, "exclusive_blacklist_scope", "run")
    if scope not in ("run", "page"):
        scope = "run"

    if not hasattr(cfg, "_unstable_questions"):
        setattr(cfg, "_unstable_questions", defaultdict(set))
    _unstable_questions = getattr(cfg, "_unstable_questions")

    def _page_key() -> str:
        try:
            u = page.url or ""
            return u.split("?", 1)[0]
        except Exception:
            return "unknown_page"

    def _qkey(qname: str) -> str:
        if scope == "page":
            return f"{_page_key()}::{qname}"
        return qname

    def _mark_unstable(qname: str, reason: str):
        k = _qkey(qname)
        _unstable_questions[k].add(reason)

    def _log_checkbox_summary(qname: str, msg: str):
        logger.info(f"checkbox({qname}): {msg}")

    def _to_int(x, default=0):
        try:
            if x is None:
                return default
            s = str(x).strip()
            if s == "":
                return default
            return int(float(s))
        except Exception:
            return default

    def _get_min_max_for_checkbox(base_name: str, option_count: int):
        min_key = f"MI{base_name}CNT"
        max_key = f"M{base_name}CNT"

        min_raw = hidden.get(min_key, None)
        max_raw = hidden.get(max_key, None)

        mn = _to_int(min_raw, 0)
        mx = _to_int(max_raw, 0)

        if mx == 0:
            mx = option_count
        else:
            mx = max(0, min(mx, option_count))

        if mn == 0:
            mn = 1
        else:
            mn = max(0, min(mn, option_count))

        if mx < mn:
            mx = mn

        return mn, mx, min_key, max_key, min_raw, max_raw

    def _get_exclusive_values_for_question(qname: str):
        return page.evaluate(
            """([qname]) => {
              function norm(s){ return (s==null?"":String(s)).trim(); }

              function parseNoCheck(s){
                const oc = norm(s);
                if(!oc) return null;
                const re1 = /noCheckBoxValue\\(\\s*['"]([^'"]+)['"]\\s*,\\s*['"]([^'"]+)['"]\\s*\\)/i;
                const m = oc.match(re1);
                if(!m) return null;
                return { idArg: norm(m[1]), v: norm(m[2]) };
              }

              function findOnclickUp(el){
                let cur = el;
                for(let i=0; i<4 && cur; i++){
                  const oc = cur.getAttribute && cur.getAttribute("onclick");
                  if(oc) return oc;
                  cur = cur.parentElement;
                }
                return "";
              }

              const out = [];
              const seen = new Set();

              const inputs = Array.from(document.querySelectorAll('input[type="checkbox"][name="'+qname+'"]'));

              for(const inp of inputs){
                const v = norm(inp.value);
                if(!v) continue;

                const oc = norm(inp.getAttribute("onclick")) || norm(findOnclickUp(inp));
                const parsed = parseNoCheck(oc);

                if(parsed && parsed.v && parsed.v === v){
                  if(!seen.has(v)){
                    seen.add(v);
                    out.push(v);
                  }
                }else{
                  if(parsed && parsed.v){
                    if(!seen.has(parsed.v)){
                      seen.add(parsed.v);
                      out.push(parsed.v);
                    }
                  }
                }
              }

              return out;
            }""",
            [qname],
        )

    def _sleep_after_click():
        page.wait_for_timeout(getattr(cfg, "checkbox_post_click_ms", 15))

    def _verify_checkbox_state(qname: str, expected_checked: Optional[set[str]] = None) -> Dict[str, Any]:
        expected = list(expected_checked) if expected_checked else None
        return page.evaluate(
            """([qname, expected]) => {
              function norm(s){ return (s==null?"":String(s)).trim(); }
              const inputs = Array.from(document.querySelectorAll('input[type="checkbox"][name="'+qname+'"]'));
              const st = inputs.map(i => ({
                v: norm(i.value),
                checked: !!i.checked,
                disabled: !!i.disabled
              }));
              const checked = st.filter(x=>x.checked).map(x=>x.v);
              const disabled = st.filter(x=>x.disabled).map(x=>x.v);

              let ok = true;
              let reason = "";

              if(expected){
                const exp = new Set(expected.map(norm));
                const got = new Set(checked.map(norm));
                if(exp.size !== got.size) ok=false;
                else {
                  for(const v of exp){ if(!got.has(v)) { ok=false; break; } }
                }
                if(!ok){
                  reason = `checked mismatch. expected=${Array.from(exp).join(",")} got=${checked.join(",")}`;
                }
              }

              return { ok, reason, checked, disabled, snapshot: st };
            }""",
            [qname, expected],
        )

    def _filter_enabled_values(qname: str, values: List[str]) -> List[str]:
        if not values:
            return []
        return page.evaluate(
            """([qname, vals]) => {
            const set = new Set((vals||[]).map(String));
            const boxes = Array.from(document.querySelectorAll(
                `input[type="checkbox"][name="${qname}"]`
            ));

            function isDisabledLike(node){
                if(!node) return true;
                if (node.disabled === true) return true;

                let cur = node;
                while(cur){
                  if (cur.getAttribute && cur.getAttribute("aria-disabled") === "true") return true;
                  if (cur.classList && cur.classList.contains("disabled")) return true;
                  cur = cur.parentElement;
                }

                try {
                  const cs = window.getComputedStyle(node);
                  if (cs && cs.pointerEvents === "none") return true;
                } catch(e) {}
                return false;
            }

            const enabled = [];
            for (const b of boxes) {
                const v = String(b.value||"");
                if (set.has(v) && !isDisabledLike(b)) enabled.push(v);
            }
            return enabled;
            }""",
            [qname, values],
        ) or []


    def _exclusive_disabled_all_others(qname: str, picked_v: str) -> bool:
        return bool(
            page.evaluate(
                """([qname, pickedV]) => {
                  const boxes = Array.from(document.querySelectorAll(
                    `input[type="checkbox"][name="${qname}"]`
                  ));
                  const others = boxes.filter(b => String(b.value) !== String(pickedV));
                  if (others.length === 0) return true;

                  const disabledCount = others.filter(b => b.disabled === true).length;
                  const uncheckedCount = others.filter(b => b.checked === false).length;

                  return (disabledCount === others.length) && (uncheckedCount === others.length);
                }""",
                [qname, picked_v],
            )
        )

    # (A) 일반 checkbox
    for name, enum in meta.get("checks", {}).items():
        if name in handled or not enum:
            continue
        if _is_missing(name):
            logger.warning(f"Field '{name}' is missing (possibly auto-advanced). Aborting autofill to press Next.")
            return {"ok": True, "reason": "auto_advanced"}

        if name.endswith("_NONE"):
            logger.info(f"checkbox(skip): {name} endswith _NONE (general loop)")
            continue

        m = suffix_pat.match(name)
        if m:
            base = m.group(1)
            if base in suffix_groups:
                continue

        opt_n = len(enum)
        mn, mx, min_key, max_key, min_raw, max_raw = _get_min_max_for_checkbox(name, opt_n)

        exclusive_vals = []
        try:
            exclusive_vals = _get_exclusive_values_for_question(name) or []
        except Exception:
            exclusive_vals = []

        exclusive_vals = [str(v).strip() for v in exclusive_vals if str(v).strip() != ""]
        exclusive_set = set(exclusive_vals)

        exclusive_vals = [v for v in exclusive_vals if v in set(enum)]
        banned = _exclusive_blacklist[_qkey(name)]
        exclusive_vals = [v for v in exclusive_vals if str(v) not in banned]
        exclusive_set = set(exclusive_vals)

        normal_enum = [v for v in enum if v not in exclusive_set]
        normal_enum = _filter_enabled_values(name, [str(v) for v in normal_enum])

        bad_disable = _disable_sideeffect_blacklist[_qkey(name)]
        normal_enum = [v for v in normal_enum if str(v) not in bad_disable]

        chose_exclusive = False
        if exclusive_vals and (random.random() < 0.1):
            v = random.choice(exclusive_vals)
            logger.info(
                f"checkbox: {name} EXCLUSIVE(noCheckBoxValue) prob-hit -> pick_only={v} "
                f"(min={mn} max={mx} {min_key}={min_raw} {max_key}={max_raw})"
            )

            for vv in enum:
                sel_off = f'input[type="checkbox"][name="{name}"][value="{vv}"]'
                set_checked(page, sel_off, False)
                click_gap(cfg)

            sel_on = f'input[type="checkbox"][name="{name}"][value="{v}"]'
            set_checked(page, sel_on, True)
            click_gap(cfg)

            _sleep_after_click()

            expected = {str(v)}
            st1 = _verify_checkbox_state(name, expected_checked=expected)
            if not st1.get("ok", False):
                logger.warning(f"checkbox: {name} exclusive verify failed (1st). {st1.get('reason','')}")
                for vv in enum:
                    sel_off = f'input[type="checkbox"][name="{name}"][value="{vv}"]'
                    set_checked(page, sel_off, False)
                    click_gap(cfg)
                set_checked(page, sel_on, True)
                click_gap(cfg)
                _sleep_after_click()

                st2 = _verify_checkbox_state(name, expected_checked=expected)
                if not st2.get("ok", False):
                    logger.warning(f"checkbox: {name} exclusive verify failed (2nd). {st2.get('reason','')}")
                    for vv in enum:
                        if str(vv) == str(v):
                            continue
                        sel_other = f'input[type="checkbox"][name="{name}"][value="{vv}"]'
                        set_checked(page, sel_other, False)
                        click_gap(cfg)

                    _sleep_after_click()
                    st3 = _verify_checkbox_state(name, expected_checked=expected)
                    if not st3.get("ok", False):
                        logger.warning(
                            f"checkbox: {name} exclusive final verify still mismatch. "
                            f"checked={_norm_sort_vals(st3.get('checked') or [])} disabled={_norm_sort_vals(st3.get('disabled') or [])}"
                        )
                else:
                    logger.info(f"checkbox: {name} exclusive verify ok (2nd)")
            else:
                logger.info(f"checkbox: {name} exclusive verify ok (1st)")

            fired = _exclusive_disabled_all_others(name, str(v))
            if not fired:
                _log_checkbox_summary(name, f"EXCLUSIVE fired=FAIL -> blacklist v={v}")
                _mark_unstable(name, "exclusive_failed")

                _exclusive_blacklist[_qkey(name)].add(str(v))

                set_checked(page, sel_on, False)
                click_gap(cfg)
                _sleep_after_click()

                chose_exclusive = False
            else:
                _log_checkbox_summary(name, f"EXCLUSIVE fired=OK v={v}")
                chose_exclusive = True

            if chose_exclusive:
                selvals = get_selected_values(page, name)
                fill_T_inputs_for_selected(page, meta, name, selvals, cfg, logger)

        if chose_exclusive:
            continue

        if not normal_enum:
            if exclusive_vals:
                v = random.choice(exclusive_vals)
                logger.info(f"checkbox: {name} normal_empty -> fallback EXCLUSIVE only pick={v} (min={mn} max={mx})")
                for vv in enum:
                    sel_off = f'input[type="checkbox"][name="{name}"][value="{vv}"]'
                    set_checked(page, sel_off, False)
                    click_gap(cfg)

                sel_on = f'input[type="checkbox"][name="{name}"][value="{v}"]'
                set_checked(page, sel_on, True)
                click_gap(cfg)
                _sleep_after_click()

                fired = _exclusive_disabled_all_others(name, str(v))
                if not fired:
                    _log_checkbox_summary(name, f"FALLBACK-EXCLUSIVE fired=FAIL -> blacklist v={v}")
                    _mark_unstable(name, "fallback_exclusive_failed")

                    _exclusive_blacklist[_qkey(name)].add(str(v))
                    set_checked(page, sel_on, False)
                    click_gap(cfg)
                    _sleep_after_click()
                    continue

                click_gap(cfg)
                selvals = get_selected_values(page, name)
                fill_T_inputs_for_selected(page, meta, name, selvals, cfg, logger)
            else:
                logger.warning(f"checkbox: {name} enum exists but normal_enum empty and no exclusive detected")
            continue

        normal_n = len(normal_enum)
        mn2 = min(mn, normal_n) if normal_n > 0 else 0
        mx2 = min(mx, normal_n) if normal_n > 0 else 0
        if mx2 < mn2:
            mx2 = mn2

        if cfg.checkbox_select_all:
            k = mx2
        else:
            k = random.randint(mn2, mx2) if mx2 >= mn2 else mn2

        picks = list(normal_enum) if k >= normal_n else random.sample(normal_enum, k)

        logger.info(
            f"checkbox: {name} opt={opt_n} normal={normal_n} exclusive={list(exclusive_set)} "
            f"min={mn}->{mn2} max={mx}->{mx2} "
            f"({min_key}={min_raw}, {max_key}={max_raw}) "
            f"pick_count={len(picks)} picks={picks}"
        )

        actually_picked: List[str] = []
        for v in picks:
            if str(v) in _disable_sideeffect_blacklist[_qkey(name)]:
                continue

            caused, new_disabled = _check_causes_new_disabled(name, str(v))
            if caused:
                logger.warning(f"checkbox: {name} skip value={v} (caused new disabled controls: {len(new_disabled)})")
                _disable_sideeffect_blacklist[_qkey(name)].add(str(v))
                _mark_unstable(name, "caused_disable_other_inputs")
                continue

            actually_picked.append(str(v))

        picks = actually_picked

        _sleep_after_click()
        stn = _verify_checkbox_state(name, expected_checked=None)
        checked_now = stn.get("checked", []) or []
        disabled_now = set(stn.get("disabled", []) or [])

        if len(checked_now) < mn2:
            _log_checkbox_summary(name, f"normal picked but checked<{mn2} (got={len(checked_now)}). will try top-up.")
            need_more = mn2 - len(checked_now)

            remaining = [vv for vv in normal_enum if (vv not in checked_now and vv not in disabled_now)]
            random.shuffle(remaining)

            attempts = 0
            for vv in remaining:
                if need_more <= 0:
                    break
                attempts += 1

                caused, new_disabled = _check_causes_new_disabled(name, str(vv))
                if caused:
                    logger.warning(f"checkbox: {name} TOP-UP skip value={vv} (caused new disabled controls: {len(new_disabled)})")
                    _disable_sideeffect_blacklist[_qkey(name)].add(str(vv))
                    _mark_unstable(name, "caused_disable_other_inputs")
                    continue

                stx = _verify_checkbox_state(name, expected_checked=None)
                checked_now = stx.get("checked", []) or []
                disabled_now = set(stx.get("disabled", []) or [])
                need_more = mn2 - len(checked_now)

            _sleep_after_click()
            sty = _verify_checkbox_state(name, expected_checked=None)
            checked_now2 = sty.get("checked", []) or []

            if len(checked_now2) < mn2:
                _log_checkbox_summary(name, f"TOP-UP failed: checked<{mn2} (got={len(checked_now2)}). checked={_norm_sort_vals(checked_now2)}")
                _mark_unstable(name, "min_not_met")
            else:
                _log_checkbox_summary(name, f"TOP-UP ok: checked={_norm_sort_vals(checked_now2)} (attempts={attempts})")
                checked_now = checked_now2

        selvals = get_selected_values(page, name)
        fill_T_inputs_for_selected(page, meta, name, selvals, cfg, logger)
        _click_step_next_if_present(page, name, logger, cfg)

        try:
            page.wait_for_timeout(300)
        except Exception:
            pass

    # (B) suffix checkbox group

    for base, g in suffix_groups.items():
        members: List[str] = g["members"]
        values: List[str] = g["values"]

        if _is_missing(base):
            logger.warning(f"Field group '{base}' is missing (possibly auto-advanced). Aborting autofill to press Next.")
            return {"ok": True, "reason": "auto_advanced"}


        rule = None
        try:
            ov = getattr(cfg, "case_overrides", None) or {}
            rr = ov.get("__CHECK_COUNT_RULES__", {}) or {}
            if isinstance(rr, dict):
                rule = rr.get(base)
        except Exception:
            rule = None

        handled_members = [m for m in members if m in handled]
        if handled_members and not rule:
            logger.info(f"checkbox-group: {base} skipped (handled by overrides: {handled_members})")
            continue
        if handled_members and rule:
            logger.info(f"checkbox-group: {base} has count-rule, so handled overrides will be normalized by group logic: {handled_members}")

        enabled_members = page.evaluate(
            """(members) => {
            function isDisabledLike(node){
                if(!node) return true;
                if (node.disabled === true) return true;

                let cur = node;
                while(cur){
                  if (cur.getAttribute && cur.getAttribute("aria-disabled") === "true") return true;
                  if (cur.classList && cur.classList.contains("disabled")) return true;
                  cur = cur.parentElement;
                }

                try {
                  const cs = window.getComputedStyle(node);
                  if (cs && cs.pointerEvents === "none") return true;
                } catch(e) {}

                return false;
            }

            const out = [];
            for (const nm of (members||[])){
                const el = document.querySelector('input[type="checkbox"][name="'+nm+'"]');
                if(!el) continue;
                if(!isDisabledLike(el)) out.push(nm);
            }
            return out;
            }""",
            members,
        )

        if not enabled_members:
            logger.warning(f"checkbox-group: {base} skipped (no enabled members)")
            continue

        members = enabled_members
        enum_by_member = g.get("enum_by_member", {}) or {}
        values = []
        for nm in members:
            for v in (enum_by_member.get(nm) or []):
                values.append(str(v))

        if not values:
            logger.warning(f"checkbox-group: {base} skipped (no enabled values)")
            continue

        opt_n = len(values)
        mn, mx, min_key, max_key, min_raw, max_raw = _get_min_max_for_checkbox(base, opt_n)

        # Detect exclusive checkboxes like noCheckBoxValue
        exclusive_vals_raw = page.evaluate(
            """([base, vals]) => {
              const out = [];
              for (const v of vals) {
                const nm = base + "_" + v;
                const el = document.querySelector('input[name="'+nm+'"]');
                if (el) {
                  const oc = String(el.getAttribute('onclick') || '');
                  if (oc.indexOf('noCheckBoxValue') >= 0 || oc.indexOf('noCheck') >= 0) {
                    out.push(String(v));
                  }
                }
              }
              return out;
            }""",
            [base, values]
        ) or []
        exclusive_vals = [str(x) for x in exclusive_vals_raw if str(x) in values]

        chose_exclusive = False
        if exclusive_vals and random.random() < 0.1:
            v_ex = random.choice(exclusive_vals)
            logger.info(f"checkbox-group: {base} EXCLUSIVE(noCheckBoxValue) prob-hit -> pick_only={v_ex}")
            for v0 in values:
                nm0 = f"{base}_{v0}"
                set_checked(page, f'input[type="checkbox"][name="{nm0}"]', False)
            click_gap(cfg)
            nm_ex = f"{base}_{v_ex}"
            set_checked(page, f'input[type="checkbox"][name="{nm_ex}"]', True)
            click_gap(cfg)
            chose_exclusive = True
            
        if chose_exclusive:
            try:
                page.evaluate(
                    "(base) => { if (typeof window.colorCheckbox === 'function') window.colorCheckbox(base); }",
                    base
                )
            except Exception:
                pass
            continue

        prefer_stay = bool(getattr(cfg, "prefer_stay_on_default_path", True))

        none_vals: set[str] = set()
        for x in exclusive_vals: none_vals.add(str(x))
        count_domain: List[str] = []

        r_min: Optional[int] = None
        if prefer_stay and rule:
            r_from, r_to = rule.get("range", (None, None))
            r_min = rule.get("min", None)
            none_vals = set(str(v) for v in (rule.get("none_values") or []) if str(v).strip())

            if isinstance(r_from, int) and isinstance(r_to, int) and isinstance(r_min, int):
                count_domain = [v for v in values if v.isdigit() and (r_from <= int(v) <= r_to)]
                count_domain = [v for v in count_domain if v not in none_vals]
            else:
                count_domain = []

        pick_pool = list(values)
        if prefer_stay and rule and count_domain:
            pick_pool = list(count_domain)
        else:
            if none_vals:
                pick_pool = [v for v in pick_pool if v not in none_vals] or list(values)

        pick_pool = [v for v in pick_pool if str(v).strip()]
        try:
            pick_pool = sorted(list(dict.fromkeys(pick_pool)), key=lambda x: int(x) if str(x).isdigit() else x)
        except Exception:
            pick_pool = list(dict.fromkeys(pick_pool))

        if not pick_pool:
            logger.warning(f"checkbox-group: {base} skipped (empty pick_pool)")
            continue

        pool_n = len(pick_pool)

        mn2 = min(mn, pool_n) if pool_n > 0 else 0
        mx2 = min(mx, pool_n) if pool_n > 0 else 0
        if prefer_stay and rule and (r_min is not None) and isinstance(r_min, int) and r_min >= 0:
            mn2 = min(r_min, pool_n)
            if mx2 < mn2:
                mx2 = mn2

        if cfg.checkbox_select_all:
            k = mx2
        else:
            k = random.randint(mn2, mx2) if mx2 >= mn2 else mn2

        picks = list(pick_pool) if k >= pool_n else random.sample(pick_pool, k)

        for v0 in values:
            nm0 = f"{base}_{v0}"
            set_checked(page, f'input[type="checkbox"][name="{nm0}"]', False)
        click_gap(cfg)
        page.wait_for_timeout(getattr(cfg, "checkbox_group_settle_ms", 20))

        failed = []
        for v in picks:
            nm = f"{base}_{v}"
            ok = set_checked(page, f'input[type="checkbox"][name="{nm}"]', True)
            click_gap(cfg)
            if not ok:
                failed.append(nm)

        if failed:
            logger.warning(f"checkbox-group: {base} pick failed (disabledLike?): {failed}")

        page.wait_for_timeout(getattr(cfg, "checkbox_group_settle_ms", 20))

        if prefer_stay and rule and count_domain:
            def _checked_vals() -> List[str]:
                return page.evaluate(
                    """([base, vals]) => {
                    const out = [];
                    for (const v of (vals||[])){
                        const nm = base + "_" + String(v);
                        const el = document.querySelector('input[type="checkbox"][name="'+nm+'"]');
                        if (el && el.checked) out.push(String(v));
                    }
                    return out;
                    }""",
                    [base, values]
                ) or []

            checked_vals = _checked_vals()
            cd_set = set(count_domain)
            cnt_now = sum(1 for v in checked_vals if v in cd_set)

            if cnt_now < mn2:
                need_more = mn2 - cnt_now
                remain = [v for v in count_domain if v not in set(checked_vals)]
                random.shuffle(remain)

                attempts = 0
                for v in remain:
                    if need_more <= 0:
                        break
                    nm = f"{base}_{v}"
                    set_checked(page, f'input[type="checkbox"][name="{nm}"]', True)
                    click_gap(cfg)
                    page.wait_for_timeout(getattr(cfg, "checkbox_group_settle_ms", 20))
                    attempts += 1

                    checked_vals = _checked_vals()
                    cnt_now = sum(1 for x in checked_vals if x in cd_set)
                    need_more = mn2 - cnt_now

                logger.info(f"checkbox-group({base}): top-up cnt_now={cnt_now}/{mn2} attempts={attempts} checked={_norm_sort_vals(checked_vals)}")

            if none_vals:
                for nv in none_vals:
                    nm = f"{base}_{nv}"
                    set_checked(page, f'input[type="checkbox"][name="{nm}"]', False)
                click_gap(cfg)
                page.wait_for_timeout(getattr(cfg, "checkbox_group_settle_ms", 20))

        try:
            page.evaluate(
                """(base) => {
                try {
                    if (typeof window.colorCheckbox === "function") window.colorCheckbox(base);
                } catch(e) {}
                }""",
                base
            )
        except Exception:
            pass

        page.wait_for_timeout(getattr(cfg, "checkbox_group_settle_ms", 20))
        try:
            actual_selvals = get_selected_values(page, base)
            sync_other_inputs_for_base(page, meta, base, cfg, logger)
        except Exception as exc:
            logger.warning(f"checkbox-group: {base} other-sync failed: {exc}")
            actual_selvals = get_selected_values(page, base)
        logger.info(f"checkbox-group: {base} picks={picks} checked={_norm_sort_vals(actual_selvals)}")

    try:
        if _unstable_questions:
            prefix = _page_key() + "::" if scope == "page" else ""
            related = {k: _norm_sort_vals(list(v)) for k, v in _unstable_questions.items() if (not prefix or k.startswith(prefix))}
            if related:
                logger.warning(f"checkbox unstable summary(scope={scope}): {related}")
    except Exception:
        pass

    # 3) select
    for name, static_values in meta.get("selects", {}).items():
        if name in handled:
            continue
        if not _is_name_enabled(page, name, tag="select"):
            logger.info(f"select(skip disabled): {name}")
            continue

        # cascading drop-down 지원: 이전 속성 변경(Ajax 등)으로 옵션이 뒤늦게 채워지는 경우를 대기
        attempts = 0
        live_values = []
        while attempts < 5:
            live_values = page.evaluate(
                """(name) => {
                    const sel = document.querySelector('select[name="'+name+'"]');
                    if(!sel) return null;
                    return Array.from(sel.options).map(o => o.value);
                }""",
                name
            ) or static_values
            
            valid_opts = [val for val in live_values if val and str(val).strip() not in ("0", "")]
            if valid_opts or attempts == 4:
                break
            page.wait_for_timeout(100)
            attempts += 1

        v = choose_select_value(live_values, cfg)
        if v is None:
            continue
        page.evaluate(
            """([name, v]) => {
              const el = document.querySelector('select[name="'+name+'"]');
              if (!el) return;
              el.value = v;
              el.dispatchEvent(new Event('input',{bubbles:true}));
              el.dispatchEvent(new Event('change',{bubbles:true}));
            }""",
            [name, v],
        )
        logger.info(f"select: {name}={v}")

    # 4) numeric series groups (e.g. D3_1..D3_4) 먼저 정렬/단조 증가 형태로 채움
    numeric_series_groups = _detect_numeric_series_groups(meta, page)
    series_handled = _fill_numeric_series_groups(page, meta, numeric_series_groups, num_cons, logger)

    # 4) inputs (general) - T* 스킵
    for name, info in inputs_meta.items():
        if name in handled or name in series_handled:
            continue

        itype = (info.get("type") or "text").lower()
        maxlen = info.get("maxlength")
        pattern = info.get("pattern")

        if itype in ("hidden", "radio", "checkbox", "submit", "button", "image", "file", "reset"):
            continue
        if name[:1].upper() == "T":
            continue
        if not _is_name_enabled(page, name, tag="input"):
            logger.info(f"input(skip disabled): {name}")
            continue

        cons = num_cons.get(name) if isinstance(num_cons, dict) else None
        cmin = cons.get("min") if isinstance(cons, dict) and cons.get("min") is not None else None
        cmax = cons.get("max") if isinstance(cons, dict) and cons.get("max") is not None else None

        hmin = info.get("min")
        hmax = info.get("max")
        
        # 설정 파일 제약 조건 우선, 없으면 HTML min/max 사용
        min_v = cmin if cmin is not None else hmin
        max_v = cmax if cmax is not None else hmax

        forced_val = _pick_input_value_with_constraints(name, info, min_v, max_v)

        cond_forced_val = _pick_input_value_with_conditional_rules(page, name, cond_num_rules)
        if cond_forced_val is not None:
            forced_val = cond_forced_val

        # itype == "number" 등 수치형 입력 시 최종 min_v/max_v 적용 확인
        if forced_val is not None and itype in ("tel", "number", "text"):
            val = forced_val
            ok = set_value(page, f'input[name="{name}"]', val)
            if ok:
                handled.add(name)
                logger.info(f"input({itype}, constrained): {name}={val} (min={min_v}, max={max_v})")
            else:
                logger.info(f"input(skip disabled/runtime): {name}")
            continue

        context_text = _extract_field_context(page, name, tag="input", iid=info.get("id"))

        if itype == "tel":
            if _looks_like_phone_field(name, info.get("id"), context_text):
                val = generate_tel_digits(maxlen, pattern, name=name, iid=info.get("id"))
            else:
                val = _pick_reasonable_numeric_input_value(
                    name=name,
                    info=info,
                    context_text=context_text,
                    min_v=min_v,
                    max_v=max_v,
                )
        elif itype == "number":
            if (min_v is not None) or (max_v is not None):
                val = _pick_reasonable_numeric_input_value(
                    name=name,
                    info=info,
                    context_text=context_text,
                    min_v=min_v,
                    max_v=max_v,
                )
            else:
                val = generate_number(maxlen)
        elif itype == "email":
            val = generate_email(maxlen, name=name)
        else:
            if pattern and re.search(r"\d", str(pattern)) and not _looks_like_phone_field(name, info.get("id"), context_text):
                val = _pick_reasonable_numeric_input_value(
                    name=name,
                    info=info,
                    context_text=context_text,
                    min_v=min_v,
                    max_v=max_v,
                )
            else:
                val = generate_text(
                    maxlen=maxlen,
                    name=name,
                    iid=info.get("id"),
                    pattern=pattern,
                    context_text=context_text,
                    multiline=False,
                )

        ok = set_value(page, f'input[name="{name}"]', val)
        if ok:
            handled.add(name)
            logger.info(f"input({itype}): {name}={val}")
        else:
            logger.info(f"input(skip disabled/runtime): {name}")

    # 5) textarea (general) - T* 스킵
    for name in meta.get("textareas", []):
        if name in handled:
            continue
        if name[:1].upper() == "T":
            continue
        if not _is_name_enabled(page, name, tag="textarea"):
            logger.info(f"textarea(skip disabled): {name}")
            continue
        val = generate_text(
            maxlen=None,
            name=name,
            iid=None,
            pattern=None,
            context_text=_extract_field_context(page, name, tag="textarea"),
            multiline=True,
        )
        ok = set_value(page, f'textarea[name="{name}"]', val)
        if ok:
            logger.info(f"textarea: {name}={val}")
        else:
            logger.info(f"textarea(skip disabled/runtime): {name}")

    # 6) Canvas Signature (서명 패드 지원 - Iframe 포함)
    try:
        targets = list(dict.fromkeys([page.main_frame] + page.frames))
        for frame in targets:
            canvases = frame.locator("canvas")
            count = canvases.count()
            for i in range(count):
                loc = canvases.nth(i)
                if loc.is_visible():
                    try:
                        loc.scroll_into_view_if_needed()
                        page.wait_for_timeout(100)
                    except Exception:
                        pass
                    
                    # 서명 그리기
                    box = loc.bounding_box()
                    if box and box["width"] > 50 and box["height"] > 30:
                        logger.info(f"canvas[signature]: drawing fast random scribble on canvas {i} in frame {frame.name or frame.url}")
                        try:
                            cx = box["x"] + box["width"] * 0.5
                            cy = box["y"] + box["height"] * 0.5
                            page.mouse.move(cx + random.uniform(-20, 20), cy + random.uniform(-20, 20))
                            page.mouse.down()
                            for _ in range(random.randint(3, 5)):
                                tx = cx + random.uniform(-box["width"] * 0.3, box["width"] * 0.3)
                                ty = cy + random.uniform(-box["height"] * 0.3, box["height"] * 0.3)
                                page.mouse.move(tx, ty, steps=2)
                            page.mouse.up()
                            logger.info(f"canvas[signature]: fast scribble completed")
                        except Exception as draw_err:
                            logger.warning(f"canvas[signature]: scribble failed - {draw_err}")
    except Exception as e:
        logger.warning(f"canvas[signature]: attempt failed - {e}")

    checked_cnt = page.evaluate(
        """() => document.querySelectorAll('input[type="radio"]:checked, input[type="checkbox"]:checked').length"""
    )
    logger.info(f"checked_count_after_fill={checked_cnt}")

    return {"ok": True}