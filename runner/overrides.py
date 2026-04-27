from __future__ import annotations
from typing import Any, Dict, Set, List, Optional
import logging
import random
from playwright.sync_api import Page

from .config import RunnerConfig
from .dom_actions import set_checked, set_value, click_with_td_fallback
from .other_fill import get_selected_values, fill_T_inputs_for_selected


def _safe_eval(page: Page, expression: str, arg: Any = None, default: Any = None) -> Any:
    try:
        if arg is None:
            return page.evaluate(expression)
        return page.evaluate(expression, arg)
    except Exception:
        return default


def _radio_candidates(page: Page, name: str) -> List[str]:
    vals = _safe_eval(
        page,
        """(qname) => {
        function norm(v){ return (v == null ? '' : String(v)).trim(); }
        function isVisible(el){
            if (!el) return false;
            try {
                const cs = window.getComputedStyle(el);
                if (cs && (cs.display === 'none' || cs.visibility === 'hidden' || cs.pointerEvents === 'none')) return false;
            } catch (e) {}
            let cur = el;
            for (let i = 0; i < 8 && cur; i += 1) {
                try {
                    const cs = window.getComputedStyle(cur);
                    if (cs && (cs.display === 'none' || cs.visibility === 'hidden')) return false;
                } catch (e) {}
                cur = cur.parentElement;
            }
            try {
                const r = el.getBoundingClientRect();
                if (r && r.width > 0 && r.height > 0) return true;
            } catch (e) {}
            return false;
        }
        const els = Array.from(document.querySelectorAll(`input[type="radio"][name="${qname}"]`));
        const enabled = els.filter(el => el && el.disabled !== true);
        const visibleEnabled = enabled.filter(isVisible);
        const picked = visibleEnabled.length ? visibleEnabled : enabled;
        return picked
          .map(el => norm(el.getAttribute('value') || el.value))
          .filter(v => v !== '');
        }""",
        name,
        [],
    ) or []
    out: List[str] = []
    seen = set()
    for v in vals:
        sv = str(v).strip()
        if not sv or sv in seen:
            continue
        seen.add(sv)
        out.append(sv)
    return out


def _ensure_radio_selected(page: Page, name: str, pick: str) -> bool:
    try:
        click_with_td_fallback(page, f'input[type="radio"][name="{name}"][value="{pick}"]')
    except Exception:
        pass
    try:
        set_checked(page, f'input[type="radio"][name="{name}"][value="{pick}"]', True)
    except Exception:
        pass
    checked = _safe_eval(
        page,
        """([qname, pick]) => {
        const el = document.querySelector(`input[type="radio"][name="${qname}"][value="${pick}"]`);
        return !!(el && el.checked);
        }""",
        [name, str(pick)],
        False,
    )
    return bool(checked)


def _select_usable_options(page: Page, name: str, excluded: Optional[List[str]] = None) -> List[str]:
    excluded = [str(x) for x in (excluded or [])]
    vals = _safe_eval(
        page,
        """([name, excludedValues]) => {
        const excluded = new Set((excludedValues || []).map(v => (v ?? '').toString()));
        const el = document.querySelector('select[name="'+name+'"]');
        if (!el) return [];
        const out = [];
        const opts = Array.from(el.options || []);
        for (const o of opts) {
            if (o.disabled) continue;
            const ov = (o.value ?? '').toString();
            if (!ov) continue;
            if (excluded.has(ov)) continue;
            out.push(ov);
        }
        return out;
        }""",
        [name, excluded],
        [],
    )
    return [str(v) for v in (vals or []) if str(v).strip()]


def _select_first_usable_option(page: Page, name: str, excluded: Optional[List[str]] = None) -> Optional[str]:
    excluded = [str(x) for x in (excluded or [])]
    return _safe_eval(
        page,
        """([name, excludedValues]) => {
        const excluded = new Set((excludedValues || []).map(v => (v ?? '').toString()));
        const el = document.querySelector('select[name="'+name+'"]');
        if (!el) return null;
        const opts = Array.from(el.options || []);
        for (const o of opts) {
            if (o.disabled) continue;
            const ov = (o.value ?? '').toString();
            if (!ov) continue;
            if (excluded.has(ov)) continue;
            return ov;
        }
        return null;
        }""",
        [name, excluded],
        None,
    )


