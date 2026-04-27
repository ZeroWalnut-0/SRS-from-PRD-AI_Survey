from __future__ import annotations

import logging
import random
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from playwright.sync_api import Page

from .dom_actions import click_with_td_fallback, set_checked, set_value
from .generators import generate_email, generate_text, generate_tel_digits
from .other_fill import sync_other_inputs_for_base


# ============================================================
# JS parsing helpers
# ============================================================

def _norm_js_space(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _strip_js_comments(src: str) -> str:
    if not src:
        return ""
    try:
        src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
        src = re.sub(r"(^|[^:])//.*?$", r"\1", src, flags=re.M)
    except Exception:
        pass
    return src





def _clean_field_name(name: str) -> str:
    s = (name or '').strip()
    if not s:
        return ''
    s = re.sub(r"^\$\([\"']#?([^\"']+)[\"']\)\.val\(\)$", r"\1", s)
    s = re.sub(r"^document\.getElementById\([\"']([^\"']+)[\"']\)\.value$", r"\1", s)
    s = re.sub(r"^document\.querySelector\([\"']#([^\"']+)[\"']\)\.value$", r"\1", s)
    s = re.sub(r"^[\"']|[\"']$", "", s)
    s = re.sub(r"^#", "", s)
    m = re.match(r"^\[name=[\"']?([^\"']+)[\"']?\]$", s)
    if m:
        s = m.group(1)
    m = re.match(r"^input\[name=[\"']?([^\"']+)[\"']?\]$", s, flags=re.I)
    if m:
        s = m.group(1)
    s = re.sub(r"\.val\(\)$", "", s)
    s = re.sub(r"\.trim\(\)$", "", s)
    s = re.sub(r"^parse(?:Int|Float)\((.*)\)$", r"\1", s)
    return s.strip()

def _skip_ws(src: str, i: int) -> int:
    n = len(src)
    while i < n and src[i].isspace():
        i += 1
    return i


def _read_balanced(src: str, i: int, open_ch: str, close_ch: str) -> tuple[str, int]:
    if i >= len(src) or src[i] != open_ch:
        return "", i
    depth = 0
    start = i + 1
    j = i
    in_str: str | None = None
    esc = False
    while j < len(src):
        ch = src[j]
        if in_str is not None:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == in_str:
                in_str = None
            j += 1
            continue
        if ch in ('"', "'", '`'):
            in_str = ch
            j += 1
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return src[start:j], j + 1
        j += 1
    return src[start:], len(src)


def _read_to_semicolon(src: str, i: int) -> tuple[str, int]:
    """
    JS statement reader with light ASI support.
    - 기본은 세미콜론(;)까지 읽는다.
    - 다만 top-level에서 줄바꿈을 만나면 statement 끝으로 본다.
      (예: `var YEAR` / `YEAR = $("#DQ1").val()` 같은 ASI 스타일 대응)
    """
    n = len(src)
    start = i
    p = b = c = 0
    in_str: str | None = None
    esc = False
    while i < n:
        ch = src[i]
        if in_str is not None:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ('"', "'", '`'):
            in_str = ch
            i += 1
            continue
        if ch == '(':
            p += 1
        elif ch == ')':
            p = max(0, p - 1)
        elif ch == '[':
            b += 1
        elif ch == ']':
            b = max(0, b - 1)
        elif ch == '{':
            c += 1
        elif ch == '}':
            if c == 0 and p == 0 and b == 0:
                break
            c = max(0, c - 1)
        elif ch == ';' and p == 0 and b == 0 and c == 0:
            return src[start:i], i + 1
        elif ch in ('\n', '\r') and p == 0 and b == 0 and c == 0:
            return src[start:i], i + 1
        i += 1
    return src[start:i], i


def _parse_js_stmt(src: str, i: int) -> tuple[dict[str, Any] | None, int]:
    i = _skip_ws(src, i)
    n = len(src)
    if i >= n:
        return None, i

    if src[i] == '{':
        body, j = _read_balanced(src, i, '{', '}')
        return {"type": "block", "body": _parse_js_block(body)}, j

    if re.match(r'if\b', src[i:], flags=re.I):
        j = i + 2
        j = _skip_ws(src, j)
        if j >= n or src[j] != '(':
            expr, k = _read_to_semicolon(src, i)
            return {"type": "expr", "code": expr.strip()}, k
        cond, j = _read_balanced(src, j, '(', ')')
        cons, j = _parse_js_stmt(src, j)
        j = _skip_ws(src, j)
        alt = None
        if re.match(r'else\b', src[j:], flags=re.I):
            j += 4
            alt, j = _parse_js_stmt(src, j)
        return {"type": "if", "cond": cond.strip(), "then": cons, "else": alt}, j

    if re.match(r'(?:return)\b', src[i:], flags=re.I):
        expr, j = _read_to_semicolon(src, i)
        return {"type": "return", "code": expr.strip()}, j

    if re.match(r'(?:var|let|const)\b', src[i:], flags=re.I):
        expr, j = _read_to_semicolon(src, i)
        return {"type": "decl", "code": expr.strip()}, j

    expr, j = _read_to_semicolon(src, i)
    code = expr.strip()
    low = code.lower()
    if low.startswith('alert(') or low.startswith('confirm('):
        return {"type": "alert", "code": code}, j
    return {"type": "expr", "code": code}, j


def _parse_js_block(src: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    i = 0
    n = len(src)
    while i < n:
        i = _skip_ws(src, i)
        if i >= n:
            break
        if src[i] == ';':
            i += 1
            continue
        stmt, j = _parse_js_stmt(src, i)
        if stmt:
            out.append(stmt)
        i = max(j, i + 1)
    return out


def _contains_return_stmt(node: dict[str, Any] | None) -> bool:
    if not node:
        return False
    typ = node.get('type')
    if typ == 'return':
        return True
    if typ == 'block':
        return any(_contains_return_stmt(x) for x in (node.get('body') or []))
    if typ == 'if':
        return _contains_return_stmt(node.get('then')) or _contains_return_stmt(node.get('else'))
    return False



def _split_top_level(expr: str, op: str) -> list[str]:
    s = _norm_js_space(expr)
    if not s:
        return []
    parts: list[str] = []
    cur: list[str] = []
    p = b = cdepth = 0
    in_str: str | None = None
    esc = False
    i = 0
    oplen = len(op)
    while i < len(s):
        ch = s[i]
        if in_str is not None:
            cur.append(ch)
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ('"', "'", '`'):
            in_str = ch
            cur.append(ch)
            i += 1
            continue
        if ch == '(':
            p += 1
        elif ch == ')':
            p = max(0, p - 1)
        elif ch == '[':
            b += 1
        elif ch == ']':
            b = max(0, b - 1)
        elif ch == '{':
            cdepth += 1
        elif ch == '}':
            cdepth = max(0, cdepth - 1)
        if p == 0 and b == 0 and cdepth == 0 and s[i:i+oplen] == op:
            token = _norm_js_space(''.join(cur))
            if token:
                parts.append(token)
            cur = []
            i += oplen
            continue
        cur.append(ch)
        i += 1
    token = _norm_js_space(''.join(cur))
    if token:
        parts.append(token)
    return parts


def _flatten_guard_atoms(cond: str) -> list[str]:
    c = _norm_js_space(cond)
    if not c:
        return []
    and_parts = _split_top_level(c, '&&') or [c]
    atoms: list[str] = []
    for part in and_parts:
        or_parts = [_norm_js_space(x) for x in (_split_top_level(part, '||') or []) if _norm_js_space(x)]
        if or_parts and all(x.startswith('!') for x in or_parts):
            atoms.extend(or_parts)
        else:
            atoms.append(_norm_js_space(part))
    return [x for x in atoms if x]


def _collect_validation_condition_paths_from_ast(src: str) -> list[list[str]]:
    text = _strip_js_comments(src)
    try:
        ast = _parse_js_block(text)
    except Exception:
        return []

    paths: list[list[str]] = []

    def walk_block(stmts: list[dict[str, Any]], guards: list[str]) -> None:
        for stmt in stmts or []:
            typ = stmt.get('type')
            if typ == 'return':
                if guards:
                    paths.append(list(guards))
                continue
            if typ == 'if':
                cond = _norm_js_space(stmt.get('cond') or '')
                atoms = _flatten_guard_atoms(cond) if cond else []
                then_node = stmt.get('then')
                else_node = stmt.get('else')
                if then_node:
                    if then_node.get('type') == 'block':
                        walk_block(list(then_node.get('body') or []), guards + atoms)
                    elif then_node.get('type') == 'return':
                        if guards or atoms:
                            paths.append(list(guards + atoms))
                    elif then_node.get('type') == 'if':
                        walk_block([then_node], guards + atoms)
                if else_node and _contains_return_stmt(else_node):
                    neg = f'!({cond})' if cond else '!__COND__'
                    if else_node.get('type') == 'block':
                        walk_block(list(else_node.get('body') or []), guards + [neg])
                    elif else_node.get('type') == 'return':
                        paths.append(list(guards + [neg]))
                    elif else_node.get('type') == 'if':
                        walk_block([else_node], guards + [neg])
                continue
            if typ == 'block':
                walk_block(list(stmt.get('body') or []), guards)

    walk_block(ast, [])

    uniq: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    for p in paths:
        cleaned = tuple(x for x in (_norm_js_space(v) for v in p) if x)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            uniq.append(list(cleaned))
    return uniq


def _find_if_conditions_with_return(src: str) -> List[str]:
    out: List[str] = []
    if not src:
        return out

    try:
        for path in _collect_validation_condition_paths_from_ast(src):
            joined = " && ".join([_norm_js_space(x) for x in path if _norm_js_space(x)])
            if joined:
                out.append(joined)
    except Exception:
        pass

    text = _strip_js_comments(src)
    for m in re.finditer(r"if\s*\((.*?)\)\s*return\s*;", text, flags=re.I | re.S):
        cond = (m.group(1) or "").strip()
        if cond:
            out.append(cond)
    for m in re.finditer(r"if\s*\((.*?)\)\s*\{(.*?)\}", text, flags=re.I | re.S):
        cond = (m.group(1) or "").strip()
        body = m.group(2) or ""
        if cond and re.search(r"return", body):
            out.append(cond)

    uniq: List[str] = []
    seen: Set[str] = set()
    for c in out:
        c2 = _norm_js_space(c)
        if not c2 or c2 in seen:
            continue
        seen.add(c2)
        uniq.append(c2)
    return uniq

def _extract_var_to_field_map(src: str) -> Dict[str, str]:
    text = _strip_js_comments(src)
    out: Dict[str, str] = {}

    field_expr_patterns = [
        r'\$\("#([^"\\]+)"\)\.val\(\)(?:\.trim\(\))?',
        r'document\.getElementById\("([^"\\]+)"\)\.value(?:\.trim\(\))?',
        r"document\.querySelector\(\s*['\"]\[name=['\"]([^'\"\\]+)['\"]\]['\"]\s*\)\.value(?:\.trim\(\))?",
        r"document\.querySelector\(\s*['\"]#([^'\"\\]+)['\"]\s*\)\.value(?:\.trim\(\))?",
        r'document\.getElementsByName\("([^"\\]+)"\)\s*\[\s*\d+\s*\]\.value(?:\.trim\(\))?',
    ]

    wrappers = [
        r'(?P<expr>{FIELD})',
        r'(?:parseInt|parseFloat|Number)\(\s*(?P<expr>{FIELD})\s*(?:,\s*10\s*)?\)',
        r'\(\s*(?:parseInt|parseFloat|Number)\(\s*(?P<expr>{FIELD})\s*(?:,\s*10\s*)?\)\s*\)',
    ]

    trailing = r'(?:\s*\|\|\s*-?\d+(?:\.\d+)?)?\s*;'

    for fpat in field_expr_patterns:
        for wpat in wrappers:
            expr_pat = wpat.replace('{FIELD}', fpat)
            for prefix in (r'(?:const|let|var)\s+', r''):
                pat = rf'{prefix}([A-Za-z_]\w*)\s*=\s*{expr_pat}{trailing}'
                for m in re.finditer(pat, text, flags=re.I | re.S):
                    field_name = next((g for g in m.groups()[1:] if g), None)
                    if field_name:
                        out[m.group(1)] = _clean_field_name(field_name)

    # alias chain: X = Y;  / var X = Y;
    for _ in range(5):
        changed = False
        for m in re.finditer(r'(?:const|let|var)?\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*;', text, flags=re.I):
            lhs = m.group(1)
            rhs = m.group(2)
            if rhs in out and out.get(lhs) != out[rhs]:
                out[lhs] = out[rhs]
                changed = True
        if not changed:
            break

    return out


def _now_year() -> int:
    return datetime.now().year


def _extract_scalar_vars(src: str) -> Dict[str, int]:
    text = _strip_js_comments(src)
    out: Dict[str, int] = {}
    cy = _now_year()

    # const X = 123;
    for m in re.finditer(r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*(-?\d+)\s*;', text, flags=re.I):
        out.setdefault(m.group(1), int(m.group(2)))

    # const X = (new Date()).getFullYear() - 25;
    for m in re.finditer(
        r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*[\(\s]*(?:new\s+Date\(\)|[A-Za-z_]\w*)\.getFullYear\(\)\s*[\)]*\s*([+\-])\s*(\d+)\s*;',
        text,
        flags=re.I,
    ):
        nm, op, raw = m.group(1), m.group(2), int(m.group(3))
        out[nm] = cy + raw if op == "+" else cy - raw

    # const X = Y + 1;
    for _ in range(5):
        changed = False
        for m in re.finditer(r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*([+\-])\s*(\d+)\s*;', text, flags=re.I):
            lhs, rhs, op, raw = m.group(1), m.group(2), m.group(3), int(m.group(4))
            if rhs in out:
                val = out[rhs] + raw if op == "+" else out[rhs] - raw
                if out.get(lhs) != val:
                    out[lhs] = val
                    changed = True
        if not changed:
            break

    return out


def _resolve_num_expr(expr: str, scalar_vars: Dict[str, int]) -> Optional[int]:
    s = _norm_js_space(expr)
    if not s:
        return None

    if re.fullmatch(r'-?\d+', s):
        return int(s)

    if s in scalar_vars:
        return scalar_vars[s]

    m = re.fullmatch(r'"(-?\d+)(?:\.0+)?"|\'(-?\d+)(?:\.0+)?\'', s)
    if m:
        raw = m.group(1) or m.group(2)
        return int(float(raw))

    m = re.fullmatch(r'(?:parseInt|parseFloat|Number)\(\s*["\']?(-?\d+)(?:\.0+)?["\']?\s*\)', s, flags=re.I)
    if m:
        return int(float(m.group(1)))

    # X + 1 / X - 1
    m = re.fullmatch(r'([A-Za-z_]\w*)\s*([+\-])\s*(\d+)', s)
    if m and m.group(1) in scalar_vars:
        base = scalar_vars[m.group(1)]
        raw = int(m.group(3))
        return base + raw if m.group(2) == "+" else base - raw

    return None


def _extract_regex_vars(src: str) -> Dict[str, str]:
    text = _strip_js_comments(src)
    out: Dict[str, str] = {}

    for m in re.finditer(r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*/(.+?)/([gimuy]*)\s*;', text, flags=re.I | re.S):
        out[m.group(1)] = m.group(2)

    # new RegExp("..."), new RegExp('...')
    for m in re.finditer(r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*new\s+RegExp\(\s*["\'](.+?)["\']\s*(?:,\s*["\']([gimuy]*)["\'])?\s*\)\s*;', text, flags=re.I | re.S):
        out[m.group(1)] = m.group(2)

    return out


def _extract_field_compare_disjunctions(
    cond: str,
    resolve_field,
    scalar_vars: Dict[str, int],
) -> List[Dict[str, str]]:
    s = _norm_js_space(cond)
    if not s or '||' not in s:
        return []

    parts = [_norm_js_space(x) for x in (_split_top_level(s, '||') or []) if _norm_js_space(x)]
    if len(parts) < 2:
        return []

    field_cmp_patterns = [
        (
            rf'^(?:parseInt|parseFloat|Number)\(\s*{_field_token_regex()}\s*,?\s*(?:10)?\s*\)\s*(<=|>=|<|>)\s*(?:parseInt|parseFloat|Number)\(\s*{_field_token_regex()}\s*,?\s*(?:10)?\s*\)\s*$',
            'numeric',
        ),
        (rf'^{_field_token_regex()}\s*(<=|>=|<|>)\s*{_field_token_regex()}\s*$', 'plain'),
    ]

    rels: List[Dict[str, str]] = []
    seen: Set[Tuple[str, str, str]] = set()

    def first_field(groups, start, count=5):
        for g in groups[start:start + count]:
            if g:
                return g
        return None

    invert = {'>': '<=', '>=': '<', '<': '>=', '<=': '>'}

    for part in parts:
        matched = False
        for pat, kind in field_cmp_patterns:
            m = re.match(pat, part, flags=re.I)
            if not m:
                continue
            groups = m.groups()
            if kind == 'numeric':
                left_tok = first_field(groups, 0)
                op = groups[5]
                right_tok = first_field(groups, 6)
            else:
                left_tok = first_field(groups, 0)
                op = groups[5]
                right_tok = first_field(groups, 6)
            left = resolve_field(left_tok) if left_tok else ''
            right = resolve_field(right_tok) if right_tok else ''
            valid_op = invert.get(op)
            if left and right and valid_op:
                key = (left, valid_op, right)
                if key not in seen:
                    seen.add(key)
                    rels.append({'left': left, 'op': valid_op, 'right': right, 'kind': 'numeric'})
            matched = True
            break
        if matched:
            continue

        # mixed compare like: A < B || A > LIMIT  -> ignore here; numeric limit parsing handles it later
        # variable aliases that resolve to fields are already covered by _field_token_regex() and resolve_field.

    return rels


def extract_next_source(page: Page) -> str:
    try:
        src = page.evaluate(
            """() => {
                try {
                    if (typeof window.next === "function") return window.next.toString();
                } catch (e) {}
                return "";
            }"""
        )
        return src or ""
    except Exception:
        return ""


# ============================================================
# Constraint extraction
# ============================================================

def _mark_invalid_numeric_compare(out: Dict[str, Any], field_name: str, op: str, value: int) -> None:
    out["numeric"].setdefault(field_name, {})
    slot = out["numeric"][field_name]
    if op == ">=":
        slot["max"] = min(slot.get("max", value - 1), value - 1) if "max" in slot else value - 1
    elif op == ">":
        slot["max"] = min(slot.get("max", value), value) if "max" in slot else value
    elif op == "<=":
        slot["min"] = max(slot.get("min", value + 1), value + 1) if "min" in slot else value + 1
    elif op == "<":
        slot["min"] = max(slot.get("min", value), value) if "min" in slot else value


def _add_length_min(out: Dict[str, Any], name: str, value: int) -> None:
    cur = out["length_min"].get(name)
    out["length_min"][name] = value if cur is None else max(cur, value)


def _add_length_max(out: Dict[str, Any], name: str, value: int) -> None:
    cur = out["length_max"].get(name)
    out["length_max"][name] = value if cur is None else min(cur, value)


def _field_token_regex() -> str:
    return r'(?:\$\("#([^"\\]+)"\)\.val\(\)(?:\.trim\(\))?|document\.getElementById\("([^"\\]+)"\)\.value(?:\.trim\(\))?|document\.querySelector\(\s*[\'"]#([^\'"\\]+)[\'"]\s*\)\.value(?:\.trim\(\))?|document\.querySelector\(\s*[\'"]\[name=[\'"]([^\'"\\]+)[\'"]\][\'"]\s*\)\.value(?:\.trim\(\))?|([A-Za-z_]\w*)(?:\.trim\(\))?)'



def extract_next_constraints(page: Page) -> Dict[str, Any]:
    src = extract_next_source(page)
    out: Dict[str, Any] = {
        "source": src,
        "required": set(),
        "numeric_only": set(),
        "length_min": {},
        "length_max": {},
        "numeric": {},
        "regex": {},
        "relations": [],
    }
    if not src:
        return out

    conds = _find_if_conditions_with_return(src)
    var_to_field = _extract_var_to_field_map(src)
    scalar_vars = _extract_scalar_vars(src)
    regex_vars = _extract_regex_vars(src)

    existing_field_cache: Dict[str, bool] = {}

    def _field_exists_in_dom(name: str) -> bool:
        nm = _clean_field_name(name)
        if not nm:
            return False
        if nm in existing_field_cache:
            return existing_field_cache[nm]
        ok = False
        try:
            ok = bool(page.evaluate(
                """(nm) => !!(document.querySelector(`[name=\"${nm}\"]`) || document.getElementById(nm))""",
                nm,
            ))
        except Exception:
            ok = False
        existing_field_cache[nm] = ok
        return ok

    def resolve_field(tok: str) -> str:
        raw = str(tok or '').strip()
        if not raw:
            return ''
        key = _clean_field_name(raw)
        mapped = _clean_field_name(var_to_field.get(key, var_to_field.get(raw, '')))
        if mapped:
            return mapped
        if raw != key:
            return key
        return key if _field_exists_in_dom(key) else ''

    FT = _field_token_regex()
    num_call = rf'(?:parseInt|parseFloat|Number)\(\s*{FT}\s*(?:,\s*10\s*)?\)'

    def _first_field(groups, start, count=5):
        return next((g for g in groups[start:start+count] if g), None)

    for cond in conds:
        raw_cond = _norm_js_space(cond)

        for rel in _extract_field_compare_disjunctions(raw_cond, resolve_field, scalar_vars):
            out["relations"].append(rel)

        atoms = _flatten_guard_atoms(raw_cond) or [raw_cond]

        for c in atoms:
            c = _norm_js_space(c)
            if not c:
                continue

            required_patterns = [
                rf'^!\s*{FT}\s*$',
                rf"^{FT}\s*([=!]==?)\s*[\"']\s*[\"']\s*$",
                rf"^String\(\s*{FT}\s*\)\s*([=!]==?)\s*[\"']\s*[\"']\s*$",
            ]
            hit_required = False
            for pat in required_patterns:
                m = re.match(pat, c, flags=re.I)
                if not m:
                    continue
                token = _first_field(m.groups(), 0)
                if not token:
                    continue
                nm = resolve_field(token)
                if nm:
                    out["required"].add(nm)
                    hit_required = True
                break
            if hit_required:
                continue

            numeric_only_patterns = [
                rf'^!\s*isNaN\(\s*{FT}\s*\)\s*==\s*false\s*$',
                rf'^isNaN\(\s*{FT}\s*\)\s*$',
                rf'^isNaN\(\s*{FT}\s*\)\s*==\s*true\s*$',
            ]
            hit_numeric_only = False
            for pat in numeric_only_patterns:
                m = re.match(pat, c, flags=re.I)
                if not m:
                    continue
                token = _first_field(m.groups(), 0)
                if not token:
                    continue
                nm = resolve_field(token)
                if nm:
                    out["numeric_only"].add(nm)
                    hit_numeric_only = True
                break
            if hit_numeric_only:
                continue

            m = re.match(rf'^!\s*([A-Za-z_]\w*)\.test\(\s*{FT}\s*\)\s*$', c, flags=re.I)
            if m:
                rv = m.group(1)
                token = _first_field(m.groups(), 1)
                nm = resolve_field(token) if token else ""
                if nm and rv in regex_vars:
                    out["regex"][nm] = regex_vars[rv]
                continue

            m = re.match(rf'^!\s*/(.+?)/[gimuy]*\.test\(\s*{FT}\s*\)\s*$', c, flags=re.I)
            if m:
                pat_body = m.group(1)
                token = _first_field(m.groups(), 1)
                nm = resolve_field(token) if token else ""
                if nm and pat_body:
                    out["regex"][nm] = pat_body
                continue

            m = re.match(rf'^(?:String\()?(?:{FT})\)?\.length\s*<\s*(\d+)\s*$', c, flags=re.I)
            if m:
                token = _first_field(m.groups(), 0)
                if token:
                    nm = resolve_field(token)
                    if nm:
                        _add_length_min(out, nm, int(m.groups()[-1]))
                continue

            m = re.match(rf'^(?:String\()?(?:{FT})\)?\.length\s*>\s*(\d+)\s*$', c, flags=re.I)
            if m:
                token = _first_field(m.groups(), 0)
                if token:
                    nm = resolve_field(token)
                    if nm:
                        _add_length_max(out, nm, int(m.groups()[-1]))
                continue

            # OR range must be handled before single-compare parsing
            m = re.match(rf'^{num_call}\s*(<|<=)\s*(.+?)\s*\|\|\s*{num_call}\s*(>|>=)\s*(.+?)\s*$', c, flags=re.I)
            if m:
                groups = m.groups()
                token_left = _first_field(groups, 0)
                left_op = groups[5]
                low_expr = groups[6]
                token_right = _first_field(groups, 7)
                right_op = groups[12]
                high_expr = groups[13]
                nm_left = resolve_field(token_left) if token_left else ""
                nm_right = resolve_field(token_right) if token_right else ""
                if nm_left and nm_left == nm_right:
                    low = _resolve_num_expr(low_expr, scalar_vars)
                    high = _resolve_num_expr(high_expr, scalar_vars)
                    if low is not None:
                        _mark_invalid_numeric_compare(out, nm_left, left_op, low)
                    if high is not None:
                        _mark_invalid_numeric_compare(out, nm_left, right_op, high)
                continue

            m = re.match(rf'^{FT}\s*(<|<=)\s*(.+?)\s*\|\|\s*{FT}\s*(>|>=)\s*(.+?)\s*$', c, flags=re.I)
            if m:
                groups = m.groups()
                token_left = _first_field(groups, 0)
                left_op = groups[5]
                low_expr = groups[6]
                token_right = _first_field(groups, 7)
                right_op = groups[12]
                high_expr = groups[13]
                nm_left = resolve_field(token_left) if token_left else ""
                nm_right = resolve_field(token_right) if token_right else ""
                if nm_left and nm_left == nm_right:
                    low = _resolve_num_expr(low_expr, scalar_vars)
                    high = _resolve_num_expr(high_expr, scalar_vars)
                    if low is not None:
                        _mark_invalid_numeric_compare(out, nm_left, left_op, low)
                    if high is not None:
                        _mark_invalid_numeric_compare(out, nm_left, right_op, high)
                continue

            # field-to-field compare -> invert invalid condition to valid relation
            m = re.match(rf'^{num_call}\s*(<=|>=|<|>)\s*{num_call}\s*$', c, flags=re.I)
            if m:
                groups = m.groups()
                token_left = _first_field(groups, 0)
                op = groups[5]
                token_right = _first_field(groups, 6)
                nm_left = resolve_field(token_left) if token_left else ""
                nm_right = resolve_field(token_right) if token_right else ""
                valid_op = {'>': '<=', '>=': '<', '<': '>=', '<=': '>'}.get(op)
                if nm_left and nm_right and valid_op:
                    out["relations"].append({"left": nm_left, "op": valid_op, "right": nm_right, "kind": "numeric"})
                continue

            m = re.match(rf'^{FT}\s*(<=|>=|<|>)\s*{FT}\s*$', c, flags=re.I)
            if m:
                groups = m.groups()
                token_left = _first_field(groups, 0)
                op = groups[5]
                token_right = _first_field(groups, 6)
                nm_left = resolve_field(token_left) if token_left else ""
                nm_right = resolve_field(token_right) if token_right else ""
                valid_op = {'>': '<=', '>=': '<', '<': '>=', '<=': '>'}.get(op)
                if nm_left and nm_right and valid_op:
                    out["relations"].append({"left": nm_left, "op": valid_op, "right": nm_right, "kind": "numeric"})
                continue

            # numeric single compare
            m = re.match(rf'^{num_call}\s*(<=|>=|<|>)\s*(.+?)\s*$', c, flags=re.I)
            if m:
                groups = m.groups()
                token = _first_field(groups, 0)
                op = groups[5]
                rhs = groups[6]
                nm = resolve_field(token) if token else ""
                num = _resolve_num_expr(rhs, scalar_vars)
                if nm and num is not None:
                    _mark_invalid_numeric_compare(out, nm, op, num)
                continue

            m = re.match(rf'^{FT}\s*(<=|>=|<|>)\s*(.+?)\s*$', c, flags=re.I)
            if m:
                groups = m.groups()
                token = _first_field(groups, 0)
                op = groups[5]
                rhs = groups[6]
                nm = resolve_field(token) if token else ""
                num = _resolve_num_expr(rhs, scalar_vars)
                if nm and num is not None:
                    _mark_invalid_numeric_compare(out, nm, op, num)
                continue

    # direct fallback parsing for numeric input guards like:
    # if (parseInt($("#C2_4").val().trim(),10) > 1000) { ... return; }
    direct_numeric_patterns = [
        rf'^(?:parseInt|parseFloat|Number)\(\s*{FT}\s*(?:,\s*10\s*)?\)\s*(<|<=|>|>=)\s*(-?\d+(?:\.\d+)?)\s*$',
        rf'^{FT}\s*(<|<=|>|>=)\s*(-?\d+(?:\.\d+)?)\s*$',
        rf'^(?:parseInt|parseFloat|Number)\(\s*(-?\d+(?:\.\d+)?)\s*(?:,\s*10\s*)?\)\s*(<|<=|>|>=)\s*{FT}\s*$',
        rf'^(-?\d+(?:\.\d+)?)\s*(<|<=|>|>=)\s*(?:parseInt|parseFloat|Number)\(\s*{FT}\s*(?:,\s*10\s*)?\)\s*$',
    ]

    for cond in conds:
        for atom in (_flatten_guard_atoms(_norm_js_space(cond)) or [_norm_js_space(cond)]):
            c = _norm_js_space(atom)
            if not c or '||' in c:
                continue
            matched_direct = False
            for pat in direct_numeric_patterns[:2]:
                m = re.match(pat, c, flags=re.I)
                if not m:
                    continue
                token = _first_field(m.groups(), 0)
                op = m.groups()[5]
                raw_num = m.groups()[6]
                nm = resolve_field(token) if token else ''
                num = _safe_int(raw_num)
                if nm and num is not None:
                    _mark_invalid_numeric_compare(out, nm, op, num)
                matched_direct = True
                break
            if matched_direct:
                continue
            for pat in direct_numeric_patterns[2:]:
                m = re.match(pat, c, flags=re.I)
                if not m:
                    continue
                raw_num = m.groups()[0]
                op = m.groups()[1]
                token = _first_field(m.groups(), 2)
                nm = resolve_field(token) if token else ''
                num = _safe_int(raw_num)
                invert = {'>':'<','>=':'<=','<':'>','<=':'>='}
                if nm and num is not None and op in invert:
                    _mark_invalid_numeric_compare(out, nm, invert[op], num)
                break

    uniq_rel = []
    seen_rel = set()
    for rel in out["relations"]:
        key = (_clean_field_name(rel.get("left")), str(rel.get("op") or ""), _clean_field_name(rel.get("right")))
        if key in seen_rel:
            continue
        seen_rel.add(key)
        uniq_rel.append(rel)
    out["relations"] = uniq_rel
    return out


# ============================================================
# DOM helpers / combine with ASP guards
# ============================================================

def _is_empty_value(v: Any) -> bool:
    return v is None or str(v).strip() == ""


def _get_current_values(page: Page) -> Dict[str, str]:
    try:
        return page.evaluate(
            """() => {
                const out = {};
                const els = Array.from(document.querySelectorAll("input[name], select[name], textarea[name]"));
                for (const el of els) {
                    const nm = el.name;
                    if (!nm) continue;
                    const type = (el.getAttribute("type") || "").toLowerCase();
                    if (type === "radio") {
                        const checked = document.querySelector(`input[type="radio"][name="${nm}"]:checked`);
                        out[nm] = checked ? (checked.value || "") : "";
                        continue;
                    }
                    if (type === "checkbox") {
                        const checked = Array.from(document.querySelectorAll(`input[type="checkbox"][name="${nm}"]:checked`)).map(x => x.value || "");
                        out[nm] = checked.join(",");
                        continue;
                    }
                    out[nm] = el.value || "";
                }
                return out;
            }"""
        ) or {}
    except Exception:
        return {}


def _should_fill_other_required(name: str, current_vals: Dict[str, str]) -> bool:
    try:
        nm = str(name or "").strip()
        if not nm.startswith("T") or "_" not in nm:
            return True
        body = nm[1:]
        base, suffix = body.rsplit("_", 1)
        selected_raw = str(current_vals.get(base, "") or "").strip()
        if not selected_raw:
            return False
        selected_vals = [x.strip() for x in selected_raw.split(",") if x.strip()]
        return suffix in selected_vals
    except Exception:
        return True


def _pick_numeric_value(min_v: Optional[int], max_v: Optional[int], exact_len: Optional[int] = None) -> str:
    current_year = _now_year()
    if min_v is not None and max_v is not None:
        lo, hi = int(min_v), int(max_v)
        if hi < lo:
            hi = lo
        if exact_len == 4:
            lo = max(lo, 1900)
            hi = min(hi, current_year - 1)
            if hi < lo:
                hi = lo
        return str(random.randint(lo, hi))
    if exact_len == 4:
        lo = max(1900, int(min_v) if min_v is not None else 1900)
        hi = min(current_year - 1, int(max_v) if max_v is not None else current_year - 1)
        if hi < lo:
            hi = lo
        return str(random.randint(lo, hi))
    if min_v is not None:
        lo = int(min_v)
        hi = lo + (20 if lo < 100 else 100)
        return str(random.randint(lo, hi))
    if max_v is not None:
        hi = max(1, int(max_v))
        return str(random.randint(1, hi))
    if exact_len and exact_len > 0:
        first = str(random.randint(1, 9)) if exact_len > 1 else str(random.randint(0, 9))
        rest = "".join(str(random.randint(0, 9)) for _ in range(max(0, exact_len - 1)))
        return first + rest
    return str(random.randint(1, 99))


def _guess_value_from_regex(field_name: str, regex_body: str) -> Optional[str]:
    nm = (field_name or "").lower()
    rb = regex_body or ""
    if ("email" in nm) or ("@" in rb and "\\." in rb):
        return generate_email(30)
    if ("010-" in rb) or ("01[1|6|7|8|9]" in rb) or ("01[16789]" in rb):
        return "010-6529-2005"
    if re.search(r"\\d\{4\}-\\d\{2\}-\\d\{2\}", rb):
        return "2026-03-13"
    if re.search(r"\\d\{4\}", rb):
        return "2020"
    if re.search(r"\\d\{2\}", rb):
        return "10"
    return None


def _fill_generic_other_visible_fields(page: Page, fill_text: str) -> List[str]:
    try:
        return page.evaluate(
            """(fillText) => {
                const reOther = /(기타|other|etc)/i;
                const result = [];
                function visible(el){
                    if (!el) return false;
                    const cs = window.getComputedStyle(el);
                    if (!cs) return true;
                    if (cs.display === "none" || cs.visibility === "hidden") return false;
                    if (el.disabled) return false;
                    if (el.type && String(el.type).toLowerCase() === "hidden") return false;
                    return true;
                }
                function fire(el){
                    try { el.dispatchEvent(new Event("input", {bubbles:true})); } catch(e){}
                    try { el.dispatchEvent(new Event("change", {bubbles:true})); } catch(e){}
                    try { el.dispatchEvent(new Event("blur", {bubbles:true})); } catch(e){}
                }
                const opts = Array.from(document.querySelectorAll('input[type="radio"], input[type="checkbox"]')).filter(x => x.checked);
                for (const opt of opts){
                    const scope = opt.closest("tr, td, li, .row, .form-group, .input-group, div, p") || opt.parentElement || document;
                    const txt = (scope.innerText || scope.textContent || "");
                    if (!reOther.test(txt)) continue;
                    const fields = Array.from(scope.querySelectorAll('input[type="text"], input[type="tel"], textarea')).filter(visible);
                    for (const el of fields){
                        if ((el.value || "").trim()) continue;
                        el.value = fillText;
                        fire(el);
                        result.push(String(el.name || el.id || "unknown"));
                    }
                }
                return result;
            }""",
            fill_text,
        ) or []
    except Exception:
        return []


def _safe_int(v: Any) -> Optional[int]:
    try:
        if v is None:
            return None
        s = str(v).strip()
        if s == "":
            return None
        return int(float(s))
    except Exception:
        return None


def _get_asp_numeric_constraints(cfg: Any) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = {}
    try:
        ov = getattr(cfg, "case_overrides", None) or {}
        if not isinstance(ov, dict):
            return out
        raw = ov.get("__NUM_CONSTRAINTS__", {}) or {}
        if not isinstance(raw, dict):
            return out
        for name, rule in raw.items():
            if not isinstance(rule, dict):
                continue
            mn = _safe_int(rule.get("min"))
            mx = _safe_int(rule.get("max"))
            if mn is None and mx is None:
                continue
            slot: Dict[str, int] = {}
            if mn is not None:
                slot["min"] = mn
            if mx is not None:
                slot["max"] = mx
            out[str(name)] = slot
    except Exception:
        return {}
    return out


def _merge_numeric_rules(
    asp_numeric: Dict[str, Dict[str, int]],
    js_numeric: Dict[str, Dict[str, int]],
) -> Tuple[Dict[str, Dict[str, int]], Dict[str, Dict[str, Any]]]:
    merged: Dict[str, Dict[str, int]] = {}
    conflicts: Dict[str, Dict[str, Any]] = {}
    names = set(asp_numeric.keys()) | set(js_numeric.keys())
    for name in names:
        a = asp_numeric.get(name, {}) or {}
        j = js_numeric.get(name, {}) or {}
        a_min = _safe_int(a.get("min"))
        a_max = _safe_int(a.get("max"))
        j_min = _safe_int(j.get("min"))
        j_max = _safe_int(j.get("max"))
        mins = [v for v in (a_min, j_min) if v is not None]
        maxs = [v for v in (a_max, j_max) if v is not None]
        mn = max(mins) if mins else None
        mx = min(maxs) if maxs else None
        if mn is not None and mx is not None and mn > mx:
            conflicts[name] = {
                "asp": {k: v for k, v in (("min", a_min), ("max", a_max)) if v is not None},
                "js": {k: v for k, v in (("min", j_min), ("max", j_max)) if v is not None},
                "merged": {"min": mn, "max": mx},
            }
            continue
        slot: Dict[str, int] = {}
        if mn is not None:
            slot["min"] = mn
        if mx is not None:
            slot["max"] = mx
        if slot:
            merged[name] = slot
    return merged, conflicts


def _build_combined_constraints(page: Page, cfg: Any) -> Dict[str, Any]:
    js_cons = extract_next_constraints(page)
    asp_numeric = _get_asp_numeric_constraints(cfg)
    js_numeric = js_cons.get("numeric", {}) or {}
    merged_numeric, conflicts = _merge_numeric_rules(asp_numeric, js_numeric)
    combined = dict(js_cons)
    combined["asp_numeric"] = asp_numeric
    combined["js_numeric"] = js_numeric
    combined["numeric"] = merged_numeric
    combined["numeric_conflicts"] = conflicts
    return combined



def _set_value_if_exists(page: Page, name: str, value: Any) -> bool:
    try:
        nm = _clean_field_name(name)
        if not nm:
            return False
        ok = bool(set_value(page, f'[name="{nm}"]', str(value)))
        if ok:
            return True
        return bool(set_value(page, f'#{nm}', str(value)))
    except Exception:
        return False


def _get_numeric_rule(cons: Dict[str, Any], name: str) -> Dict[str, Any]:
    nm = _clean_field_name(name)
    return ((cons.get('numeric') or {}).get(nm, {}) or {})


def _coerce_int(v: Any) -> Optional[int]:
    try:
        if v is None:
            return None
        s = str(v).strip()
        if s == '':
            return None
        return int(float(s))
    except Exception:
        return None


def _apply_relation_constraints(page: Page, cons: Dict[str, Any]) -> List[str]:
    changed: List[str] = []
    relations = list(cons.get('relations') or [])
    if not relations:
        return changed
    vals = _get_current_values(page)
    for rel in relations:
        left = _clean_field_name(rel.get('left'))
        right = _clean_field_name(rel.get('right'))
        op = str(rel.get('op') or '').strip()
        if not left or not right or not op:
            continue
        lv = _coerce_int(vals.get(left))
        rv = _coerce_int(vals.get(right))
        if lv is None or rv is None:
            continue
        ok = ((op == '<=' and lv <= rv) or (op == '<' and lv < rv) or (op == '>=' and lv >= rv) or (op == '>' and lv > rv))
        if ok:
            continue
        lrule = _get_numeric_rule(cons, left)
        rrule = _get_numeric_rule(cons, right)
        lmin, lmax = _coerce_int(lrule.get('min')), _coerce_int(lrule.get('max'))
        rmin, rmax = _coerce_int(rrule.get('min')), _coerce_int(rrule.get('max'))
        new_l, new_r = lv, rv
        if op in ('<=', '<'):
            target_r = lv if op == '<=' else lv + 1
            if rmax is not None:
                target_r = min(target_r, rmax)
            if rmin is not None:
                target_r = max(target_r, rmin)
            if ((op == '<=' and lv <= target_r) or (op == '<' and lv < target_r)):
                new_r = target_r
            else:
                target_l = rv if op == '<=' else rv - 1
                if lmin is not None:
                    target_l = max(target_l, lmin)
                if lmax is not None:
                    target_l = min(target_l, lmax)
                if ((op == '<=' and target_l <= rv) or (op == '<' and target_l < rv)):
                    new_l = target_l
                else:
                    continue
        else:
            target_l = rv if op == '>=' else rv + 1
            if lmin is not None:
                target_l = max(target_l, lmin)
            if lmax is not None:
                target_l = min(target_l, lmax)
            if ((op == '>=' and target_l >= rv) or (op == '>' and target_l > rv)):
                new_l = target_l
            else:
                target_r = lv if op == '>=' else lv - 1
                if rmin is not None:
                    target_r = max(target_r, rmin)
                if rmax is not None:
                    target_r = min(target_r, rmax)
                if ((op == '>=' and lv >= target_r) or (op == '>' and lv > target_r)):
                    new_r = target_r
                else:
                    continue
        if new_l != lv and _set_value_if_exists(page, left, new_l):
            changed.append(f"{left}={new_l}(relation:{left}{op}{right})")
            vals[left] = str(new_l)
            lv = new_l
        if new_r != rv and _set_value_if_exists(page, right, new_r):
            changed.append(f"{right}={new_r}(relation:{left}{op}{right})")
            vals[right] = str(new_r)
    return changed


def _get_conditional_numeric_rules(cfg: Any) -> List[Dict[str, Any]]:
    try:
        ov = getattr(cfg, "case_overrides", None) or {}
        if not isinstance(ov, dict):
            return []
        rules = ov.get("__COND_NUM_RULES__", []) or []
        if not isinstance(rules, list):
            return []
        return [r for r in rules if isinstance(r, dict)]
    except Exception:
        return []


def _get_matched_conditional_rule(
    page: Page,
    current_vals: Dict[str, Any],
    name: str,
    rules: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nm = _clean_field_name(name)
    if not nm or not rules:
        return {}

    best: Dict[str, Any] = {}
    best_score = -1

    for rule in rules:
        target = _clean_field_name(str(rule.get("target") or ""))
        if target != nm:
            continue

        when = rule.get("when") or {}
        if not isinstance(when, dict) or not when:
            continue

        matched = True
        score = 0
        for wk, wv in when.items():
            wkn = _clean_field_name(str(wk or ""))
            expected = str(wv or "").strip()
            actual = str(current_vals.get(wkn, "") or "").strip()
            if actual == "":
                try:
                    actual = str(page.locator(f'[name="{wkn}"]').first.input_value() or "").strip()
                except Exception:
                    actual = ""
            if actual != expected:
                matched = False
                break
            score += 1

        if matched and score > best_score:
            best = rule
            best_score = score

    return best


def _apply_conditional_numeric_rule(
    rule: Dict[str, Any],
    mn: Optional[int],
    mx: Optional[int],
) -> Tuple[Optional[int], Optional[int]]:
    if not isinstance(rule, dict):
        return mn, mx
    rmin = _safe_int(rule.get("min"))
    rmax = _safe_int(rule.get("max"))
    if rmin is not None:
        mn = rmin if mn is None else max(mn, rmin)
    if rmax is not None:
        mx = rmax if mx is None else min(mx, rmax)
    if mn is not None and mx is not None and mn > mx:
        mx = mn
    return mn, mx


def _filter_choice_values_with_rule(vals: List[str], rule: Dict[str, Any]) -> List[str]:
    if not vals:
        return vals
    out = [str(v).strip() for v in vals if str(v).strip() != ""]
    neq_vals = [str(x).strip() for x in (rule.get("neq") or []) if str(x).strip() != ""]
    if neq_vals:
        out = [v for v in out if v not in neq_vals]

    rmin = _safe_int(rule.get("min"))
    rmax = _safe_int(rule.get("max"))
    if rmin is not None or rmax is not None:
        num_vals = []
        for v in out:
            try:
                iv = int(float(v))
            except Exception:
                continue
            if rmin is not None and iv < rmin:
                continue
            if rmax is not None and iv > rmax:
                continue
            num_vals.append(v)
        if num_vals:
            out = num_vals
    return out


def apply_next_constraints(page: Page, meta: Dict[str, Any], cfg, logger: logging.Logger) -> Dict[str, Any]:
    cons = _build_combined_constraints(page, cfg)
    inputs_meta = meta.get("inputs_meta", {}) or {}
    current_vals = _get_current_values(page)
    cond_num_rules = _get_conditional_numeric_rules(cfg)
    changed: List[str] = []

    conflicts = cons.get("numeric_conflicts", {}) or {}
    if conflicts:
        msg_parts = []
        for name, detail in sorted(conflicts.items()):
            msg_parts.append(f"{name}: ASP={detail.get('asp', {})} JS={detail.get('js', {})}")
        logger.warning("[next_logic] numeric conflict: " + " | ".join(msg_parts))

    # required fill
    for name in sorted([x for x in cons.get("required", []) if str(x or "").strip()]):
        cur = current_vals.get(name, "")
        if not _is_empty_value(cur):
            continue
        if not _should_fill_other_required(name, current_vals):
            continue
        info = inputs_meta.get(name, {}) or {}
        itype = (info.get("type") or "text").lower()
        matched_rule = _get_matched_conditional_rule(page, current_vals, name, cond_num_rules)
        if name in meta.get("selects", {}):
            vals = [v for v in (meta["selects"].get(name) or []) if str(v).strip() not in ("", "0")]
            vals = _filter_choice_values_with_rule(vals, matched_rule)
            if vals:
                pick = str(random.choice(vals))
                if _set_value_if_exists(page, name, pick):
                    changed.append(f"{name}=select:{pick}")
            continue
        if name in meta.get("radios", {}):
            vals = [v for v in (meta["radios"].get(name) or []) if str(v).strip() not in ("", "0")]
            vals = _filter_choice_values_with_rule(vals, matched_rule)
            if vals:
                pick = str(random.choice(vals))
                if click_with_td_fallback(page, f'input[type="radio"][name="{name}"][value="{pick}"]') or set_checked(page, f'input[type="radio"][name="{name}"][value="{pick}"]', True):
                    changed.append(f"{name}=radio:{pick}")
            continue
        if name in meta.get("checks", {}):
            vals = [v for v in (meta["checks"].get(name) or []) if str(v).strip() != ""]
            vals = _filter_choice_values_with_rule(vals, matched_rule)
            if vals and set_checked(page, f'input[type="checkbox"][name="{name}"][value="{random.choice(vals)}"]', True):
                changed.append(f"{name}=check")
            continue
        cond_mn, cond_mx = _apply_conditional_numeric_rule(matched_rule, None, None)
        if cond_mn is not None or cond_mx is not None:
            exact_len = int(info.get("maxlength")) if str(info.get("maxlength") or "").isdigit() else None
            v = _pick_numeric_value(cond_mn, cond_mx, exact_len)
        elif itype == "email" or "email" in name.lower():
            v = generate_email(info.get("maxlength") or 30)
        else:
            v = generate_text(info.get("maxlength")) or "AUTO"
        if _set_value_if_exists(page, name, v):
            changed.append(f"{name}={v}")

    current_vals = _get_current_values(page)
    field_names = sorted(
        set((cons.get("numeric") or {}).keys())
        | set(cons.get("numeric_only", set()))
        | set((cons.get("length_min") or {}).keys())
        | set((cons.get("length_max") or {}).keys())
        | set((cons.get("regex") or {}).keys())
        | { _clean_field_name(str(r.get("target") or "")) for r in cond_num_rules if isinstance(r, dict) and str(r.get("target") or "").strip() }
    )

    for name in field_names:
        if name in meta.get("radios", {}) or name in meta.get("checks", {}):
            continue

        cur = str(current_vals.get(name, "") or "").strip()
        info = inputs_meta.get(name, {}) or {}
        itype = (info.get("type") or "").lower()
        maxlength = info.get("maxlength")
        min_len = int((cons.get("length_min", {}) or {}).get(name, 0) or 0)
        max_len_js = (cons.get("length_max", {}) or {}).get(name)
        numeric_only = name in (cons.get("numeric_only") or set())
        nrule = (cons.get("numeric", {}) or {}).get(name, {}) or {}
        mn = nrule.get("min")
        mx = nrule.get("max")
        matched_rule = _get_matched_conditional_rule(page, current_vals, name, cond_num_rules)
        mn, mx = _apply_conditional_numeric_rule(matched_rule, _safe_int(mn), _safe_int(mx))
        need_fix = False
        normalized = cur

        if numeric_only:
            digits = re.sub(r"\D", "", cur)
            if digits != cur:
                normalized = digits
                need_fix = True
            elif not cur:
                need_fix = True

        if min_len and len(str(normalized or "")) < min_len:
            need_fix = True
        if max_len_js is not None and len(str(normalized or "")) > int(max_len_js):
            normalized = str(normalized or "")[: int(max_len_js)]
            need_fix = True

        if mn is not None or mx is not None:
            try:
                num = int(float(str(normalized).strip()))
            except Exception:
                num = None
            if num is None or (mn is not None and num < int(mn)) or (mx is not None and num > int(mx)):
                need_fix = True

        if need_fix:
            exact_len = None
            try:
                if min_len:
                    exact_len = min_len
                elif maxlength and str(maxlength).isdigit():
                    exact_len = int(maxlength)
            except Exception:
                exact_len = None

            if numeric_only or itype in ("tel", "number") or mn is not None or mx is not None:
                v = _pick_numeric_value(_safe_int(mn), _safe_int(mx), exact_len)
            else:
                v = generate_text(maxlength) or "AUTO"
                if min_len and len(v) < min_len:
                    pad_to = max(min_len, int(maxlength) if maxlength and str(maxlength).isdigit() else min_len)
                    v = (v + ("X" * pad_to))[:pad_to]
                if max_len_js is not None:
                    v = v[: int(max_len_js)]
            if _set_value_if_exists(page, name, str(v)):
                changed.append(f"{name}={v}(constraint)")

        rb = (cons.get("regex", {}) or {}).get(name)
        if rb:
            try:
                ok = bool(page.evaluate(
                    """([nm, pat]) => {
                        const el = document.querySelector(`[name="${nm}"]`) || document.getElementById(nm);
                        if (!el) return false;
                        try { return new RegExp(pat).test((el.value || '').trim()); }
                        catch(e) { return false; }
                    }""",
                    [name, rb],
                ))
            except Exception:
                ok = False
            if not ok:
                guessed = _guess_value_from_regex(name, rb) or "AUTO"
                if _set_value_if_exists(page, name, guessed):
                    changed.append(f"{name}={guessed}(regex)")

    relation_changed = _apply_relation_constraints(page, cons)
    changed.extend(relation_changed)

    # final numeric clamp pass after relation handling and generic fills
    latest_vals = _get_current_values(page)
    for name, rule in sorted((cons.get("numeric", {}) or {}).items()):
        nm = _clean_field_name(name)
        if not nm:
            continue
        cur = str(latest_vals.get(nm, "") or "").strip()
        mn = _safe_int((rule or {}).get("min"))
        mx = _safe_int((rule or {}).get("max"))
        try:
            num = int(float(cur))
        except Exception:
            num = None
        if num is None:
            continue
        fixed = None
        if mn is not None and num < mn:
            fixed = mn
        if mx is not None and num > mx:
            fixed = mx if fixed is None else min(max(fixed, mn if mn is not None else fixed), mx)
        if fixed is not None and _set_value_if_exists(page, nm, fixed):
            changed.append(f"{nm}={fixed}(final_clamp)")
            latest_vals[nm] = str(fixed)

    other_changed = _fill_generic_other_visible_fields(page, getattr(cfg, "other_text_default", "모름"))
    for nm in other_changed:
        changed.append(f"{nm}=OTHER")

    if changed:
        logger.info("[next_logic] adjusted: " + " | ".join(changed))
    else:
        logger.info("[next_logic] no adjustment")
    return {"constraints": cons, "changed": changed}


def diagnose_next_failures(page: Page, meta: Dict[str, Any], logger: logging.Logger) -> List[str]:
    cfg = None
    try:
        cfg = (meta or {}).get("cfg")
    except Exception:
        cfg = None
    cons = _build_combined_constraints(page, cfg)
    vals = _get_current_values(page)
    issues: List[str] = []

    for name in sorted([x for x in cons.get("required", []) if str(x or "").strip()]):
        if not _should_fill_other_required(name, vals):
            continue
        if _is_empty_value(vals.get(name, "")):
            issues.append(f"required:{name}")

    for name in sorted(cons.get("numeric_only", set())):
        cur = str(vals.get(name, "") or "").strip()
        if cur and not re.fullmatch(r"\d+", cur):
            issues.append(f"numeric_only:{name}")

    for name, min_len in sorted((cons.get("length_min", {}) or {}).items()):
        cur = str(vals.get(name, "") or "").strip()
        if cur and len(cur) < int(min_len):
            issues.append(f"min_length:{name}<{min_len}")

    for name, max_len in sorted((cons.get("length_max", {}) or {}).items()):
        cur = str(vals.get(name, "") or "").strip()
        if cur and len(cur) > int(max_len):
            issues.append(f"max_length:{name}>{max_len}")

    for name, detail in sorted((cons.get("numeric_conflicts") or {}).items()):
        issues.append(f"numeric_conflict:{name}:ASP={detail.get('asp', {})}:JS={detail.get('js', {})}")

    for name, rule in sorted((cons.get("numeric", {}) or {}).items()):
        cur = str(vals.get(name, "") or "").strip()
        try:
            num = int(float(cur))
        except Exception:
            num = None
        mn = rule.get("min")
        mx = rule.get("max")
        if num is None:
            issues.append(f"numeric_invalid:{name}")
        elif mn is not None and num < int(mn):
            issues.append(f"numeric_min:{name}<{mn}")
        elif mx is not None and num > int(mx):
            issues.append(f"numeric_max:{name}>{mx}")

    for rel in list(cons.get('relations') or []):
        left = _clean_field_name(rel.get('left'))
        right = _clean_field_name(rel.get('right'))
        op = str(rel.get('op') or '').strip()
        if not left or not right or not op:
            continue
        lv = _coerce_int(vals.get(left))
        rv = _coerce_int(vals.get(right))
        if lv is None or rv is None:
            continue
        ok = ((op == '<=' and lv <= rv) or (op == '<' and lv < rv) or (op == '>=' and lv >= rv) or (op == '>' and lv > rv))
        if not ok:
            issues.append(f"relation:{left}{op}{right}")

    for name, rb in sorted((cons.get("regex") or {}).items()):
        try:
            ok = bool(page.evaluate(
                """([nm, pat]) => {
                    const el = document.querySelector(`[name="${nm}"]`) || document.getElementById(nm);
                    if (!el) return false;
                    try { return new RegExp(pat).test((el.value || '').trim()); }
                    catch(e) { return false; }
                }""",
                [name, rb],
            ))
        except Exception:
            ok = False
        if not ok:
            issues.append(f"regex_fail:{name}")

    # 7) Canvas / SignaturePad check
    try:
        has_empty_sig = bool(page.evaluate(
            """() => {
                const canvases = Array.from(document.querySelectorAll('canvas'));
                if (canvases.length === 0) return false;
                
                // SignaturePad 인스턴스가 전역으로 있는 경우 검사
                if (window.signaturePad && typeof window.signaturePad.isEmpty === 'function') {
                    return window.signaturePad.isEmpty();
                }
                
                // 전역 인스턴스가 없더라도, canvas가 존재하고 #upload 버튼이 있으면 서명 필요 문항으로 간주
                const uploadBtn = document.querySelector('#upload, #btn_upload');
                if (uploadBtn) {
                    // canvas가 비어있는지 픽셀 검사 (완벽하진 않으나 힌트로 사용)
                    for (const cv of canvases) {
                        try {
                            const ctx = cv.getContext('2d');
                            const data = ctx.getImageData(0, 0, cv.width, cv.height).data;
                            let is_empty = true;
                            for (let i = 0; i < data.length; i += 4) {
                                if (data[i+3] > 0) { // 투명도가 0보다 큰 픽셀이 있으면 비어있는 게 아님
                                    is_empty = false;
                                    break;
                                }
                            }
                            if (is_empty) return true;
                        } catch(e) {}
                    }
                }
                return false;
            }"""
        ))
        if has_empty_sig:
            issues.append("signature_empty")
    except Exception:
        pass

    if issues:
        logger.warning("[next_logic] unresolved: " + " | ".join(issues))
    else:
        logger.info("[next_logic] no unresolved issues detected")
    return issues





def _repair_specific_issues(page: Page, meta: Dict[str, Any], cfg, issues: List[str], logger: logging.Logger) -> List[str]:
    """
    diagnose_next_failures()가 찾아낸 이슈만 가볍게 보정한다.
    전체 apply_next_constraints()보다 범위가 훨씬 좁다.
    - numeric_invalid / numeric_min / numeric_max / numeric_only / length
    - relation
    - regex_fail
    - required
    까지 범용적으로 처리한다.
    """
    cons = _build_combined_constraints(page, cfg)
    vals = _get_current_values(page)
    inputs_meta = (meta or {}).get("inputs_meta", {}) or {}
    cond_num_rules = _get_conditional_numeric_rules(cfg)
    changed: List[str] = []

    def _maxlength(name: str) -> Optional[int]:
        try:
            raw = (inputs_meta.get(name) or {}).get("maxlength")
            if raw is None:
                return None
            s = str(raw).strip()
            return int(s) if s.isdigit() else None
        except Exception:
            return None

    def _matched_rule(name: str) -> Dict[str, Any]:
        try:
            return _get_matched_conditional_rule(page, vals, name, cond_num_rules)
        except Exception:
            return {}

    def _numeric_bounds(name: str) -> Tuple[Optional[int], Optional[int]]:
        base_rule = _get_numeric_rule(cons, name)
        mn = _coerce_int(base_rule.get('min'))
        mx = _coerce_int(base_rule.get('max'))
        mn, mx = _apply_conditional_numeric_rule(_matched_rule(name), mn, mx)
        return mn, mx

    def _apply_numeric_fix(name: str, reason: str, prefer_min: bool = False, prefer_max: bool = False) -> bool:
        nonlocal vals
        nm = _clean_field_name(name)
        if not nm:
            return False
        mn, mx = _numeric_bounds(nm)
        cur_num = _coerce_int(vals.get(nm))
        if prefer_min and mn is not None:
            pick = _pick_numeric_value(mn, mx, _maxlength(nm))
        elif prefer_max and mx is not None:
            pick = _pick_numeric_value(mn, mx, _maxlength(nm))
        elif cur_num is None:
            pick = _pick_numeric_value(mn, mx, _maxlength(nm))
        elif mn is not None and cur_num < mn:
            pick = _pick_numeric_value(mn, mx, _maxlength(nm))
        elif mx is not None and cur_num > mx:
            pick = _pick_numeric_value(mn, mx, _maxlength(nm))
        else:
            if mn is None and mx is None:
                ml = _maxlength(nm)
                pick = _pick_numeric_value(0, None, ml)
            else:
                pick = _pick_numeric_value(mn, mx, _maxlength(nm))
        if _set_value_if_exists(page, nm, pick):
            changed.append(f"{nm}={pick}({reason})")
            vals[nm] = str(pick)
            return True
        return False

    def _apply_relation_issue(left: str, op: str, right: str) -> bool:
        nonlocal vals
        left = _clean_field_name(left)
        right = _clean_field_name(right)
        if not left or not right or op not in ('<=', '<', '>=', '>'):
            return False
        lv = _coerce_int(vals.get(left))
        rv = _coerce_int(vals.get(right))
        lmn, lmx = _numeric_bounds(left)
        rmn, rmx = _numeric_bounds(right)

        if lv is None and not _apply_numeric_fix(left, f"issue:relation:{left}{op}{right}:left", prefer_min=True):
            return False
        vals = _get_current_values(page)
        lv = _coerce_int(vals.get(left))
        if rv is None and not _apply_numeric_fix(right, f"issue:relation:{left}{op}{right}:right", prefer_min=True):
            return False
        vals = _get_current_values(page)
        lv = _coerce_int(vals.get(left))
        rv = _coerce_int(vals.get(right))
        if lv is None or rv is None:
            return False

        ok = ((op == '<=' and lv <= rv) or (op == '<' and lv < rv) or (op == '>=' and lv >= rv) or (op == '>' and lv > rv))
        if ok:
            return False

        new_l, new_r = lv, rv
        if op in ('<=', '<'):
            target_r = lv if op == '<=' else lv + 1
            if rmx is not None:
                target_r = min(target_r, rmx)
            if rmn is not None:
                target_r = max(target_r, rmn)
            if ((op == '<=' and lv <= target_r) or (op == '<' and lv < target_r)):
                new_r = target_r
            else:
                target_l = rv if op == '<=' else rv - 1
                if lmn is not None:
                    target_l = max(target_l, lmn)
                if lmx is not None:
                    target_l = min(target_l, lmx)
                if ((op == '<=' and target_l <= rv) or (op == '<' and target_l < rv)):
                    new_l = target_l
                else:
                    return False
        else:
            target_l = rv if op == '>=' else rv + 1
            if lmn is not None:
                target_l = max(target_l, lmn)
            if lmx is not None:
                target_l = min(target_l, lmx)
            if ((op == '>=' and target_l >= rv) or (op == '>' and target_l > rv)):
                new_l = target_l
            else:
                target_r = lv if op == '>=' else lv - 1
                if rmn is not None:
                    target_r = max(target_r, rmn)
                if rmx is not None:
                    target_r = min(target_r, rmx)
                if ((op == '>=' and lv >= target_r) or (op == '>' and lv > target_r)):
                    new_r = target_r
                else:
                    return False

        applied = False
        if new_l != lv and _set_value_if_exists(page, left, new_l):
            changed.append(f"{left}={new_l}(issue:relation:{left}{op}{right})")
            vals[left] = str(new_l)
            applied = True
        if new_r != rv and _set_value_if_exists(page, right, new_r):
            changed.append(f"{right}={new_r}(issue:relation:{left}{op}{right})")
            vals[right] = str(new_r)
            applied = True
        return applied

    for issue in issues or []:
        if not issue:
            continue

        m = re.match(r'^required:(.+)$', issue)
        if m:
            name = _clean_field_name(m.group(1))
            if name:
                info = inputs_meta.get(name, {}) or {}
                itype = (info.get('type') or 'text').lower()
                if name in (meta.get('selects') or {}):
                    options = [v for v in ((meta.get('selects') or {}).get(name) or []) if str(v).strip() not in ('', '0')]
                    options = _filter_choice_values_with_rule(options, _matched_rule(name))
                    if options:
                        pick = str(options[0])
                        if _set_value_if_exists(page, name, pick):
                            changed.append(f"{name}={pick}(issue:required:select)")
                            vals[name] = pick
                    continue
                if name in (meta.get('radios') or {}):
                    options = [v for v in ((meta.get('radios') or {}).get(name) or []) if str(v).strip() not in ('', '0')]
                    options = _filter_choice_values_with_rule(options, _matched_rule(name))
                    if options:
                        pick = str(options[0])
                        if click_with_td_fallback(page, f'input[type="radio"][name="{name}"][value="{pick}"]') or set_checked(page, f'input[type="radio"][name="{name}"][value="{pick}"]', True):
                            changed.append(f"{name}={pick}(issue:required:radio)")
                            vals[name] = pick
                    continue
                if name in (meta.get('checks') or {}):
                    options = [v for v in ((meta.get('checks') or {}).get(name) or []) if str(v).strip() != '']
                    options = _filter_choice_values_with_rule(options, _matched_rule(name))
                    if options and set_checked(page, f'input[type="checkbox"][name="{name}"][value="{options[0]}"]', True):
                        changed.append(f"{name}={options[0]}(issue:required:check)")
                        vals[name] = str(options[0])
                    continue
                if itype == 'email' or 'email' in name.lower():
                    v = generate_email(_maxlength(name) or 30)
                elif itype == 'tel' or re.search(r'(hp|phone|mobile|cell|tel)', name, flags=re.I):
                    iid = str(info.get('id') or '')
                    v = generate_tel_digits(_maxlength(name), pattern=info.get('pattern'), name=name, iid=iid)
                else:
                    mn, mx = _numeric_bounds(name)
                    if mn is not None or mx is not None:
                        v = _pick_numeric_value(mn, mx, _maxlength(name))
                    else:
                        v = generate_text(_maxlength(name)) or 'AUTO'
                if _set_value_if_exists(page, name, v):
                    changed.append(f"{name}={v}(issue:required)")
                    vals[name] = str(v)
            continue

        m = re.match(r'^numeric_invalid:(.+)$', issue)
        if m:
            _apply_numeric_fix(m.group(1), 'issue:invalid')
            continue

        m = re.match(r'^numeric_max:([^>]+)>(-?\d+)$', issue)
        if m:
            _apply_numeric_fix(m.group(1), 'issue:max', prefer_max=True)
            continue

        m = re.match(r'^numeric_min:([^<]+)<(-?\d+)$', issue)
        if m:
            _apply_numeric_fix(m.group(1), 'issue:min', prefer_min=True)
            continue

        m = re.match(r'^numeric_only:(.+)$', issue)
        if m:
            name = _clean_field_name(m.group(1))
            if name:
                cur = str(vals.get(name, '') or '')
                digits = re.sub(r'\D', '', cur)
                if digits != cur and _set_value_if_exists(page, name, digits):
                    changed.append(f"{name}={digits}(issue:numeric_only)")
                    vals[name] = digits
            continue

        m = re.match(r'^max_length:([^>]+)>(\d+)$', issue)
        if m:
            name = _clean_field_name(m.group(1))
            mx = _safe_int(m.group(2))
            if name and mx is not None:
                cur = str(vals.get(name, '') or '')
                fixed = cur[:mx]
                if fixed != cur and _set_value_if_exists(page, name, fixed):
                    changed.append(f"{name}={fixed}(issue:maxlen)")
                    vals[name] = fixed
            continue

        m = re.match(r'^min_length:([^<]+)<(\d+)$', issue)
        if m:
            name = _clean_field_name(m.group(1))
            mn = _safe_int(m.group(2))
            if name and mn is not None:
                cur = str(vals.get(name, '') or '')
                if len(cur) < mn:
                    fixed = (cur + ('0' * mn))[:mn]
                    if _set_value_if_exists(page, name, fixed):
                        changed.append(f"{name}={fixed}(issue:minlen)")
                        vals[name] = fixed
            continue

        m = re.match(r'^relation:([^<>=]+)(<=|>=|<|>)([^<>=]+)$', issue)
        if m:
            _apply_relation_issue(m.group(1), m.group(2), m.group(3))
            continue

        m = re.match(r'^regex_fail:(.+)$', issue)
        if m:
            name = _clean_field_name(m.group(1))
            rb = str(((cons.get('regex') or {}).get(name) or '')).strip()
            if name and rb:
                guessed = _guess_value_from_regex(name, rb) or 'AUTO'
                if _set_value_if_exists(page, name, guessed):
                    changed.append(f"{name}={guessed}(issue:regex)")
                    vals[name] = guessed
            continue

    if changed:
        logger.info("[next_logic] issue_repair: " + " | ".join(changed))
    return changed

def _extract_radio_array_bias_rules(src: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    text = _strip_js_comments(src or "")
    if not text:
        return out
    for m in re.finditer(r'RadioArrayCnt\(\s*["\']([^"\']+)["\']\s*,\s*(\d+)\s*\)', text, flags=re.I):
        names = [_clean_field_name(x) for x in str(m.group(1) or "").split(",") if _clean_field_name(x)]
        try:
            threshold = int(m.group(2))
        except Exception:
            threshold = 0
        if len(names) >= 2 and threshold > 0:
            out.append({"names": names, "threshold": threshold})
    return out


def _repair_radio_bias_from_source(page: Page, meta: Dict[str, Any], logger: logging.Logger, src: str) -> List[str]:
    changed: List[str] = []
    radios = (meta or {}).get("radios", {}) or {}
    rules = _extract_radio_array_bias_rules(src)
    if not rules:
        return changed

    for rule in rules:
        names = [n for n in (rule.get("names") or []) if n in radios]
        threshold = int(rule.get("threshold") or 0)
        if len(names) < 2 or threshold <= 0:
            continue

        cur_vals: Dict[str, str] = {}
        freq: Dict[str, int] = defaultdict(int)
        for nm in names:
            val = str(page.evaluate(
                """(qname) => {
                  const el = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
                  if (!el) return '';
                  return String(el.getAttribute('value') || el.value || '').trim();
                }""",
                nm,
            ) or "").strip()
            if not val:
                continue
            cur_vals[nm] = val
            freq[val] += 1

        overloaded = [v for v, c in freq.items() if c >= threshold]
        if not overloaded:
            continue

        for overloaded_val in overloaded:
            target_names = [nm for nm in names if cur_vals.get(nm) == overloaded_val]
            random.shuffle(target_names)
            repaired = False
            for nm in target_names:
                candidates = [str(v).strip() for v in (radios.get(nm) or []) if str(v).strip() not in ('', overloaded_val)]
                candidates.sort(key=lambda v: (freq.get(v, 0), random.random()))
                for pick in candidates:
                    ok = click_with_td_fallback(page, f'input[type="radio"][name="{nm}"][value="{pick}"]') or set_checked(page, f'input[type="radio"][name="{nm}"][value="{pick}"]', True)
                    if not ok:
                        continue
                    changed.append(f"{nm}={pick}(alert:bias)")
                    old_val = cur_vals.get(nm, "")
                    if old_val:
                        freq[old_val] = max(0, int(freq.get(old_val, 0)) - 1)
                    freq[pick] = int(freq.get(pick, 0)) + 1
                    cur_vals[nm] = pick
                    repaired = True
                    break
                if repaired:
                    break
    return changed


def _extract_product_limit_rules(src: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    text = _strip_js_comments(src or "")
    if not text:
        return out

    assign_pat = re.compile(
        r'var\s+(\w+)\s*=\s*parseInt\(\$\("#([^"]+)"\)\.val\(\)\.replace\(/,\/g,\s*["\']{2}\),\s*10\)\s*\|\|\s*0\s*;', 
        flags=re.I,
    )
    vars_to_fields: Dict[str, str] = {}
    for m in assign_pat.finditer(text):
        vars_to_fields[m.group(1).strip()] = _clean_field_name(m.group(2))

    for mm in re.finditer(r'var\s+\w+\s*=\s*(\w+)\s*\*\s*(\w+)\s*;.*?var\s+\w+\s*=\s*parseInt\(\s*["\']?(\d+)["\']?', text, flags=re.I | re.S):
        left_var = mm.group(1).strip()
        right_var = mm.group(2).strip()
        limit = _safe_int(mm.group(3))
        left = vars_to_fields.get(left_var, "")
        right = vars_to_fields.get(right_var, "")
        if left and right and limit is not None:
            out.append({"left": left, "right": right, "limit": int(limit)})
    return out


def _repair_product_limit_from_source(page: Page, meta: Dict[str, Any], cfg: Any, logger: logging.Logger, src: str) -> List[str]:
    changed: List[str] = []
    cons = _build_combined_constraints(page, cfg)
    rules = _extract_product_limit_rules(src)
    if not rules:
        return changed

    vals = _get_current_values(page)
    for rule in rules:
        left = _clean_field_name(rule.get("left"))
        right = _clean_field_name(rule.get("right"))
        limit = _safe_int(rule.get("limit"))
        if not left or not right or limit is None:
            continue
        lv = _safe_int(vals.get(left))
        rv = _safe_int(vals.get(right))
        if lv is None or rv is None or lv * rv <= limit:
            continue

        lrule = _get_numeric_rule(cons, left)
        rrule = _get_numeric_rule(cons, right)
        lmin, lmax = _coerce_int(lrule.get("min")), _coerce_int(lrule.get("max"))
        rmin, rmax = _coerce_int(rrule.get("min")), _coerce_int(rrule.get("max"))
        candidates: List[Tuple[str, int]] = []

        target_right = limit // max(1, lv)
        if rmax is not None:
            target_right = min(target_right, rmax)
        if rmin is not None:
            target_right = max(target_right, rmin)
        if target_right * lv <= limit:
            candidates.append((right, int(target_right)))

        target_left = limit // max(1, rv)
        if lmax is not None:
            target_left = min(target_left, lmax)
        if lmin is not None:
            target_left = max(target_left, lmin)
        if target_left * rv <= limit:
            candidates.append((left, int(target_left)))

        if not candidates:
            fallback_right = max(rmin or 0, min(limit, rv))
            candidates.append((right, int(fallback_right)))

        candidates.sort(key=lambda x: (abs((_safe_int(vals.get(x[0])) or 0) - x[1]), x[0]))
        target_name, target_value = candidates[0]
        if _set_value_if_exists(page, target_name, str(target_value)):
            changed.append(f"{target_name}={target_value}(alert:product_limit)")
            vals[target_name] = str(target_value)
    return changed


def _extract_string_vars(src: str) -> Dict[str, str]:
    """
    var NAME = "VALUE"; 또는 var NAME = 'VALUE';에서 문자열 변수 할당을 추출.
    fp1var = "7" 같은 금지값 변수 해소에 사용.
    """
    text = _strip_js_comments(src)
    out: Dict[str, str] = {}
    for m in re.finditer(
        r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*["\']([^"\']*)["\']',
        text, flags=re.I
    ):
        out.setdefault(m.group(1), m.group(2))
    return out


def _extract_forbidden_radio_values(src: str) -> Dict[str, List[str]]:
    """
    next()에서 getRadioValue("FIELD") == "VALUE" 또는 fp1var 같은
    변수 갱당 패턴을 찾아 금지 라디오 값을 추출.
    반환: {field_name: [forbidden_value, ...]}
    """
    text = _strip_js_comments(src or "")
    if not text:
        return {}
    string_vars = _extract_string_vars(text)
    scalar_vars = _extract_scalar_vars(text)
    out: Dict[str, List[str]] = {}
    pat = re.compile(
        r'getRadioValue\(\s*["\']([^"\']+)["\']\s*\)\s*==\s*(?:["\']([^"\']*)["\']|([A-Za-z_]\w*))',
        flags=re.I,
    )
    for m in pat.finditer(text):
        field = m.group(1).strip()
        literal = m.group(2)  # 문자열 리터럴
        var_ref = m.group(3)  # 변수 참조
        if literal is not None:
            forbidden_val = str(literal).strip()
        elif var_ref:
            if var_ref in string_vars:
                forbidden_val = str(string_vars[var_ref]).strip()
            elif var_ref in scalar_vars:
                forbidden_val = str(scalar_vars[var_ref]).strip()
            else:
                continue
        else:
            continue
        if field and forbidden_val:
            out.setdefault(field, [])
            if forbidden_val not in out[field]:
                out[field].append(forbidden_val)
    return out


def _repair_forbidden_radio_values(
    page: Page,
    meta: Dict[str, Any],
    src: str,
    logger: logging.Logger,
) -> List[str]:
    """
    현재 선택된 radio 값이 next() JS에서 명시적으로 차단(예: fp1var="7")된 경우,
    다른 유효한 값으로 재선택한다.
    """
    changed: List[str] = []
    forbidden = _extract_forbidden_radio_values(src)
    if not forbidden:
        return changed
    radios = (meta or {}).get("radios", {}) or {}
    for field, bad_values in forbidden.items():
        try:
            cur = str(page.evaluate(
                """(qname) => {
                  const el = document.querySelector(`input[type="radio"][name="${qname}"]:checked`);
                  return el ? String(el.getAttribute("value") || el.value || "").trim() : "";
                }""",
                field,
            ) or "").strip()
        except Exception:
            continue
        if not cur or cur not in bad_values:
            continue
        candidates = [
            str(v).strip() for v in (radios.get(field) or [])
            if str(v).strip() and str(v).strip() not in bad_values
        ]
        if not candidates:
            logger.warning(f"[next_logic] forbidden_radio: {field}={cur} 유효한 대체값 없음")
            continue
        random.shuffle(candidates)
        for pick in candidates:
            sel = f'input[type="radio"][name="{field}"][value="{pick}"]'
            ok = click_with_td_fallback(page, sel) or set_checked(page, sel, True)
            if ok:
                logger.info(f"[next_logic] forbidden_radio: {field} 값 변경 {cur} -> {pick}")
                changed.append(f"{field}={pick}(alert:forbidden_radio)")
                break
    return changed


def repair_after_alert(page: Page, meta: Dict[str, Any], cfg, logger: logging.Logger, alert_text: str = "") -> Dict[str, Any]:
    """
    Alert 복구는 문항명을 하드코딩하지 않고, 먼저 현재 페이지의 next() 제약을 진단해서
    실제 실패 이슈(numeric_min/max, relation, regex 등)를 바로 고친다.

    흐름:
      0) diagnose_next_failures() -> _repair_specific_issues()  (가장 우선, 완전 범용)
      1) alert 문구 기반의 가벼운 보정 (월/일/년/시/분/전화번호/숫자 등)
      2) 그래도 바뀐 게 없을 때만 apply_next_constraints() fallback
      3) 마지막으로 한 번 더 diagnose_next_failures()를 돌려 남은 이슈를 보정
    """
    text = str(alert_text or "")
    inputs_meta = (meta or {}).get("inputs_meta", {}) or {}
    vals = _get_current_values(page)
    changed: List[str] = []
    fallback_result: Dict[str, Any] = {"constraints": {}, "changed": []}
    diag_meta = {**(meta or {}), "cfg": cfg}

    def _dedupe(items: List[str]) -> List[str]:
        out: List[str] = []
        seen: Set[str] = set()
        for x in items:
            if x in seen:
                continue
            seen.add(x)
            out.append(x)
        return out

    def _safe_maxlen(info: Dict[str, Any]) -> Optional[int]:
        try:
            raw = info.get("maxlength")
            if raw is None:
                return None
            s = str(raw).strip()
            if not s:
                return None
            return int(s)
        except Exception:
            return None

    def _refresh_vals() -> Dict[str, Any]:
        try:
            return _get_current_values(page)
        except Exception:
            return vals

    def _month_candidate_names() -> List[str]:
        scored: List[tuple[int, str]] = []
        for name, info in inputs_meta.items():
            nm = str(name or "")
            low = nm.lower()
            score = 0
            if re.search(r"(^|_)(mm|month)(_|$)", low):
                score += 200
            if "month" in low or "mon" in low:
                score += 120
            if low.endswith("_2"):
                score += 60
            if low.endswith("2"):
                score += 30
            ml = _safe_maxlen(info)
            if ml == 2:
                score += 20
            cur = str(vals.get(nm, "") or "").strip()
            if cur == "" or not cur.isdigit() or not (1 <= int(cur) <= 12):
                score += 15
            if score > 0:
                scored.append((score, nm))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [nm for _, nm in scored]

    def _day_candidate_names() -> List[str]:
        scored: List[tuple[int, str]] = []
        for name, info in inputs_meta.items():
            nm = str(name or "")
            low = nm.lower()
            score = 0
            if re.search(r"(^|_)(dd|day)(_|$)", low):
                score += 200
            if "day" in low:
                score += 120
            if low.endswith("_3"):
                score += 60
            if low.endswith("3"):
                score += 30
            ml = _safe_maxlen(info)
            if ml == 2:
                score += 20
            cur = str(vals.get(nm, "") or "").strip()
            if cur == "" or not cur.isdigit() or not (1 <= int(cur) <= 31):
                score += 15
            if score > 0:
                scored.append((score, nm))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [nm for _, nm in scored]

    def _year_candidate_names() -> List[str]:
        scored: List[tuple[int, str]] = []
        for name, info in inputs_meta.items():
            nm = str(name or "")
            low = nm.lower()
            score = 0
            if re.search(r"(^|_)(yy|yyyy|year)(_|$)", low):
                score += 200
            if "year" in low:
                score += 120
            if low.endswith("_1"):
                score += 60
            if low.endswith("1"):
                score += 30
            ml = _safe_maxlen(info)
            if ml == 4:
                score += 40
            cur = str(vals.get(nm, "") or "").strip()
            try:
                num = int(cur)
            except Exception:
                num = None
            if num is None or not (1900 <= num <= _now_year()):
                score += 15
            if score > 0:
                scored.append((score, nm))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [nm for _, nm in scored]

    def _set_first_valid(names: List[str], picker, tag: str) -> bool:
        nonlocal vals
        for nm in names:
            info = inputs_meta.get(nm, {}) or {}
            ml = _safe_maxlen(info)
            try:
                value = str(picker(nm, info, ml))
            except Exception:
                continue
            if not value:
                continue
            if _set_value_if_exists(page, nm, value):
                changed.append(f"{nm}={value}({tag})")
                vals[nm] = value
                return True
        return False

    # 0) alert 문구가 모호해도 먼저 issue 기반 범용 복구를 시도
    try:
        initial_issues = diagnose_next_failures(page, diag_meta, logger)
    except Exception:
        initial_issues = []

    if initial_issues:
        issue_changed = _repair_specific_issues(page, meta, cfg, initial_issues, logger)
        if issue_changed:
            changed.extend(issue_changed)
            vals = _refresh_vals()

    quick_changed = bool(changed)

    try:
        next_src = extract_next_source(page) or ""
    except Exception:
        next_src = ""

    if ("편중" in text or "응답하신 금액을 확인" in text or "총 할부금액" in text or "한도 금액" in text) and next_src:
        extra_changed: List[str] = []
        if "편중" in text:
            extra_changed.extend(_repair_radio_bias_from_source(page, meta, logger, next_src))
        if ("응답하신 금액을 확인" in text or "총 할부금액" in text or "한도 금액" in text):
            extra_changed.extend(_repair_product_limit_from_source(page, meta, cfg, logger, next_src))
        if extra_changed:
            changed.extend(extra_changed)
            vals = _refresh_vals()
            quick_changed = True

    # forbidden radio value 복구: getRadioValue("FIELD") == fp1var(="7") 패턴
    # 알람 문구에 무관하게 next() 소스에서 직접 감지
    if next_src:
        forbidden_changed = _repair_forbidden_radio_values(page, meta, next_src, logger)
        if forbidden_changed:
            changed.extend(forbidden_changed)
            vals = _refresh_vals()
            quick_changed = True

    if ("기타에 응답" in text or "기타에 응답해 주십시오" in text or "특수문자" in text or "중복됩니다" in text):
        bases: List[str] = []
        try:
            if next_src:
                for m in re.finditer(r"[Tt]([A-Za-z][A-Za-z0-9]*)_\d+", next_src):
                    b = str(m.group(1) or "").strip()
                    if b and b not in bases:
                        bases.append(b)
        except Exception:
            pass
        if not bases:
            try:
                for name in (inputs_meta or {}).keys():
                    nm = str(name or "")
                    mm = re.match(r"^T([A-Za-z][A-Za-z0-9]*)_\d+$", nm)
                    if mm:
                        b = mm.group(1)
                        if b not in bases:
                            bases.append(b)
            except Exception:
                pass
        other_changed: List[str] = []
        for base in bases:
            try:
                synced = sync_other_inputs_for_base(page, meta, base, cfg, logger)
                for nm in synced:
                    other_changed.append(f"{nm}=OTHER")
            except Exception:
                continue
        if other_changed:
            changed.extend(other_changed)
            vals = _refresh_vals()
            quick_changed = True

    # 1) alert 문구 기반 가벼운 보정
    if re.search(r"월", text):
        quick_changed = _set_first_valid(
            _month_candidate_names(),
            lambda nm, info, ml: _pick_numeric_value(1, 12, 2 if ml == 2 else ml),
            "alert:month",
        ) or quick_changed

    if re.search(r"일", text) and not re.search(r"월", text):
        quick_changed = _set_first_valid(
            _day_candidate_names(),
            lambda nm, info, ml: _pick_numeric_value(1, 28, 2 if ml == 2 else ml),
            "alert:day",
        ) or quick_changed

    if re.search(r"년|연도", text):
        quick_changed = _set_first_valid(
            _year_candidate_names(),
            lambda nm, info, ml: _pick_numeric_value(2000, _now_year() - 1, 4 if (ml == 4 or ml is None) else ml),
            "alert:year",
        ) or quick_changed

    if re.search(r"시", text):
        quick_changed = _set_first_valid(
            _dedupe([n for n in sorted(inputs_meta.keys()) if str(n).lower().endswith("_3") or str(n).lower().endswith("3")]),
            lambda nm, info, ml: _pick_numeric_value(0, 23, 2 if ml == 2 else ml),
            "alert:hour",
        ) or quick_changed

    if re.search(r"분", text):
        quick_changed = _set_first_valid(
            _dedupe([n for n in sorted(inputs_meta.keys()) if str(n).lower().endswith("_4") or str(n).lower().endswith("4")]),
            lambda nm, info, ml: _pick_numeric_value(0, 59, 2 if ml == 2 else ml),
            "alert:minute",
        ) or quick_changed

    if re.search(r"숫자", text):
        for name, info in inputs_meta.items():
            cur = str(vals.get(name, "") or "")
            digits = re.sub(r"\D", "", cur)
            if cur and digits != cur:
                if _set_value_if_exists(page, name, digits):
                    changed.append(f"{name}={digits}(alert:numeric_only)")
                    vals[name] = digits
                    quick_changed = True
                    break

    m = re.search(r"(\d+)\s*이상", text)
    if m:
        target = int(m.group(1))
        for name, info in inputs_meta.items():
            cur = str(vals.get(name, "") or "").strip()
            try:
                num = int(float(cur))
            except Exception:
                num = None
            if num is None or num < target:
                v = _pick_numeric_value(target, None, _safe_maxlen(info))
                if _set_value_if_exists(page, name, v):
                    changed.append(f"{name}={v}(alert:min)")
                    vals[name] = v
                    quick_changed = True
                    break

    m = re.search(r"(\d+)\s*이하", text)
    if m:
        target = int(m.group(1))
        for name, info in inputs_meta.items():
            cur = str(vals.get(name, "") or "").strip()
            try:
                num = int(float(cur))
            except Exception:
                num = None
            if num is None or num > target:
                v = _pick_numeric_value(None, target, _safe_maxlen(info))
                if _set_value_if_exists(page, name, v):
                    changed.append(f"{name}={v}(alert:max)")
                    vals[name] = v
                    quick_changed = True
                    break

    phone_alert = re.search(r"휴대폰번호|휴대폰\s*번호|전화번호|연락처", text)
    phone_alert = bool(phone_alert) and not bool(re.search(r"년|연도|월|일|시|분", text))
    if phone_alert:
        for name in sorted(inputs_meta.keys()):
            low = name.lower()
            if any(k in low for k in ("hp", "phone", "mobile", "tel", "cell")):
                info = inputs_meta.get(name, {}) or {}
                maxlen = _safe_maxlen(info)
                iid = str(info.get("id") or "")
                v = generate_tel_digits(maxlen, pattern=info.get("pattern"), name=name, iid=iid)

                cur = str(vals.get(name, "") or "").strip()
                if cur == v:
                    for _ in range(5):
                        alt = generate_tel_digits(maxlen, pattern=info.get("pattern"), name=name, iid=iid)
                        if alt != cur:
                            v = alt
                            break

                if set_value(page, f'[name="{name}"]', v):
                    changed.append(f"{name}={v}(alert:phone)")
                    vals[name] = v
                    quick_changed = True
                    break

    # 2) 빠른 수정이 전혀 안 먹었을 때만 전체 fallback
    if not changed:
        fallback_result = apply_next_constraints(page, meta, cfg, logger)
        changed.extend(list(fallback_result.get("changed") or []))
        if changed:
            vals = _refresh_vals()

    # 3) 마지막으로 다시 진단해서 남은 이슈를 범용 복구
    try:
        final_issues = diagnose_next_failures(page, diag_meta, logger)
    except Exception:
        final_issues = []
    if final_issues:
        final_changed = _repair_specific_issues(page, meta, cfg, final_issues, logger)
        if final_changed:
            changed.extend(final_changed)

    uniq_changed = _dedupe(changed)

    if uniq_changed:
        logger.info("[next_logic] alert_repair: " + " | ".join(uniq_changed))
    else:
        logger.info("[next_logic] alert_repair: no changes")

    return {"constraints": fallback_result.get("constraints", {}), "changed": uniq_changed}
