from __future__ import annotations
from typing import Any, Dict, List
from bs4 import BeautifulSoup


def parse_form_fields(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")
    form = soup.find("form")
    if not form:
        return {"has_form": False}

    form_action = (form.get("action") or "").strip()

    hidden: Dict[str, str] = {}
    radios: Dict[str, List[str]] = {}
    checks: Dict[str, List[str]] = {}
    selects: Dict[str, List[str]] = {}
    textareas: List[str] = []
    canvases: List[str] = []
    inputs_meta: Dict[str, Dict[str, Any]] = {}

    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        itype = (inp.get("type") or "text").lower()
        val = inp.get("value") or ""

        maxlength = inp.get("maxlength")
        try:
            maxlength_int = int(maxlength) if maxlength is not None and str(maxlength).isdigit() else None
        except Exception:
            maxlength_int = None

        pattern = inp.get("pattern")
        iid = inp.get("id")
        hmin = inp.get("min")
        hmax = inp.get("max")
        required = inp.has_attr("required") or inp.get("aria-required") == "true"
        placeholder = inp.get("placeholder") or ""
        title = inp.get("title") or ""
        aria_label = inp.get("aria-label") or ""

        def _attr_to_int(v):
            try:
                return int(float(v)) if v is not None and str(v).strip() != "" else None
            except:
                return None

        inputs_meta[name] = {
            "type": itype,
            "maxlength": maxlength_int,
            "pattern": pattern,
            "id": iid,
            "min": _attr_to_int(hmin),
            "max": _attr_to_int(hmax),
            "required": required,
            "placeholder": placeholder,
            "title": title,
            "aria_label": aria_label,
            "disabled": inp.has_attr("disabled"),
            "readonly": inp.has_attr("readonly"),
        }

        if itype == "hidden":
            hidden[name] = val
        elif itype == "radio":
            radios.setdefault(name, [])
            if val not in radios[name]:
                radios[name].append(val)
        elif itype == "checkbox":
            checks.setdefault(name, [])
            if val not in checks[name]:
                checks[name].append(val)

    for sel in form.find_all("select"):
        name = sel.get("name")
        if not name:
            continue
        vals = []
        for opt in sel.find_all("option"):
            v = opt.get("value")
            if v is None:
                continue
            vals.append(v)
        selects[name] = vals
        inputs_meta.setdefault(name, {
            "type": "select",
            "maxlength": None,
            "pattern": None,
            "id": sel.get("id"),
            "disabled": sel.has_attr("disabled"),
            "readonly": False,
        })

    for ta in form.find_all("textarea"):
        name = ta.get("name")
        if name:
            textareas.append(name)
            inputs_meta.setdefault(name, {
                "type": "textarea",
                "maxlength": ta.get("maxlength"),
                "pattern": None,
                "id": ta.get("id"),
                "disabled": ta.has_attr("disabled"),
                "readonly": ta.has_attr("readonly"),
            })
    
    for cv in form.find_all("canvas"):
        cid = cv.get("id")
        if cid:
            canvases.append(cid)
        else:
            canvases.append("canvas_unnamed")

    return {
        "has_form": True,
        "form_action": form_action,
        "hidden": hidden,
        "radios": radios,
        "checks": checks,
        "selects": selects,
        "textareas": textareas,
        "canvases": canvases,
        "inputs_meta": inputs_meta,
    }