def apply_overrides_first(page: Page, meta: Dict[str, Any], cfg: RunnerConfig, logger: logging.Logger) -> Set[str]:
    handled: Set[str] = set()
    ov = getattr(cfg, "case_overrides", None) or {}
    if not isinstance(ov, dict) or not ov:
        return handled

    inputs_meta = meta.get("inputs_meta", {})
    radios = meta.get("radios", {})
    checks = meta.get("checks", {})
    selects = meta.get("selects", {})
    textareas = set(meta.get("textareas", []))

    for name, val in ov.items():
        if not name:
            continue

        NEQ_PREFIX = "__NEQ__:"
        NEQSET_PREFIX = "__NEQSET__:"

        if name in radios:
            pick = str(val)
            radio_vals = _radio_candidates(page, name)
            chosen: Optional[str] = None

            if pick.startswith(NEQ_PREFIX) or pick.startswith(NEQSET_PREFIX):
                if pick.startswith(NEQSET_PREFIX):
                    excluded_values = [x.strip() for x in pick[len(NEQSET_PREFIX):].split(",") if x.strip() != ""]
                else:
                    excluded_values = [pick[len(NEQ_PREFIX):]]

                candidates = [rv for rv in radio_vals if rv not in excluded_values]
                if candidates:
                    chosen = random.choice(candidates)

                if chosen and _ensure_radio_selected(page, name, chosen):
                    logger.info(f"[override] radio(NEQSET): {name} excluded={excluded_values} -> picked={chosen}")
                    handled.add(name)
                else:
                    logger.info(f"[override] radio(NEQSET) not applied: {name} (excluded={excluded_values}, candidates={radio_vals})")
                continue

            if pick in radio_vals:
                chosen = pick
                if _ensure_radio_selected(page, name, chosen):
                    logger.info(f"[override] radio: {name}={chosen}")
                    handled.add(name)
                else:
                    logger.warning(f"[override] radio failed after exact match: {name}={chosen}")
                continue

            fallback_candidates = [rv for rv in radio_vals if rv != pick]
            if fallback_candidates:
                chosen = random.choice(fallback_candidates)

            if chosen and _ensure_radio_selected(page, name, chosen):
                logger.warning(f"[override] radio fallback: {name} requested={pick} missing -> picked={chosen}")
                handled.add(name)
            else:
                logger.warning(f"[override] radio not applied: {name} requested={pick} candidates={radio_vals}")
            continue

        if name in checks:
            if isinstance(val, str):
                picks = [v.strip() for v in val.split(",") if v.strip()]
            elif isinstance(val, (list, tuple, set)):
                picks = [str(x) for x in val]
            else:
                picks = [str(val)]

            falsy = {None, "", "0", "N", "n", "false", "False", "off", "OFF"}
            if (val in falsy) or (isinstance(val, str) and val.strip() in falsy):
                sel_all = f'input[type="checkbox"][name="{name}"]'
                if page.locator(sel_all).count() > 0:
                    set_checked(page, sel_all, False)
                    page.wait_for_timeout(80)
                    logger.info(f"[override] checkbox UNCHECK: {name} (val='{val}')")
                    handled.add(name)
                continue

            applied = False
            for v in picks:
                sel = f'input[type="checkbox"][name="{name}"][value="{v}"]'
                if page.locator(sel).count() > 0:
                    set_checked(page, sel, True)
                    page.wait_for_timeout(80)
                    applied = True
                    continue

                fallback_sel = f'input[type="checkbox"][name="{name}"]'
                if page.locator(fallback_sel).count() > 0:
                    set_checked(page, fallback_sel, True)
                    page.wait_for_timeout(80)
                    logger.warning(f"[override] checkbox fallback: {name} requested value='{v}' missing -> picked first")
                    applied = True
                else:
                    logger.info(f"[override] checkbox not found: {name} (value='{v}')")

            if applied:
                logger.info(f"[override] checkbox: {name} picks={picks}")
                handled.add(name)
            continue

        if name in selects:
            v = str(val)
            chosen: Optional[str] = None

            if v.startswith(NEQ_PREFIX):
                excluded = v[len(NEQ_PREFIX):]
                candidates = _select_usable_options(page, name, excluded=[excluded])
                chosen = random.choice(candidates) if candidates else None
                if chosen is not None:
                    page.evaluate(
                        """([name, value]) => {
                        const el = document.querySelector('select[name="'+name+'"]');
                        if (!el) return;
                        el.value = value;
                        el.dispatchEvent(new Event('change',{bubbles:true}));
                        }""",
                        [name, chosen],
                    )
                    logger.info(f"[override] select(NEQ): {name}!={excluded} -> picked={chosen}")
                    handled.add(name)
                else:
                    logger.info(f"[override] select(NEQ) not found: {name} (excluded={excluded})")
                continue

            exists = _safe_eval(
                page,
                """([name, value]) => {
                const el = document.querySelector('select[name="'+name+'"]');
                if (!el) return false;
                return Array.from(el.options || []).some(o => !o.disabled && String(o.value ?? '') === String(value ?? ''));
                }""",
                [name, v],
                False,
            )

            if exists:
                chosen = v
            else:
                candidates = _select_usable_options(page, name)
                chosen = random.choice(candidates) if candidates else None
            if chosen is not None:
                page.evaluate(
                    """([name, value]) => {
                    const el = document.querySelector('select[name="'+name+'"]');
                    if (!el) return;
                    el.value = value;
                    el.dispatchEvent(new Event('change',{bubbles:true}));
                    }""",
                    [name, chosen],
                )
                if chosen == v:
                    logger.info(f"[override] select: {name}={v}")
                else:
                    logger.warning(f"[override] select fallback: {name} requested={v} missing -> picked={chosen}")
                handled.add(name)
            else:
                logger.info(f"[override] select not applied: {name} requested={v}")
            continue

        if name in inputs_meta:
            v = "" if val is None else str(val)
            set_value(page, f'input[name="{name}"]', v)
            logger.info(f"[override] input: {name}={v}")
            handled.add(name)
            continue

        if name in textareas:
            v = "" if val is None else str(val)
            set_value(page, f'textarea[name="{name}"]', v)
            logger.info(f"[override] textarea: {name}={v}")
            handled.add(name)
            continue

    try:
        for base in list(handled):
            selected_vals = get_selected_values(page, base)
            if selected_vals:
                fill_T_inputs_for_selected(page, meta, base, selected_vals, cfg, logger)
    except Exception:
        pass

    return handled
