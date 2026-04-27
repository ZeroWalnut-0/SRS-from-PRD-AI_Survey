from __future__ import annotations

from typing import Any, Dict, List, Set
import logging

from playwright.sync_api import Page

from .config import RunnerConfig
from .dom_actions import set_value
from .generators import generate_tel_digits, generate_text


_OTHER_KEYWORDS = (
    "기타",
    "other",
    "others",
    "specify",
    "else",
    "직접",
    "주관식",
)


def _normalize_token(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _escape_attr_value(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _build_selector(tag: str, name: str | None = None, iid: str | None = None) -> str:
    if iid:
        return f'{tag}[id="{_escape_attr_value(iid)}"]'
    if name:
        return f'{tag}[name="{_escape_attr_value(name)}"]'
    return tag


def get_selected_values(page: Page, base_name: str) -> Set[str]:
    try:
        vals = page.evaluate(
            """(nm) => {
              const out = new Set();
              Array.from(document.querySelectorAll('input[name="'+nm+'"]'))
                   .filter(e => e.checked)
                   .forEach(e => out.add(String(e.value || '').trim()));
                   
              Array.from(document.querySelectorAll(`input[name^="${nm}_"]`))
                   .filter(e => e.checked && (e.type === "checkbox" || e.type === "radio"))
                   .forEach(e => {
                        out.add(String(e.value || '').trim());
                        const suffix = e.name.slice(nm.length + 1).trim();
                        if (suffix) out.add(suffix);
                   });
              return Array.from(out);
            }""",
            base_name,
        )
        return {_normalize_token(v) for v in (vals or []) if _normalize_token(v)}
    except Exception:
        return set()


def _get_selected_option_details(page: Page, base_name: str) -> List[Dict[str, str]]:
    try:
        rows = page.evaluate(
            r"""(nm) => {
              const pushText = (el) => {
                if (!el) return '';
                return String(el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
              };

              const inps1 = Array.from(document.querySelectorAll('input[name="'+nm+'"]'));
              const inps2 = Array.from(document.querySelectorAll(`input[name^="${nm}_"]`)).filter(e => e.type === "checkbox" || e.type === "radio");
              const els = Array.from(new Set([...inps1, ...inps2]));
              return els
                .filter(e => e.checked)
                .map((el) => {
                  const id = el.id || '';
                  let labelText = '';
                  if (id) {
                    const lb = document.querySelector(`label[for="${id}"]`);
                    if (lb) labelText = pushText(lb);
                  }
                  if (!labelText) {
                    const lb = el.closest('label');
                    if (lb) labelText = pushText(lb);
                  }
                  const wrap = el.closest('li, td, th, tr, .row, .form-group, .question, .q-title, .qtext, .conts, .title, div, span');
                  const wrapText = pushText(wrap);
                  return {
                    value: String(el.value || '').trim(),
                    id: id,
                    label: labelText,
                    context: wrapText,
                  };
                });
            }""",
            base_name,
        )
        out: List[Dict[str, str]] = []
        for row in rows or []:
            out.append(
                {
                    "value": _normalize_token((row or {}).get("value")),
                    "id": _normalize_token((row or {}).get("id")),
                    "label": _normalize_token((row or {}).get("label")),
                    "context": _normalize_token((row or {}).get("context")),
                }
            )
        return out
    except Exception:
        return []


def _extract_field_context(page: Page, selector: str) -> str:
    try:
        return str(
            page.evaluate(
                r"""(sel) => {
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

                  const id = el.getAttribute('id') || '';
                  if (id) {
                    const lb = document.querySelector(`label[for="${id}"]`);
                    if (lb) push(lb.innerText || lb.textContent || '');
                    const td = document.getElementById('TD_' + id);
                    if (td) push(td.innerText || td.textContent || '');
                  }

                  const wrap = el.closest('label, td, th, tr, li, .row, .form-group, .question, .q-title, .qtext, .conts, .title');
                  if (wrap) push(wrap.innerText || wrap.textContent || '');

                  return parts.join(' | ').slice(0, 500);
                }""",
                selector,
            )
            or ""
        )
    except Exception:
        return ""


def _discover_related_other_fields(
    page: Page,
    base_name: str,
    selected_values: Set[str],
) -> List[Dict[str, str]]:
    try:
        rows = page.evaluate(
            """({ baseName, selectedValues }) => {
              const selectedSet = new Set((selectedValues || []).map(v => String(v || '').trim()).filter(Boolean));
              const seen = new Set();
              const out = [];

              const isFillable = (el) => {
                if (!el) return false;
                const tag = (el.tagName || '').toLowerCase();
                if (tag === 'textarea') return !el.disabled;
                if (tag !== 'input') return false;
                const type = String(el.type || 'text').toLowerCase();
                if (['hidden', 'radio', 'checkbox', 'button', 'submit', 'reset', 'file', 'image'].includes(type) && type !== 'text') return false;
                return !el.disabled;
              };

              const alternatePrefix = (baseName.startsWith('V') || baseName.startsWith('H')) ? `T${baseName.slice(1)}_` : '';

              const addEl = (el, reason) => {
                if (!isFillable(el)) return;
                const tag = (el.tagName || '').toLowerCase();
                const name = String(el.getAttribute('name') || '').trim();
                const id = String(el.getAttribute('id') || '').trim();
                if (!name && !id) return;
                if (name === baseName) return;
                const key = `${tag}||${name}||${id}`;
                if (seen.has(key)) return;
                seen.add(key);
                out.push({
                  tag,
                  name,
                  id,
                  type: tag === 'textarea' ? 'textarea' : String(el.type || 'text').toLowerCase(),
                  reason: String(reason || ''),
                });
              };

              const addNearby = (anchor, reason) => {
                if (!anchor) return;
                const scopes = [];
                let node = anchor;
                for (let i = 0; i < 4 && node; i += 1) {
                  scopes.push(node);
                  node = node.parentElement;
                }

                scopes.forEach((scope) => {
                  scope.querySelectorAll('input, textarea').forEach((el) => addEl(el, reason));
                  let sib = scope.nextElementSibling;
                  for (let j = 0; j < 3 && sib; j += 1) {
                    sib.querySelectorAll('input, textarea').forEach((el) => addEl(el, reason));
                    sib = sib.nextElementSibling;
                  }
                });
              };

              document
                .querySelectorAll(`input[name^="T${baseName}_"], textarea[name^="T${baseName}_"]`)
                .forEach((el) => {
                  const nm = String(el.getAttribute('name') || '').trim();
                  const prefix = `T${baseName}_`;
                  if (nm.startsWith(prefix)) {
                    addEl(el, 'prefix-match');
                  } else if (alternatePrefix && nm.startsWith(alternatePrefix)) {
                    addEl(el, 'alt-prefix-match');
                  }
                });

              const inps1 = Array.from(document.querySelectorAll('input[name="'+baseName+'"]'));
              const inps2 = Array.from(document.querySelectorAll(`input[name^="${baseName}_"]`)).filter(e => e.type === "checkbox" || e.type === "radio");
              Array.from(new Set([...inps1, ...inps2]))
                .filter((el) => el.checked)
                .forEach((el) => {
                  const value = String(el.value || '').trim();
                  const suffix = String(el.name || '').slice(baseName.length + 1).trim();
                  if (selectedSet.has(value) || (suffix && selectedSet.has(suffix))) {
                    addNearby(el, 'selected-option-nearby');
                    const label = el.closest('label');
                    if (label) addNearby(label, 'selected-option-label');
                    const row = el.closest('li, td, th, tr, .row, .form-group, .question, .q-title, .qtext, .conts, .title, div, span');
                    if (row) addNearby(row, 'selected-option-row');
                  }
                });

              return out;
            }""",
            {"baseName": base_name, "selectedValues": sorted(selected_values)},
        )
        out: List[Dict[str, str]] = []
        for row in rows or []:
            out.append(
                {
                    "tag": _normalize_token((row or {}).get("tag")) or "input",
                    "name": _normalize_token((row or {}).get("name")),
                    "id": _normalize_token((row or {}).get("id")),
                    "type": _normalize_token((row or {}).get("type")) or "text",
                    "reason": _normalize_token((row or {}).get("reason")),
                }
            )
        return out
    except Exception:
        return []


def _looks_like_other_option(selected_details: List[Dict[str, str]]) -> bool:
    haystack = " ".join(
        f"{row.get('label', '')} {row.get('context', '')}".lower()
        for row in selected_details
    )
    return any(keyword in haystack for keyword in _OTHER_KEYWORDS)


def _iter_target_fields(
    page: Page,
    meta: Dict[str, Any],
    base: str,
    selected_values: Set[str],
    selected_details: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    inputs_meta = meta.get("inputs_meta", {}) or {}
    textareas = set(meta.get("textareas", []) or [])
    
    # Allowed prefixes: primary (T_base) and alternate (T_{base[1:]} if base starts with V/H)
    prefixes = [f"T{base}_"]
    if (base.startswith("V") or base.startswith("H")) and len(base) > 1:
        prefixes.append(f"T{base[1:]}_")

    targets: List[Dict[str, str]] = []
    seen: Set[str] = set()

    def add_target(tag: str, name: str | None, iid: str | None, itype: str, reason: str) -> None:
        key = f"{tag}||{name or ''}||{iid or ''}"
        if key in seen:
            return
        seen.add(key)
        targets.append(
            {
                "tag": tag,
                "name": name or "",
                "id": iid or "",
                "type": (itype or "text").lower(),
                "reason": reason,
            }
        )

    for name, info in inputs_meta.items():
        name_str = str(name)
        matched_prefix = next((p for p in prefixes if name_str.startswith(p)), None)
        if not matched_prefix:
            continue
        suffix = _normalize_token(name_str[len(matched_prefix):])
        if suffix in selected_values:
            add_target("input", name_str, _normalize_token((info or {}).get("id")), (info or {}).get("type") or "text", "meta-prefix-match")

    for ta_name in textareas:
        ta_name_str = str(ta_name)
        matched_prefix = next((p for p in prefixes if ta_name_str.startswith(p)), None)
        if not matched_prefix:
            continue
        suffix = _normalize_token(ta_name_str[len(matched_prefix):])
        if suffix in selected_values:
            add_target("textarea", ta_name_str, None, "textarea", "meta-prefix-match")

    discovered = _discover_related_other_fields(page, base, selected_values)
    allow_nearby = _looks_like_other_option(selected_details)

    for row in discovered:
        row_name = row.get("name") or ""
        row_id = row.get("id") or ""
        row_tag = row.get("tag") or "input"
        row_type = row.get("type") or "text"

        matched_prefix = next((p for p in prefixes if row_name.startswith(p)), None)
        if matched_prefix:
            add_target(row_tag, row_name, row_id, row_type, row.get("reason") or "prefix-discovered")
            continue

        if allow_nearby:
            add_target(row_tag, row_name, row_id, row_type, row.get("reason") or "nearby-other")

    return targets


def _safe_other_text(cfg: RunnerConfig, context_text: str = "", name: str | None = None, iid: str | None = None, multiline: bool = False) -> str:
    base_default = str(getattr(cfg, "other_text_default", "") or "").strip()
    generated = generate_text(
        maxlen=None,
        name=name,
        iid=iid,
        pattern=None,
        context_text=context_text or base_default,
        multiline=multiline,
    )
    candidate = _normalize_token(generated)
    lowered = candidate.lower()
    bad_tokens = {"기타", "other", "etc", "모름", "없음", "해당없음", "직접입력"}
    if (not candidate) or (lowered in bad_tokens) or ("기타" in candidate):
        return "주변인"
    return candidate


def _clear_target_value(page: Page, target: Dict[str, str], logger: logging.Logger | None = None) -> None:
    selector = _build_selector(target.get("tag") or "input", target.get("name"), target.get("id"))
    try:
        set_value(page, selector, "")
        if logger:
            logger.info(f"[OTHER] cleared {target.get('tag')} name={target.get('name','')} id={target.get('id','')} reason={target.get('reason','')}")
    except Exception:
        pass


def sync_other_inputs_for_base(
    page: Page,
    meta: Dict[str, Any],
    base: str,
    cfg: RunnerConfig,
    logger: logging.Logger,
    extra_selected_values: Set[str] | None = None,
) -> List[str]:
    selected_values = {_normalize_token(v) for v in get_selected_values(page, base) if _normalize_token(v)}
    if extra_selected_values:
        selected_values.update({_normalize_token(v) for v in extra_selected_values if _normalize_token(v)})
    selected_details = _get_selected_option_details(page, base)
    targets = _iter_target_fields(page, meta, base, selected_values, selected_details)
    if not targets:
        return []

    changed: List[str] = []
    selected_suffixes = {str(v).strip() for v in selected_values if str(v).strip()}
    prefixes = [f"T{base}_"]
    if (base.startswith("V") or base.startswith("H")) and len(base) > 1:
        prefixes.append(f"T{base[1:]}_")

    for target in targets:
        tag = target.get("tag") or "input"
        name = target.get("name") or ""
        iid = target.get("id") or ""
        reason = target.get("reason") or ""
        selector = _build_selector(tag, name, iid)

        should_fill = True
        matched_prefix = next((p for p in prefixes if name.startswith(p)), None)
        if matched_prefix:
            suffix = _normalize_token(name[len(matched_prefix):])
            if suffix:
                should_fill = suffix in selected_suffixes
        elif reason == "nearby-other" and name:
            import re
            m = re.search(r'_(\d+)$', name)
            if m:
                suffix = m.group(1)
                if suffix not in selected_suffixes:
                    should_fill = False

        if not should_fill:
            _clear_target_value(page, target, logger)
            continue

        context_text = _extract_field_context(page, selector)
        itype = (target.get("type") or "text").lower()
        if itype == "tel":
            v = generate_tel_digits(None, None, name=name, iid=iid)
        else:
            v = _safe_other_text(cfg, context_text=context_text, name=name, iid=iid, multiline=(tag == "textarea"))

        try:
            ok = set_value(page, selector, v)
            if ok:
                changed.append(name or iid or selector)
                logger.info(f"[OTHER] synced {tag} name={name} id={iid} reason={reason} value={v}")
        except Exception as exc:
            logger.warning(f"[OTHER] failed to sync {tag} name={name} id={iid} selector={selector}: {exc}")

    return changed


def fill_T_inputs_for_selected(
    page: Page,
    meta: Dict[str, Any],
    base: str,
    selected_values: Set[str],
    cfg: RunnerConfig,
    logger: logging.Logger,
):
    try:
        sync_other_inputs_for_base(page, meta, base, cfg, logger, extra_selected_values=selected_values)
    except Exception as exc:
        logger.warning(f"[OTHER] sync failed for base={base}: {exc}")
