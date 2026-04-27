# server/asp_cases.py
from __future__ import annotations

import re
import random
from typing import Any, Optional, List, Tuple, Dict, Set


def extract_screen_guards_from_asp(asp_text: str) -> dict[str, Any]:
    """
    SCREEN 회피용 최소 가드 추출 (확장판)

    ✅ 확장 내용
      1) OR 조건을 "충돌 최소화" 방식으로 안전 처리:
         - OR의 각 파트를 "회피용 가드 후보"로 만든 뒤
         - g에 이미 있는 키와 충돌/모순이 적은 후보를 선택(가능하면 여러 개도 누적)
         - 충돌하면 해당 OR 후보는 스킵 (안전 우선)

      2) Request("X")="" 같은 빈값 비교 처리:
         - If Request("X") = "" Then SCREEN  => X != "" (보수값 "0"/"N" 등)
         - If Request("X") <> "" Then SCREEN => X = ""  (빈값으로 회피)

      3) getRedis/getValue/getMultiRedis 기반 varref 인식:
         - getValue("SQ1"), getRedis("SQ1")
         - dictVar("SQ1") where dictVar is from: Set dictVar = getMultiRedis("SQ1,SQ2,...")

      4) alias_map 확장:
         - alias = CLng(Request("X")) / CInt(Request("X")) / CDbl(Request("X"))
         - alias = Request("X") 도 연결
         - alias = getValue("X") / getRedis("X") 도 연결
         - alias = dictVar("X") 도 연결

    ⚠️ 원칙: "SCREEN으로 보내는 조건을 '거짓'으로 만들 값"을 제안한다.
    """
    from typing import Optional, Tuple, List

    if not asp_text or not asp_text.strip():
        return {}

    text = asp_text
    g: dict[str, Any] = {}

    # ------------------------------------------------------------
    # 0) getMultiRedis dict 변수 추적
    #   Set D = getMultiRedis("SQ1,SQ2,...")
    # ------------------------------------------------------------
    dict_vars: set[str] = set()
    for m in re.finditer(
        r'^\s*set\s+(\w+)\s*=\s*getMultiRedis\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        dict_vars.add(m.group(1).strip())

    # ------------------------------------------------------------
    # 1) alias_map 확장
    # ------------------------------------------------------------
    alias_map: dict[str, str] = {}  # alias -> underlying varname

    # a) alias = (CLng|CInt|CDbl)(Request("X"))
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(3).strip()

    # a-2) alias = (CLng|CInt|CDbl)(alias2)
    #     예: numD2 = CInt(D2) where D2 = Request("D2")  => numD2 -> "D2"
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        lhs = m.group(1).strip()
        inner = m.group(3).strip()
        if inner in alias_map:
            alias_map[lhs] = alias_map[inner]

    # b) alias = Request("X")
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(2).strip()

    # b-1) alias = Trim(Request("X"))  ✅ NEW
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*Trim\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(2).strip()

    # c) alias = getValue("X") / getRedis("X")
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(3).strip()

    # d) alias = dictVar("X") where dictVar in dict_vars
    for dv in dict_vars:
        for m in re.finditer(
            rf'^\s*([A-Za-z_]\w*)\s*=\s*{re.escape(dv)}\(\s*["\']([^"\']+)["\']\s*\)\s*$',
            text,
            flags=re.I | re.M
        ):
            alias_map[m.group(1).strip()] = m.group(2).strip()

    # ------------------------------------------------------------
    # 1-1) alias chain 해소(연쇄 대입/형변환) ✅ NEW
    #    numD2 = CInt(D2)  where D2 -> "D2"
    #    X = Y             where Y -> underlying
    # ------------------------------------------------------------

    # 1) alias = (CLng|CInt|CDbl)(<ident>)  where <ident> already mapped
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        a = m.group(1).strip()
        inner = m.group(3).strip()
        if inner in alias_map:
            alias_map[a] = alias_map[inner]

    # 2) alias = <ident>  where <ident> already mapped
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*$',
        text,
        flags=re.I | re.M
    ):
        a = m.group(1).strip()
        inner = m.group(2).strip()
        if inner in alias_map:
            alias_map[a] = alias_map[inner]

    # 3) transitive closure (A->B, B->C면 A->C로) - 안전하게 몇 번만 반복
    for _ in range(5):
        changed = False
        for a, b in list(alias_map.items()):
            if b in alias_map and alias_map[b] != b:
                nb = alias_map[b]
                if nb != b:
                    alias_map[a] = nb
                    changed = True
        if not changed:
            break
    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------
    def _strip_comment(s: str) -> str:
        return s.split("'", 1)[0] if "'" in s else s

    def _is_screen_line(s: str) -> bool:
        ss = (s or "").lower()
        if re.search(r'\bNEXTPAGE\b\s*=\s*["\'][^"\']*SCREEN[^"\']*["\']', s, flags=re.I):
            return True
        if "screen" in ss and ("nextpage" in ss or "nexpage" in ss or "npage" in ss):
            return True
        return False

    def _choose_not_equal(v: str) -> str:
        """
        'v 와 같지 않은 값'을 강제로 만들어야 할 때:
        - Y/N 은 뒤집어서 바로 리턴
        - 그 외(숫자/문자)는 실제 DOM을 보고 고를 수 있도록 NEQ 토큰을 리턴
        """
        if v is None:
            v = ""
        v = str(v)

        up = v.upper()
        if up in ("Y", "N"):
            return "N" if up == "Y" else "Y"

        # ✅ 실제 옵션 도메인은 Python(Playwright)에서 DOM을 보고 고르도록 토큰화
        return f"__NEQ__:{v}"
    
    def _parse_varref(lhs: str) -> Optional[Tuple[str, str]]:
        """
        lhs가 어떤 변수 참조인지 해석
        반환: ("str"|"num", varname)
        """
        s = (lhs or "").strip()

        # (CLng|CInt|CDbl)(Request("X"))
        m = re.match(r'(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$', s, flags=re.I)
        if m:
            return ("num", m.group(2).strip())

        # (CLng|CInt|CDbl)(getValue/getRedis("X"))
        m = re.match(r'(CLng|CInt|CDbl)\(\s*(getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$', s, flags=re.I)
        if m:
            return ("num", m.group(3).strip())

        # ✅ NEW: (CLng|CInt|CDbl)(alias) 형태 지원: CInt(A2) / CDbl(SQ1) ...
        m = re.match(r'(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$', s, flags=re.I)
        if m:
            inner = m.group(2).strip()
            if inner in alias_map:
                return ("num", alias_map[inner])  # alias -> 실제 Request 키
            return ("num", inner)

        # Request("X")
        m = re.match(r'Request\(\s*["\']([^"\']+)["\']\s*\)\s*$', s, flags=re.I)
        if m:
            return ("str", m.group(1).strip())

        # getValue/getRedis("X")
        m = re.match(r'(getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*$', s, flags=re.I)
        if m:
            return ("str", m.group(2).strip())

        # dictVar("X") where dictVar is getMultiRedis dict variable
        m = re.match(r'(\w+)\(\s*["\']([^"\']+)["\']\s*\)\s*$', s, flags=re.I)
        if m:
            dname = m.group(1).strip()
            key = m.group(2).strip()
            if dname in dict_vars:
                return ("str", key)

        # alias name
        m = re.match(r'^([A-Za-z_]\w*)\s*$', s)
        if m:
            a = m.group(1)
            if a in alias_map:
                return ("num", alias_map[a])  # 세팅 가능하도록 underlying var 사용
            return ("num", a)

        return None

    def _guard_for_string_cmp(var: str, op: str, val: str) -> Optional[Tuple[str, str]]:
        op = op.strip()
        if op in ("<>", "!="):
            return (var, val)
        if op == "=":
            return (var, _choose_not_equal(val))
        return None

    def _guard_for_numeric_cmp(var: str, op: str, n: int) -> Optional[Tuple[str, str]]:
        # 숫자 비교는 exact override를 만들지 않고
        # 아래 __NUM_CONSTRAINTS__ 로직에 맡긴다.
        return None

    re_str_cmp = re.compile(r'(.+?)\s*(=|<>|!=)\s*["\']([^"\']*)["\']', flags=re.I)
    re_num_cmp = re.compile(r'(.+?)\s*(<=|>=|<|>|=|<>|!=)\s*(\d+)\s*$', flags=re.I)

    def _guard_candidates_for_condition(cond: str) -> List[Tuple[str, str]]:
        if not cond:
            return []
        c = cond.strip()
        or_parts = re.split(r'\s+\bOr\b\s+', c, flags=re.I)

        candidates: List[Tuple[str, str]] = []
        for opart in or_parts:
            opart = opart.strip()
            if not opart:
                continue

            and_parts = re.split(r'\s+\bAnd\b\s+', opart, flags=re.I)
            first = (and_parts[0] or "").strip()
            if not first:
                continue

            m = re_num_cmp.search(first)
            if m:
                lhs = m.group(1).strip()
                op = m.group(2).strip()
                rhs = m.group(3).strip()
                vr = _parse_varref(lhs)
                if not vr:
                    continue
                kind, var = vr
                if kind != "num":
                    continue
                try:
                    n = int(rhs)
                except Exception:
                    continue
                gv = _guard_for_numeric_cmp(var, op, n)
                if gv:
                    candidates.append(gv)
                continue

            m = re_str_cmp.search(first)
            if m:
                lhs = m.group(1).strip()
                op = m.group(2).strip()
                rhs = m.group(3)
                vr = _parse_varref(lhs)
                if not vr:
                    continue
                _, var = vr
                gv = _guard_for_string_cmp(var, op, rhs)
                if gv:
                    candidates.append(gv)
                continue

        return candidates

    def _add_guard_safely(var: str, val: str) -> bool:
        if not var:
            return False
        if var in g:
            return str(g[var]) == str(val)
        g[var] = val
        return True

    def _apply_or_candidates(cands: List[Tuple[str, str]]):
        for (var, val) in cands:
            _add_guard_safely(var, val)

    # ------------------------------------------------------------
    # 2) If/ElseIf 체인에서 SCREEN 분기의 조건을 잡고 guard 생성
    # ------------------------------------------------------------
    lines = text.splitlines()
    in_chain = False
    cur_cond: Optional[str] = None
    cur_is_screen = False

    def _finalize_branch(cond: Optional[str]):
        if not cond:
            return

        # -----------------------------------------
        # [NEW] rank "must include any" rule extraction
        #   If Request("D3_1") <> "4" And Request("D3_2") <> "4" Then SCREEN
        #   => base="D3" must include "4" at least once
        # -----------------------------------------
        try:
            # Request("BASE_1") <> "V" 패턴을 모두 수집
            parts = re.findall(
                r'Request\(\s*["\']([A-Za-z0-9]+)_(\d+)["\']\s*\)\s*(<>|!=)\s*["\']([^"\']+)["\']',
                cond,
                flags=re.I
            )
            # parts: [(base, slot, op, value), ...]

            if parts:
                # base별, value별로 슬롯들을 모은다
                by_base_val: dict[tuple[str, str], set[int]] = {}
                for b, slot, op, v in parts:
                    b = b.strip()
                    v = str(v).strip()
                    try:
                        si = int(slot)
                    except Exception:
                        continue
                    by_base_val.setdefault((b, v), set()).add(si)

                # AND 조건에서 같은 base+value가 2개 이상(= 여러 슬롯에서 "v가 아니면")이면 must include
                # (보수적으로 2개 이상일 때만 적용)
                rank_rules = g.get("__RANK_INCLUDE_ANY__", {}) or {}
                if not isinstance(rank_rules, dict):
                    rank_rules = {}

                for (b, v), slots in by_base_val.items():
                    if len(slots) >= 2:
                        # must include any of [v]
                        cur = rank_rules.get(b, [])
                        if not isinstance(cur, list):
                            cur = [str(cur)]
                        if v not in cur:
                            cur.append(v)
                        rank_rules[b] = cur

                if rank_rules:
                    g["__RANK_INCLUDE_ANY__"] = rank_rules
        except Exception:
            pass

        # -----------------------------------------
        # [NEW] Numeric SCREEN constraints from conditions
        #   ex) CLng(Request("D6_1")) < 6   => D6_1 must be >= 6
        # -----------------------------------------
        try:
            # g에 제약을 저장할 공간
            cons = g.get("__NUM_CONSTRAINTS__", {})
            if not isinstance(cons, dict):
                cons = {}

            # 패턴1: (CLng|CInt|CDbl)(Request("X")) < N  => X >= N
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*<\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                name = m.group(2).strip()
                n = int(m.group(3))
                cur = cons.get(name, {})
                if not isinstance(cur, dict):
                    cur = {}
                # 최소값(>= n)
                cur["min"] = max(int(cur.get("min", -10**9)), n)
                cons[name] = cur

            # 패턴1-2: (CLng|CInt|CDbl)(localVar) < N  => localVar가 Request("X")로 매핑되면 X >= N
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*<\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                local_name = m.group(2).strip()
                real_name = alias_map.get(local_name)
                if not real_name:
                    continue

                n = int(m.group(3))
                cur = cons.get(real_name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["min"] = max(int(cur.get("min", -10**9)), n)
                cons[real_name] = cur

            # 패턴2: (CLng|CInt|CDbl)(Request("X")) <= N  => X >= N+1
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*<=\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                name = m.group(2).strip()
                n = int(m.group(3)) + 1
                cur = cons.get(name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["min"] = max(int(cur.get("min", -10**9)), n)
                cons[name] = cur

            # 패턴2-2: (CLng|CInt|CDbl)(localVar) <= N  => X >= N+1
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*<=\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                local_name = m.group(2).strip()
                real_name = alias_map.get(local_name)
                if not real_name:
                    continue

                n = int(m.group(3)) + 1
                cur = cons.get(real_name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["min"] = max(int(cur.get("min", -10**9)), n)
                cons[real_name] = cur

            # 패턴3: ... > N  => X <= N  (screen 조건을 반대로 읽지 않고,
            # "screen을 피하려면 <= N" 같은 형태로도 저장할 수 있음)
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*>\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                name = m.group(2).strip()
                n = int(m.group(3))
                cur = cons.get(name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["max"] = min(int(cur.get("max", 10**9)), n)
                cons[name] = cur

            # 패턴3-2: (CLng|CInt|CDbl)(localVar) > N  => X <= N
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*>\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                local_name = m.group(2).strip()
                real_name = alias_map.get(local_name)
                if not real_name:
                    continue

                n = int(m.group(3))
                cur = cons.get(real_name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["max"] = min(int(cur.get("max", 10**9)), n)
                cons[real_name] = cur

            # 패턴4: ... >= N  => X <= N-1
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*>=\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                name = m.group(2).strip()
                n = int(m.group(3)) - 1
                cur = cons.get(name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["max"] = min(int(cur.get("max", 10**9)), n)
                cons[name] = cur

            # 패턴4-2: (CLng|CInt|CDbl)(localVar) >= N  => X <= N-1
            for m in re.finditer(
                r'(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*>=\s*([0-9]+)',
                cond or "",
                flags=re.I
            ):
                local_name = m.group(2).strip()
                real_name = alias_map.get(local_name)
                if not real_name:
                    continue

                n = int(m.group(3)) - 1
                cur = cons.get(real_name, {})
                if not isinstance(cur, dict):
                    cur = {}
                cur["max"] = min(int(cur.get("max", 10**9)), n)
                cons[real_name] = cur

            if cons:
                g["__NUM_CONSTRAINTS__"] = cons
        except Exception:
            pass

        # 기존 단일가드 추출 로직
        cands = _guard_candidates_for_condition(cond)
        if cands:
            _apply_or_candidates(cands)

    for raw in lines:
        s0 = _strip_comment(raw).rstrip()
        st = s0.strip()

        m_if = re.match(r'^\s*If\s+(.+?)\s+Then\b', st, flags=re.I)
        if m_if:
            if in_chain and cur_is_screen:
                _finalize_branch(cur_cond)

            in_chain = True
            cur_cond = m_if.group(1).strip()
            cur_is_screen = False
            continue

        if in_chain:
            m_elseif = re.match(r'^\s*ElseIf\s+(.+?)\s+Then\b', st, flags=re.I)
            if m_elseif:
                if cur_is_screen:
                    _finalize_branch(cur_cond)
                cur_cond = m_elseif.group(1).strip()
                cur_is_screen = False
                continue

            m_else = re.match(r'^\s*Else\b', st, flags=re.I)
            if m_else:
                if cur_is_screen:
                    _finalize_branch(cur_cond)
                cur_cond = None
                cur_is_screen = False
                continue

            m_end = re.match(r'^\s*End\s+If\b', st, flags=re.I)
            if m_end:
                if cur_is_screen:
                    _finalize_branch(cur_cond)
                in_chain = False
                cur_cond = None
                cur_is_screen = False
                continue

            if _is_screen_line(st):
                cur_is_screen = True

    if in_chain and cur_is_screen:
        _finalize_branch(cur_cond)

    # ------------------------------------------------------------
    # 3) Select Case ... Case "X" ... If ... Then ... NEXTPAGE="SCREEN"
    #    패턴도 SCREEN 회피 guard로 추출
    # ------------------------------------------------------------
    cur_case: Optional[str] = None
    pending_if_cond: Optional[str] = None

    def _flush_pending_if():
        nonlocal pending_if_cond
        if pending_if_cond:
            # ✅ Select Case 내부의 If ... Then SCREEN 분기도
            #   일반 If/ElseIf 체인과 동일하게 처리 (rank/num 제약 포함)
            _finalize_branch(pending_if_cond)
        pending_if_cond = None

    for raw in lines:
        s0 = _strip_comment(raw).rstrip()
        st = s0.strip()

        # Case "A3"
        m_case = re.match(r'^\s*Case\s+["\']([^"\']+)["\']', st, flags=re.I)
        if m_case:
            # 이전 case에서 대기중이던 if 처리
            _flush_pending_if()
            cur_case = m_case.group(1).strip()
            continue

        # Case Else / End Select 만나면 case scope 종료
        if re.match(r'^\s*(Case\s+Else|End\s+Select)\b', st, flags=re.I):
            _flush_pending_if()
            cur_case = None
            continue

        if not cur_case:
            continue

        # Select Case 내부 If 조건 캡처
        m_if2 = re.match(r'^\s*If\s+(.+?)\s+Then\b', st, flags=re.I)
        if m_if2:
            # 이전 if가 아직 SCREEN인지 판단 못하고 남아있으면 flush
            _flush_pending_if()
            pending_if_cond = m_if2.group(1).strip()
            continue

        # If 라인이 한 줄짜리로 SCREEN이면 바로 처리 (ex: If ... Then NEXTPAGE="SCREEN")
        if pending_if_cond and _is_screen_line(st):
            # 이 If 조건이 SCREEN으로 이어지는 분기 => 조건을 "피하는 값"으로 guard 생성
            _flush_pending_if()
            continue

        # Select Case 내부 End If
        if pending_if_cond and re.match(r'^\s*End\s+If\b', st, flags=re.I):
            # End If까지 왔는데 SCREEN 라인이 없으면 버림
            pending_if_cond = None
            continue

    # ------------------------------------------------------------
    # ✅ NEW: cnt 기반 체크박스 최소선택 조건으로 SCREEN 회피
    #   예) For xx=1 To 8 ... cnt < 3 Then NEXTPAGE="SCREEN"
    #       => base(D9) 범위(1~8)에서 최소 3개 체크하도록 가드 생성
    # ------------------------------------------------------------
    try:
        rules = extract_checkbox_count_branch_rules(text)
        for base, rule in (rules or {}).items():
            branch_next = str(rule.get("branch_next", "") or "")
            if "SCREEN" not in branch_next.upper():
                continue

            a, b = rule.get("range", (None, None))
            k = int(rule.get("min", 0) or 0)

            if a is None or b is None:
                continue
            a = int(a)
            b = int(b)
            if a <= 0 or b < a or k <= 0:
                continue

            # 1) 범위 전체를 기본 해제값으로(명시적으로)
            for j in range(a, b + 1):
                key = f"{base}_{j}"
                # 이미 다른 가드가 잡아둔 값이 있더라도,
                # SCREEN 회피를 위해 일단 기본값을 채워둠(아래에서 필요한 값은 다시 체크)
                if key not in g:
                    g[key] = ""

            # 2) 최소 k개는 체크되도록 강제 (a부터 k개)
            end_j = min(b, a + k - 1)
            for j in range(a, end_j + 1):
                key = f"{base}_{j}"
                g[key] = str(j)

            # 3) none_values(예: 10 단독) 같은 게 있으면 우선 해제로 가드
            #    (보통 idx==val인 케이스가 많아서 base_10 형태로 잡아준다)
            for nv in (rule.get("none_values", []) or []):
                s_nv = str(nv)
                if s_nv.isdigit():
                    key = f"{base}_{int(s_nv)}"
                    g[key] = ""

    except Exception:
        # 가드 추출 실패해도 기존 g는 유지
        pass
    
    return g

# server/asp_cases.py 하단에 추가
def extract_checkbox_count_branch_rules(asp_text: str) -> dict[str, dict[str, Any]]:
    """
    패턴 예:
      For xx = 1 To 9
        E1 = Request("E1_"&CStr(xx))
        If CStr(E1) = CStr(xx) Then cnt = cnt + 1
      Next
      If cnt < 5 Then NEXTPAGE = "G1"
      If Request("E1_10") = "10" Then NEXTPAGE = "G1"

    => {"E1": {"range": (1,9), "min": 5, "none_values": ["10"], "branch_next": "G1"}}
    """
    if not asp_text or not asp_text.strip():
        return {}

    text = asp_text
    rules: dict[str, dict[str, Any]] = {}

    # Case "E1" 블록 단위로 잡는 게 가장 안정적
    # (다만 케이스 라벨이 없으면 전체에서 매칭)
    case_blocks = re.findall(r'Case\s+"([^"]+)"(.*?)(?=Case\s+"|End\s+Select|$)', text, flags=re.I | re.S)
    if not case_blocks:
        case_blocks = [("__ALL__", text)]

    for case_name, blk in case_blocks:
        # 1) For xx = a To b ... Request("BASE_"&CStr(xx)) ... cnt < k Then NEXTPAGE="X"
        m = re.search(
            r'For\s+\w+\s*=\s*(\d+)\s+To\s+(\d+).*?Request\(\s*"([A-Za-z]+\d+)_"\s*&\s*CStr\(\w+\)\s*\).*?'
            r'If\s+cnt\s*<\s*(\d+)\s+Then\s+NEXTPAGE\s*=\s*"([^"]+)"',
            blk,
            flags=re.I | re.S
        )
        if not m:
            continue

        a = int(m.group(1))
        b = int(m.group(2))
        base = m.group(3)  # E1 같은 베이스
        k = int(m.group(4))
        branch_next = m.group(5)

        rule = {"range": (a, b), "min": k, "none_values": [], "branch_next": branch_next}

        # 2) If Request("BASE_10")="10" Then NEXTPAGE="X" 형태의 none 값 수집
        for nm in re.finditer(
            rf'Request\(\s*"({re.escape(base)}_(\d+))"\s*\)\s*=\s*"(\d+)"\s*Then\s+NEXTPAGE\s*=\s*"({re.escape(branch_next)})"',
            blk,
            flags=re.I
        ):
            idx = nm.group(2)
            val = nm.group(3)
            # 보통 idx==val 이지만, 안전하게 val을 none_values로 저장
            rule["none_values"].append(val)

        # 중복 제거
        rule["none_values"] = sorted(list({v for v in rule["none_values"] if v}))

        rules[base] = rule

    return rules

def merge_case_with_guards(case: dict[str, Any], guards: dict[str, Any]) -> dict[str, Any]:
    """
    guards는 SCREEN 회피를 위한 최소 강제값.
    기본 원칙:
    - guards는 "없는 값만" 채운다.
    - case에 이미 명시된 키는 유지한다.

    이유:
    - later SCREEN target case(SQ2/SQ3 등)도 앞선 페이지(SQ0/SQ1)의 SCREEN 가드를
      함께 가져가야 중간 페이지에서 먼저 탈락하지 않는다.
    - 반대로, 현재 케이스가 의도적으로 지정한 값(예: target SCREEN 분기의 조건값)은
      guards가 덮어쓰면 안 된다.
    """
    merged = dict(case or {})
    for k, v in (guards or {}).items():
        if k not in merged:
            merged[k] = v
    return merged

def extract_conditional_numeric_rules(asp_text: str) -> list[dict[str, Any]]:
    """
    예:
        If (B8_1 = "2025" And CInt(B8_2) < 9) Or CInt(B8_1) < 2025 Then
            NEXTPAGE = "SCREEN"
        End If

    -> [{"when":{"B8_1":"2025"}, "target":"B8_2", "min":9}]
    """
    import re

    if not asp_text or not asp_text.strip():
        return []

    rules: list[dict[str, Any]] = []

    # Case 블록 단위 순회
    case_marks = list(re.finditer(r'^\s*Case\s+["\']([^"\']+)["\']\s*$', asp_text, flags=re.I | re.M))
    spans: list[tuple[int, int]] = []
    if case_marks:
        for i, m in enumerate(case_marks):
            s = m.start()
            e = case_marks[i + 1].start() if i + 1 < len(case_marks) else len(asp_text)
            spans.append((s, e))
    else:
        spans.append((0, len(asp_text)))

    for s, e in spans:
        blk = asp_text[s:e]

        # 1) If (X = "2025" And CInt(Y) < 9) Then ...
        for m in re.finditer(
            r'If\s*\(\s*([A-Za-z_]\w*)\s*=\s*"([^"]+)"\s+And\s+CInt\(\s*([A-Za-z_]\w*)\s*\)\s*<\s*(\d+)\s*\)',
            blk,
            flags=re.I | re.S,
        ):
            cond_field = m.group(1)
            cond_value = m.group(2)
            target = m.group(3)
            limit = int(m.group(4))
            rules.append({
                "when": {cond_field: cond_value},
                "target": target,
                "min": limit,
            })

        # 2) If (X = "2026" And CInt(Y) > 3) Then ...
        for m in re.finditer(
            r'If\s*\(\s*([A-Za-z_]\w*)\s*=\s*"([^"]+)"\s+And\s+CInt\(\s*([A-Za-z_]\w*)\s*\)\s*>\s*(\d+)\s*\)',
            blk,
            flags=re.I | re.S,
        ):
            cond_field = m.group(1)
            cond_value = m.group(2)
            target = m.group(3)
            limit = int(m.group(4))
            rules.append({
                "when": {cond_field: cond_value},
                "target": target,
                "max": limit,
            })

    return rules

def _extract_checkbox_count_branch_cases(asp_text: str) -> list[dict[str, Any]]:
    """
    Heuristic: Classic ASP patterns like:

        Case "E1"
            cnt = 0
            For xx = 1 To 9
                v = Request("E1_"&CStr(xx))
                If CStr(v) = CStr(xx) Then cnt = cnt + 1
            Next
            If cnt < 5 Then NEXTPAGE="G1"
            If Request("E1_10")="10" Then NEXTPAGE="G1"

    -> generate coverage-friendly cases:
      A) cnt < threshold   (pick threshold-1 among 1..N)
      B) cnt >= threshold  (pick threshold among 1..N)
      C) none option only  (e.g., E1_10)
    """
    import re
    from typing import Any

    if not asp_text or not asp_text.strip():
        return []

    out: list[dict[str, Any]] = []

    # Case "X" 블록 단위로 훑기 (없으면 전체 텍스트로 1회 시도)
    case_marks = list(re.finditer(r'^\s*Case\s+["\']([^"\']+)["\']\s*$', asp_text, flags=re.I | re.M))
    spans: list[tuple[int, int]] = []
    if case_marks:
        for i, m in enumerate(case_marks):
            s = m.start()
            e = case_marks[i + 1].start() if i + 1 < len(case_marks) else len(asp_text)
            spans.append((s, e))
    else:
        spans.append((0, len(asp_text)))

    for s, e in spans:
        block = asp_text[s:e]

        # For xx = 1 To N
        m_for = re.search(r'\bFor\s+\w+\s*=\s*1\s+To\s+(\d+)\b', block, flags=re.I)
        # Request("BASE_"&CStr(xx))
        m_req = re.search(r'Request\(\s*["\']([A-Za-z_]\w*)_\s*["\']\s*&\s*CStr\(\s*\w+\s*\)\s*\)', block, flags=re.I)
        # If cnt < K Then
        m_thr = re.search(r'\bIf\s+cnt\s*<\s*(\d+)\s+Then\b', block, flags=re.I)

        if not (m_for and m_req and m_thr):
            continue

        base = m_req.group(1).strip()
        try:
            n = int(m_for.group(1))
            thr = int(m_thr.group(1))
        except Exception:
            continue
        if n <= 0 or thr <= 0:
            continue

        # none option: Request("BASE_10")="10" 형태
        m_none = re.search(
            rf'Request\(\s*["\']{re.escape(base)}_(\d+)["\']\s*\)\s*=\s*["\'](\d+)["\']',
            block,
            flags=re.I
        )
        none_idx = None
        none_val = None
        if m_none:
            try:
                none_idx = int(m_none.group(1))
                none_val = str(int(m_none.group(2)))
            except Exception:
                none_idx, none_val = None, None

        # 케이스를 "결정론적으로" 만들기 위해 1..N 및 none_idx까지 명시적으로 uncheck 세팅
        def build_case(picks: list[int], force_none: bool) -> dict[str, Any]:
            c: dict[str, Any] = {}

            # 1..N 전체 uncheck
            for j in range(1, n + 1):
                c[f"{base}_{j}"] = ""  # falsy => overrides.py에서 UNCHECK 처리

            # picks만 체크
            for j in picks:
                if 1 <= j <= n:
                    c[f"{base}_{j}"] = str(j)

            # none 옵션
            if none_idx is not None:
                c[f"{base}_{none_idx}"] = (none_val or str(none_idx)) if force_none else ""

            return c

        # A) cnt < thr  => thr-1개 선택
        low_k = max(0, min(n, thr - 1))
        out.append(build_case(list(range(1, low_k + 1)), force_none=False))

        # B) cnt >= thr => thr개 선택
        high_k = max(1, min(n, thr))
        out.append(build_case(list(range(1, high_k + 1)), force_none=False))

        # C) none 단독
        if none_idx is not None:
            out.append(build_case([], force_none=True))

    # 중복 제거
    uniq: list[dict[str, Any]] = []
    seen: set[str] = set()
    for c in out:
        k = "|".join([f"{kk}={c[kk]}" for kk in sorted(c.keys())])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(c)
    return uniq

def extract_cases_from_asp(
    asp_text: str,
    max_cases: int = 50,
    include_default_paths: bool = True,
    include_screen_cases: bool = False,
) -> list[dict[str, Any]]:
    """
    '케이스 후보'만 추출:
    - OR는 케이스 분기
    - AND는 같은 케이스에 묶음
    - include_screen_cases=False 이면 SCREEN 분기는 제외하고 guards로 통과 유도
    - include_screen_cases=True 이면 SCREEN 분기도 별도 케이스로 추가
    - getValue/getRedis/dict(getMultiRedis)는 varref로 인식
    - alias(예: Q17 = getValue("Q_17"))도 varref로 인식
    """
    if not asp_text or not asp_text.strip():
        return []

    text = asp_text

    # getMultiRedis 추적: set dict = getMultiRedis("SQ1,SQ2,...")
    multi_decl = re.findall(
        r'set\s+(\w+)\s*=\s*getMultiRedis\(\s*["\']([^"\']+)["\']\s*\)',
        text,
        flags=re.I
    )
    dict_vars: set[str] = set()
    for dict_name, _vars_csv in multi_decl:
        dict_vars.add(dict_name)

    # ------------------------------------------------------------
    # alias_map (딱 1번만!)
    #   Q17 = getValue("Q_17")  ->  Q17 => Q_17
    # ------------------------------------------------------------
    alias_map: dict[str, str] = {}

    for am in re.finditer(
        r'([A-Za-z_]\w*)\s*=\s*Request\(\s*["\']([^"\']+)["\']\s*\)',
        text,
        flags=re.I,
    ):
        local_var = am.group(1).strip()
        req_name = am.group(2).strip()
        alias_map[local_var] = req_name
        
    # a) alias = Request("X")
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(2).strip()

    # b) alias = getValue("X") / getRedis("X")
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(3).strip()

    # c) alias = dictVar("X") where dictVar from getMultiRedis
    for dv in dict_vars:
        for m in re.finditer(
            rf'^\s*([A-Za-z_]\w*)\s*=\s*{re.escape(dv)}\(\s*["\']([^"\']+)["\']\s*\)\s*$',
            text,
            flags=re.I | re.M
        ):
            alias_map[m.group(1).strip()] = m.group(2).strip()

    # d) alias = CLng(Request("X")) / CInt / CDbl
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(3).strip()

    # e) alias = CLng(getValue("X")) / CInt / CDbl
    for m in re.finditer(
        r'^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*(getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        text,
        flags=re.I | re.M
    ):
        alias_map[m.group(1).strip()] = m.group(4).strip()

    def parse_varref(expr: str) -> str | None:
        expr = expr.strip()

        # CLng/CInt/CDbl(Request("X"))
        m = re.match(r'(CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$', expr, flags=re.I)
        if m:
            return m.group(2).strip()

        # CLng/CInt/CDbl(getValue/getRedis("X"))
        m = re.match(r'(CLng|CInt|CDbl)\(\s*(getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$', expr, flags=re.I)
        if m:
            return m.group(3).strip()

        # CLng/CInt/CDbl(localAlias) where localAlias = Request("X")
        m = re.match(r'(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$', expr, flags=re.I)
        if m:
            local_name = m.group(2).strip()
            if local_name in alias_map:
                return alias_map[local_name]

        m = re.match(r'Request\(\s*["\']([^"\']+)["\']\s*\)$', expr, flags=re.I)
        if m:
            return m.group(1).strip()

        m = re.match(r'getValue\(\s*["\']([^"\']+)["\']\s*\)$', expr, flags=re.I)
        if m:
            return m.group(1).strip()

        m = re.match(r'getRedis\(\s*["\']([^"\']+)["\']\s*\)$', expr, flags=re.I)
        if m:
            return m.group(1).strip()

        # dictVar("X") where dictVar in dict_vars
        m = re.match(r'(\w+)\(\s*["\']([^"\']+)["\']\s*\)$', expr, flags=re.I)
        if m:
            dname = m.group(1)
            key = m.group(2)
            if dname in dict_vars:
                return key.strip()

        # alias variable (e.g., Q17) -> underlying question key (e.g., Q_17)
        m = re.match(r'^([A-Za-z_]\w*)$', expr)
        if m:
            name = m.group(1).strip()
            if name in alias_map:
                return alias_map[name]

        return None

    # 비교식: <varref> (=|<>|!=) "value"
    cmp_re = re.compile(r'(.+?)\s*(=|<>|!=)\s*["\']([^"\']+)["\']', flags=re.I)

    def parse_comparison(part: str):
        m = cmp_re.search(part.strip())
        if not m:
            return None
        left = m.group(1).strip()
        op = m.group(2).strip()
        val = m.group(3).strip()

        var = parse_varref(left)
        if not var:
            return None
        return (var, op, val)

    # If/ElseIf/Else 체인 파싱
    lines = text.splitlines()
    chains: list[list[dict[str, Any]]] = []
    cur_chain: list[dict[str, Any]] = []
    cur_branch: Optional[dict[str, Any]] = None
    in_chain = False

    def _finalize_branch(b: dict[str, Any]):
        head_text = (b.get("head", "") or "")
        body_text = "\n".join(b.get("body", []))
        full_text = head_text + "\n" + body_text

        # SCREEN 판정: head+body 전체에서 탐지 (한 줄짜리 If ... Then NEXTPAGE="SCREEN" 도 잡힘)
        b["is_screen"] = bool(
            re.search(r'\bNEXTPAGE\b\s*=\s*["\'][^"\']*SCREEN[^"\']*["\']', full_text, flags=re.I)
        )

    for raw in lines:
        st = raw.strip()

        m_if = re.search(r'\bIf\s+(.+?)\s+Then\b', st, flags=re.I)
        if m_if:
            if cur_chain:
                if cur_branch:
                    _finalize_branch(cur_branch)
                chains.append(cur_chain)
            cur_chain = []
            cur_branch = {"kind": "IF", "cond": m_if.group(1).strip(), "head": st, "body": [], "is_screen": False}
            cur_chain.append(cur_branch)
            in_chain = True
            continue

        if in_chain:
            m_elseif = re.search(r'\bElseIf\s+(.+?)\s+Then\b', st, flags=re.I)
            if m_elseif:
                if cur_branch:
                    _finalize_branch(cur_branch)
                cur_branch = {"kind": "ELSEIF", "cond": m_elseif.group(1).strip(), "head": st, "body": [], "is_screen": False}
                cur_chain.append(cur_branch)
                continue

            m_else = re.search(r'\bElse\b', st, flags=re.I)
            if m_else:
                if cur_branch:
                    _finalize_branch(cur_branch)
                cur_branch = {"kind": "ELSE", "cond": "", "head": st, "body": [], "is_screen": False}
                cur_chain.append(cur_branch)
                continue

            m_end = re.search(r'\bEnd\s+If\b', st, flags=re.I)
            if m_end:
                if cur_branch:
                    _finalize_branch(cur_branch)
                chains.append(cur_chain)
                cur_chain = []
                cur_branch = None
                in_chain = False
                continue

            if cur_branch is not None:
                cur_branch["body"].append(st)

    if cur_chain:
        if cur_branch:
            _finalize_branch(cur_branch)
        chains.append(cur_chain)

    def split_or(cond: str) -> list[str]:
        parts = re.split(r'\s+\bOr\b\s+', cond, flags=re.I)
        return [p.strip() for p in parts if p.strip()]

    def split_and(cond: str) -> list[str]:
        parts = re.split(r'\s+\bAnd\b\s+', cond, flags=re.I)
        return [p.strip() for p in parts if p.strip()]

    # 도메인 후보(부정 조건 대응)
    domain: dict[str, list[str]] = {}
    for m in re.finditer(
        r'(Request|getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*(=|<>|!=)\s*["\']([^"\']+)["\']',
        text,
        flags=re.I
    ):
        var = m.group(2).strip()
        op = m.group(3).strip()
        val = m.group(4).strip()
        if op == "=":
            domain.setdefault(var, [])
            if val not in domain[var]:
                domain[var].append(val)

    # alias 비교식도 domain에 반영: If Q17 = "1" Then  (Q17 -> Q_17)
    if alias_map:
        for m in re.finditer(
            r'^\s*([A-Za-z_]\w*)\s*(=|<>|!=)\s*["\']([^"\']+)["\']',
            text,
            flags=re.I | re.M
        ):
            lhs = m.group(1).strip()
            op = m.group(2).strip()
            val = m.group(3).strip()
            if lhs not in alias_map:
                continue
            var = alias_map[lhs]
            if op == "=":
                domain.setdefault(var, [])
                if val not in domain[var]:
                    domain[var].append(val)

    # dictVar("X") 비교도 domain에 반영
    for dname in dict_vars:
        for m in re.finditer(
            rf'{re.escape(dname)}\(\s*["\']([^"\']+)["\']\s*\)\s*(=|<>|!=)\s*["\']([^"\']+)["\']',
            text,
            flags=re.I
        ):
            var = m.group(1).strip()
            op = m.group(2).strip()
            val = m.group(3).strip()
            if op == "=":
                domain.setdefault(var, [])
                if val not in domain[var]:
                    domain[var].append(val)

    # 라인 단위 조건식 재파싱:
    #   If B2 = "2" Or B2 = "6" Or ... 형태에서 첫 비교만 잡히는 문제를 보완
    for raw in lines:
        st = (raw or "").strip()
        if not st:
            continue

        m_line = re.match(r'^(If|ElseIf)\s+(.+?)\s+Then(?:\s+.*)?$', st, flags=re.I)
        if not m_line:
            continue

        cond_text = (m_line.group(2) or "").strip()
        if not cond_text:
            continue

        for or_part in split_or(cond_text):
            for and_part in split_and(or_part):
                cmp1 = parse_comparison(and_part)
                if not cmp1:
                    continue
                var, op, val = cmp1
                if op == "=":
                    domain.setdefault(var, [])
                    if val not in domain[var]:
                        domain[var].append(val)

    default_candidates = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Y", "N", "99", "A", "B"]

    def _dedupe_keep_order(seq: list[str]) -> list[str]:
        out: list[str] = []
        seen: set[str] = set()
        for x in seq:
            sx = str(x)
            if sx in seen:
                continue
            seen.add(sx)
            out.append(sx)
        return out

    def _infer_missing_numeric_values(var: str, excluded: set[str]) -> list[str]:
        seen_vals = _dedupe_keep_order(domain.get(var, []))
        if not seen_vals:
            return []

        nums: list[int] = []
        for v in seen_vals:
            if not re.fullmatch(r'-?\d+', str(v)):
                return []
            try:
                nums.append(int(v))
            except Exception:
                return []

        if not nums:
            return []

        lo = min(nums)
        hi = max(nums)
        span = hi - lo + 1
        if span <= 1 or span > 30:
            return []

        missing: list[str] = []
        for n in range(lo, hi + 1):
            sv = str(n)
            if sv not in seen_vals and sv not in excluded:
                missing.append(sv)

        if not missing and lo > 1:
            sv = str(lo - 1)
            if sv not in excluded:
                missing.append(sv)

        return missing

    def choose_value_for_neq(var: str, excluded: set[str]) -> str:
        cands = _dedupe_keep_order(
            _infer_missing_numeric_values(var, excluded) + domain.get(var, []) + default_candidates
        )
        for v in cands:
            if v not in excluded:
                return v
        for v in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if v not in excluded:
                return v
        return "1"

    def choose_values_for_default_false(var: str, excluded: set[str], max_values: int = 3) -> list[str]:
        cands = _dedupe_keep_order(
            _infer_missing_numeric_values(var, excluded) + domain.get(var, []) + default_candidates
        )
        out: list[str] = []
        for v in cands:
            if v in excluded:
                continue
            out.append(v)
            if len(out) >= max_values:
                break
        if not out:
            for v in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if v not in excluded:
                    out.append(v)
                    break
        if not out:
            out.append("1")
        return out

    def parse_numeric_comparison(part: str):
        s = (part or "").strip()
        m = re.search(r'(.+?)\s*(<=|>=|<|>)\s*(-?\d+)\s*$', s, flags=re.I)
        if not m:
            return None
        left = (m.group(1) or "").strip()
        op = m.group(2).strip()
        try:
            num = int(m.group(3))
        except Exception:
            return None
        var = parse_varref(left)
        if not var:
            return None
        return (var, op, num)

    def build_screen_case_from_cond(cond: str) -> dict[str, Any] | None:
        if not cond:
            return None

        out: dict[str, Any] = {"__TARGET_IS_SCREEN__": True}
        num_cons: dict[str, dict[str, int]] = {}
        ok = False

        or_parts = split_or(cond) if cond else []
        target_part = or_parts[0].strip() if or_parts else (cond or "").strip()
        if not target_part:
            return None

        for a in split_and(target_part):
            cmp1 = parse_comparison(a)
            if cmp1:
                var, op, val = cmp1
                ok = True
                if op == "=":
                    out[var] = val
                else:
                    out[var] = choose_value_for_neq(var, {val})
                continue

            ncmp = parse_numeric_comparison(a)
            if ncmp:
                var, op, num = ncmp
                ok = True
                cur = num_cons.get(var, {})
                if op == "<":
                    cur["max"] = min(int(cur.get("max", 10**9)), num - 1)
                elif op == "<=":
                    cur["max"] = min(int(cur.get("max", 10**9)), num)
                elif op == ">":
                    cur["min"] = max(int(cur.get("min", -10**9)), num + 1)
                elif op == ">=":
                    cur["min"] = max(int(cur.get("min", -10**9)), num)
                num_cons[var] = cur
                continue

        cleaned_num_cons: dict[str, dict[str, int]] = {}
        for var, rule in num_cons.items():
            rr: dict[str, int] = {}
            if "min" in rule and int(rule["min"]) > -10**9:
                rr["min"] = int(rule["min"])
            if "max" in rule and int(rule["max"]) < 10**9:
                rr["max"] = int(rule["max"])
            if rr:
                cleaned_num_cons[var] = rr

        if cleaned_num_cons:
            out["__NUM_CONSTRAINTS__"] = cleaned_num_cons

        if not ok:
            return None
        return out

    def extract_select_case_screen_cases() -> list[dict[str, Any]]:
        """
        Select Case 내부의 SCREEN 분기를 별도 케이스로 복원한다.

        일반 체인 파서만으로는
        - Case 블록 내부의 local alias
        - block style / one-line style 혼용
        - ElseIf 체인과 중첩된 경우
        를 놓칠 수 있어, Case 블록을 한 번 더 훑어 SCREEN 조건만 보강 추출한다.
        """
        out: list[dict[str, Any]] = []

        case_iter = list(re.finditer(r"^\s*Case\s+[\"']([^\"']+)[\"']\s*$", text, flags=re.I | re.M))
        if not case_iter:
            return out

        spans: list[tuple[int, int]] = []
        for i, m in enumerate(case_iter):
            s = m.start()
            e = case_iter[i + 1].start() if i + 1 < len(case_iter) else len(text)
            spans.append((s, e))

        def _is_screen_text(s: str) -> bool:
            return bool(re.search(r"\bNEXTPAGE\b\s*=\s*[\"'][^\"']*SCREEN[^\"']*[\"']", s or '', flags=re.I))

        def _case_local_alias_map(block: str) -> dict[str, str]:
            local_map: dict[str, str] = {}

            pats = [
                r"^\s*([A-Za-z_]\w*)\s*=\s*Request\(\s*[\"']([^\"']+)[\"']\s*\)\s*$",
                r"^\s*([A-Za-z_]\w*)\s*=\s*Trim\(\s*Request\(\s*[\"']([^\"']+)[\"']\s*\)\s*\)\s*$",
                r"^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*Request\(\s*[\"']([^\"']+)[\"']\s*\)\s*\)\s*$",
                r"^\s*([A-Za-z_]\w*)\s*=\s*(getValue|getRedis)\(\s*[\"']([^\"']+)[\"']\s*\)\s*$",
                r"^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*(getValue|getRedis)\(\s*[\"']([^\"']+)[\"']\s*\)\s*\)\s*$",
            ]
            for line in block.splitlines():
                st = line.strip()
                if not st:
                    continue
                m = re.match(pats[0], st, flags=re.I)
                if m:
                    local_map[m.group(1).strip()] = m.group(2).strip()
                    continue
                m = re.match(pats[1], st, flags=re.I)
                if m:
                    local_map[m.group(1).strip()] = m.group(2).strip()
                    continue
                m = re.match(pats[2], st, flags=re.I)
                if m:
                    local_map[m.group(1).strip()] = m.group(3).strip()
                    continue
                m = re.match(pats[3], st, flags=re.I)
                if m:
                    local_map[m.group(1).strip()] = m.group(3).strip()
                    continue
                m = re.match(pats[4], st, flags=re.I)
                if m:
                    local_map[m.group(1).strip()] = m.group(4).strip()
                    continue

            for _ in range(5):
                changed = False
                for line in block.splitlines():
                    st = line.strip()
                    m = re.match(r'^\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*$', st, flags=re.I)
                    if not m:
                        m = re.match(r'^\s*([A-Za-z_]\w*)\s*=\s*(CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$', st, flags=re.I)
                        if not m:
                            continue
                        lhs = m.group(1).strip()
                        rhs = m.group(3).strip()
                    else:
                        lhs = m.group(1).strip()
                        rhs = m.group(2).strip()
                    if rhs in local_map and local_map.get(lhs) != local_map[rhs]:
                        local_map[lhs] = local_map[rhs]
                        changed = True
                if not changed:
                    break

            return local_map

        def _replace_local_aliases(cond: str, local_map: dict[str, str]) -> str:
            if not cond or not local_map:
                return cond
            out_cond = cond
            for alias, real in sorted(local_map.items(), key=lambda x: -len(x[0])):
                out_cond = re.sub(rf'(?<![A-Za-z0-9_]){re.escape(alias)}(?![A-Za-z0-9_])', real, out_cond)
            return out_cond

        def _dedup_append(case_obj: dict[str, Any] | None):
            if not case_obj:
                return
            out.append(case_obj)

        for s, e in spans:
            block = text[s:e]
            local_alias_map = _case_local_alias_map(block)
            pending_cond: Optional[str] = None

            for raw in block.splitlines():
                st = raw.strip()
                if not st:
                    continue

                m_inline = re.match(r'^\s*(If|ElseIf)\s+(.+?)\s+Then\s+(.+?)\s*$', st, flags=re.I)
                if m_inline:
                    cond = (m_inline.group(2) or '').strip()
                    tail = (m_inline.group(3) or '').strip()
                    if _is_screen_text(tail):
                        _dedup_append(build_screen_case_from_cond(_replace_local_aliases(cond, local_alias_map)))
                    pending_cond = None
                    continue

                m_if = re.match(r'^\s*(If|ElseIf)\s+(.+?)\s+Then\s*$', st, flags=re.I)
                if m_if:
                    pending_cond = (m_if.group(2) or '').strip()
                    continue

                if pending_cond and _is_screen_text(st):
                    _dedup_append(build_screen_case_from_cond(_replace_local_aliases(pending_cond, local_alias_map)))
                    pending_cond = None
                    continue

                if re.match(r'^\s*End\s+If\b', st, flags=re.I):
                    pending_cond = None
                    continue

        return out

    cases: list[dict[str, Any]] = []

    cases.extend(_extract_checkbox_count_branch_cases(text))

    if include_screen_cases:
        cases.extend(extract_select_case_screen_cases())

    for chain in chains:
        branch_eq_seen: dict[str, set[str]] = {}
        screen_eq_seen: dict[str, set[str]] = {}

        for branch in chain:
            kind = branch["kind"]
            cond = branch.get("cond", "")
            is_screen = bool(branch.get("is_screen", False))

            # SCREEN 분기 처리
            # - include_screen_cases=False: guards로 우회
            # - include_screen_cases=True : SCREEN 도 별도 응답 케이스로 추가
            # 또한 이후 ELSE / default(false) path 생성 시 SCREEN 값이 섞이지 않도록
            # SCREEN 분기에서 등장한 '=' 값은 별도로 누적해 둔다.
            if is_screen:
                if kind in ("IF", "ELSEIF"):
                    or_parts = split_or(cond) if cond else []
                    for or_part in or_parts:
                        and_parts = split_and(or_part)
                        for a in and_parts:
                            cmp1 = parse_comparison(a)
                            if not cmp1:
                                continue
                            var, op, val = cmp1
                            if op == "=":
                                screen_eq_seen.setdefault(var, set()).add(val)

                if include_screen_cases and kind in ("IF", "ELSEIF"):
                    sc = build_screen_case_from_cond(cond)
                    if sc:
                        cases.append(sc)
                continue

            if kind in ("IF", "ELSEIF"):
                or_parts = split_or(cond) if cond else []
                for or_part in or_parts:
                    and_parts = split_and(or_part)

                    eq: dict[str, str] = {}
                    neq: dict[str, set[str]] = {}
                    ok = False

                    for a in and_parts:
                        cmp1 = parse_comparison(a)
                        if not cmp1:
                            continue
                        var, op, val = cmp1
                        ok = True
                        if op == "=":
                            eq[var] = val
                            branch_eq_seen.setdefault(var, set()).add(val)
                        else:
                            neq.setdefault(var, set()).add(val)

                    if not ok:
                        continue

                    # 1) TRUE path 케이스: neq를 만족하도록 값 선택
                    for v, ex in neq.items():
                        if v not in eq:
                            eq[v] = choose_value_for_neq(v, ex)

                    if eq:
                        cases.append(eq)

                    # 2) DEFAULT(FALSE) path 케이스 생성
                    #    - 기존: neq가 있을 때만 생성
                    #    - 수정: eq만 있는 분기(예: If C5="2" Then)도 FALSE path를 만든다.
                    if include_default_paths:
                        default_case: dict[str, str] | None = None

                        if neq:
                            v0 = next(iter(neq.keys()))
                            ex0 = neq[v0]
                            if ex0:
                                val0 = next(iter(ex0))
                                default_case = dict(eq)
                                default_case[v0] = val0
                                cases.append(default_case)

                        elif eq:
                            v0 = next(iter(eq.keys()))
                            # default(false) path는 현재 분기값만 피하면 안 되고,
                            # 앞선 SCREEN 분기값도 함께 피해야 안전하다.
                            ex0 = {str(eq[v0])} | set(screen_eq_seen.get(v0, set()))
                            for val0 in choose_values_for_default_false(v0, ex0, max_values=4):
                                default_case = dict(eq)
                                default_case[v0] = val0
                                cases.append(default_case)

                        # neq 분기는 위에서 바로 append, eq-only 분기는 후보 여러 개 append

            elif kind == "ELSE":
                base_case: dict[str, str] = {}
                multi_choices: list[tuple[str, list[str]]] = []
                for var, seen_vals in branch_eq_seen.items():
                    excluded = set(seen_vals) | set(screen_eq_seen.get(var, set()))
                    vals = choose_values_for_default_false(var, excluded, max_values=4)
                    if not vals:
                        continue
                    vals_copy = list(vals)
                    random.shuffle(vals_copy)
                    base_case[var] = vals_copy[0]
                    if len(vals_copy) > 1:
                        multi_choices.append((var, vals_copy))
                if base_case:
                    cases.append(dict(base_case))
                    for var, vals in multi_choices:
                        for vv in vals[1:]:
                            extra = dict(base_case)
                            extra[var] = vv
                            cases.append(extra)


    def _case_pairs(case_obj: dict[str, Any]) -> list[tuple[str, str]]:
        pairs: list[tuple[str, str]] = []
        for k, v in (case_obj or {}).items():
            if str(k).startswith("__"):
                continue
            pairs.append((str(k), str(v)))
        return pairs

    def _rebalance_case_order(case_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not case_list:
            return case_list

        from collections import Counter, defaultdict

        remaining = list(case_list)
        selected: list[dict[str, Any]] = []

        values_by_var: dict[str, list[str]] = defaultdict(list)
        global_freq: Counter[tuple[str, str]] = Counter()
        all_uncovered: set[tuple[str, str]] = set()

        for c in remaining:
            for var, val in set(_case_pairs(c)):
                if val not in values_by_var[var]:
                    values_by_var[var].append(val)
                global_freq[(var, val)] += 1
                all_uncovered.add((var, val))

        selected_freq: Counter[tuple[str, str]] = Counter()

        while remaining:
            best_idx = 0
            best_key = None

            for idx, c in enumerate(remaining):
                pairs = set(_case_pairs(c))
                if not pairs:
                    key = (10**9, 10**9, 10**9, 10**9, 10**9, idx)
                    if best_key is None or key < best_key:
                        best_key = key
                        best_idx = idx
                    continue

                balance_penalty = 0
                balance_bonus = 0
                repeat_penalty = 0
                rarity_bonus = 0.0
                new_cov = len(pairs & all_uncovered)

                for var, val in pairs:
                    cur = selected_freq[(var, val)]
                    repeat_penalty += cur
                    rarity_bonus += 1.0 / max(1, global_freq[(var, val)])

                    vals = values_by_var.get(var, [])
                    if vals:
                        var_counts = [selected_freq[(var, vv)] for vv in vals]
                        min_cnt = min(var_counts) if var_counts else 0
                        max_cnt = max(var_counts) if var_counts else 0
                        balance_penalty += cur - min_cnt
                        balance_bonus += max_cnt - cur

                key = (
                    balance_penalty,
                    -balance_bonus,
                    -new_cov,
                    repeat_penalty,
                    -rarity_bonus,
                    idx,
                )
                if best_key is None or key < best_key:
                    best_key = key
                    best_idx = idx

            picked = remaining.pop(best_idx)
            selected.append(picked)

            for p in set(_case_pairs(picked)):
                selected_freq[p] += 1
            all_uncovered.difference_update(set(_case_pairs(picked)))

        return selected

    # 중복 제거 + 제한
    uniq: list[dict[str, Any]] = []
    seen = set()
    for c in cases:
        key = tuple(sorted((k, str(v)) for k, v in c.items()))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(c)

    uniq = _rebalance_case_order(uniq)
    return uniq[:max_cases]


# ===== patched screen-guard enhancements =====
_legacy_extract_screen_guards_from_asp = extract_screen_guards_from_asp

def _patched_alias_map_for_screen_guards(asp_text: str) -> dict[str, str]:
    alias_map: dict[str, str] = {}
    text = asp_text or ""
    patterns = [
        r'^\s*([A-Za-z_]\w*)\s*=\s*(?:CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        r'^\s*([A-Za-z_]\w*)\s*=\s*Trim\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        r'^\s*([A-Za-z_]\w*)\s*=\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        r'^\s*([A-Za-z_]\w*)\s*=\s*(?:getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*$',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.I | re.M):
            alias_map[m.group(1).strip()] = m.group(2).strip()

    for _ in range(5):
        changed = False
        for m in re.finditer(r'^\s*([A-Za-z_]\w*)\s*=\s*(?:CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$', text, flags=re.I | re.M):
            lhs = m.group(1).strip()
            inner = m.group(2).strip()
            if inner in alias_map and alias_map.get(lhs) != alias_map[inner]:
                alias_map[lhs] = alias_map[inner]
                changed = True
        for m in re.finditer(r'^\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*$', text, flags=re.I | re.M):
            lhs = m.group(1).strip()
            inner = m.group(2).strip()
            if inner in alias_map and alias_map.get(lhs) != alias_map[inner]:
                alias_map[lhs] = alias_map[inner]
                changed = True
        if not changed:
            break

    return alias_map

def _patched_resolve_varref(expr: str, alias_map: dict[str, str]) -> str | None:
    s = (expr or "").strip()
    if not s:
        return None

    pats = [
        r'^(?:CLng|CInt|CDbl)\(\s*Request\(\s*["\']([^"\']+)["\']\s*\)\s*\)\s*$',
        r'^Request\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        r'^(?:getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)\s*$',
        r'^(?:CLng|CInt|CDbl)\(\s*([A-Za-z_]\w*)\s*\)\s*$',
        r'^([A-Za-z_]\w*)\s*$',
    ]
    for i, pat in enumerate(pats):
        m = re.match(pat, s, flags=re.I)
        if not m:
            continue
        key = m.group(1).strip()
        if i >= 3:
            return alias_map.get(key, key)
        return key
    return None

def _patched_split_bool_parts(expr: str, op_word: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    in_quote: str | None = None
    i = 0
    n = len(expr or "")
    target = op_word.lower()

    while i < n:
        ch = expr[i]
        if in_quote:
            buf.append(ch)
            if ch == in_quote:
                in_quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch == "(":
            depth += 1
            buf.append(ch)
            i += 1
            continue
        if ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
            i += 1
            continue

        if depth == 0:
            end = i + len(op_word)
            seg = (expr[i:end] or "")
            if seg.lower() == target:
                prev_ok = (i == 0) or (not (expr[i - 1].isalnum() or expr[i - 1] == "_"))
                next_ok = (end >= n) or (not (expr[end].isalnum() or expr[end] == "_"))
                if prev_ok and next_ok:
                    part = "".join(buf).strip()
                    if part:
                        parts.append(part)
                    buf = []
                    i = end
                    continue

        buf.append(ch)
        i += 1

    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts

def _patched_collect_or_equal_exclusions(asp_text: str) -> dict[str, set[str]]:
    text = asp_text or ""
    alias_map = _patched_alias_map_for_screen_guards(text)
    excluded: dict[str, set[str]] = {}
    pending_cond: str | None = None

    def handle_cond(cond: str) -> None:
        for or_part in _patched_split_bool_parts(cond or "", "Or"):
            and_parts = _patched_split_bool_parts(or_part, "And")
            for atom in and_parts:
                m = re.match(
                    r'^\s*(.+?)\s*(=|<>|!=|<=|>=|<|>)\s*(?:"([^"]*)"|\'([^\']*)\'|(-?\d+(?:\.\d+)?))\s*$',
                    atom.strip(),
                    flags=re.I,
                )
                if not m:
                    continue
                lhs = (m.group(1) or "").strip()
                op = (m.group(2) or "").strip()
                val = m.group(3)
                if val is None:
                    val = m.group(4)
                if val is None:
                    val = m.group(5)
                var = _patched_resolve_varref(lhs, alias_map)
                if not var:
                    continue
                if op == "=" and val is not None and val != "":
                    excluded.setdefault(var, set()).add(str(val).strip())

    for raw in text.splitlines():
        line = raw.split("'", 1)[0].strip()
        if not line:
            continue

        inline = re.match(r'^\s*(?:If|ElseIf)\s+(.+?)\s+Then\s+(.*)$', line, flags=re.I)
        if inline:
            cond = (inline.group(1) or "").strip()
            tail = (inline.group(2) or "").strip()
            if re.search(r'\bNEXTPAGE\b\s*=\s*["\']SCREEN["\']', tail, flags=re.I):
                handle_cond(cond)
                pending_cond = None
            else:
                pending_cond = cond
            continue

        begin_only = re.match(r'^\s*(?:If|ElseIf)\s+(.+?)\s+Then\s*$', line, flags=re.I)
        if begin_only:
            pending_cond = (begin_only.group(1) or "").strip()
            continue

        if pending_cond and re.search(r'\bNEXTPAGE\b\s*=\s*["\']SCREEN["\']', line, flags=re.I):
            handle_cond(pending_cond)
            pending_cond = None
            continue

        if re.match(r'^\s*End\s+If\b', line, flags=re.I):
            pending_cond = None

    return excluded

def _merge_neq_tokens(existing: str | None, excluded_vals: set[str]) -> str:
    vals = set(str(v).strip() for v in excluded_vals if str(v).strip() != "")
    if existing:
        cur = str(existing)
        if cur.startswith("__NEQSET__:"):
            vals.update(x.strip() for x in cur[len("__NEQSET__:"):].split(",") if x.strip() != "")
        elif cur.startswith("__NEQ__:"):
            x = cur[len("__NEQ__:"):].strip()
            if x:
                vals.add(x)
    vals = {v for v in vals if v}
    if not vals:
        return existing or ""
    def _sort_key(v: str):
        return (0, int(v)) if v.isdigit() else (1, v)
    sorted_vals = sorted(vals, key=_sort_key)
    if len(sorted_vals) == 1:
        return "__NEQ__:" + sorted_vals[0]
    return "__NEQSET__:" + ",".join(sorted_vals)


_extract_screen_guards_from_asp_base = extract_screen_guards_from_asp


def _enhance_nested_numeric_screen_guards(asp_text: str, guards: dict[str, Any]) -> dict[str, Any]:
    text = str(asp_text or "")
    if not text.strip():
        return guards

    g = dict(guards or {})

    try:
        alias_map = _patched_alias_map_for_screen_guards(text)
    except Exception:
        alias_map = {}

    try:
        raw_num = g.get("__NUM_CONSTRAINTS__", {}) or {}
        num_cons: dict[str, dict[str, int]] = {str(k): dict(v) for k, v in raw_num.items() if isinstance(v, dict)}
    except Exception:
        num_cons = {}

    try:
        raw_rules = g.get("__COND_NUM_RULES__", []) or []
        cond_rules: list[dict[str, Any]] = [dict(x) for x in raw_rules if isinstance(x, dict)]
    except Exception:
        cond_rules = []

    seen_rule_keys: set[tuple[Any, ...]] = set()
    for rule in cond_rules:
        when = rule.get("when") or {}
        if not isinstance(when, dict):
            continue
        key = (
            tuple(sorted((str(k), str(v)) for k, v in when.items())),
            str(rule.get("target") or "").strip(),
            rule.get("min"),
            rule.get("max"),
        )
        seen_rule_keys.add(key)

    def resolve_var(expr: str) -> Optional[str]:
        s = str(expr or "").strip()
        if not s:
            return None
        changed = True
        while changed:
            changed = False
            m_wrap = re.match(r'^(?:CStr|CLng|CInt|CDbl|Trim)\(\s*(.+?)\s*\)$', s, flags=re.I)
            if m_wrap:
                s = (m_wrap.group(1) or "").strip()
                changed = True
        m = re.match(r'^Request\(\s*["\']([^"\']+)["\']\s*\)$', s, flags=re.I)
        if m:
            return m.group(1).strip()
        m = re.match(r'^(?:getValue|getRedis)\(\s*["\']([^"\']+)["\']\s*\)$', s, flags=re.I)
        if m:
            return m.group(1).strip()
        m = re.match(r'^([A-Za-z_]\w*)$', s)
        if m:
            name = m.group(1).strip()
            return alias_map.get(name, name)
        return None

    def split_bool(text_value: str, token: str) -> list[str]:
        try:
            return _patched_split_bool_parts(text_value, token)
        except Exception:
            parts = re.split(rf'\s+\b{re.escape(token)}\b\s+', str(text_value or ""), flags=re.I)
            return [p.strip() for p in parts if p.strip()]

    def add_global_bound(var: str, mn: Optional[int] = None, mx: Optional[int] = None) -> None:
        slot = num_cons.get(var, {}) or {}
        if mn is not None:
            slot["min"] = max(int(slot.get("min", -10**9)), int(mn))
        if mx is not None:
            slot["max"] = min(int(slot.get("max", 10**9)), int(mx))
        if "min" in slot and "max" in slot and int(slot["min"]) > int(slot["max"]):
            slot["max"] = int(slot["min"])
        num_cons[var] = slot

    def add_cond_rule(when: dict[str, str], target: str, mn: Optional[int] = None, mx: Optional[int] = None) -> None:
        if not when or not target or (mn is None and mx is None):
            return
        rule: dict[str, Any] = {
            "when": {str(k): str(v) for k, v in when.items()},
            "target": str(target),
        }
        if mn is not None:
            rule["min"] = int(mn)
        if mx is not None:
            rule["max"] = int(mx)
        key = (
            tuple(sorted((str(k), str(v)) for k, v in rule["when"].items())),
            rule["target"],
            rule.get("min"),
            rule.get("max"),
        )
        if key in seen_rule_keys:
            return
        seen_rule_keys.add(key)
        cond_rules.append(rule)

    def process_active_conditions(active_conds: list[str]) -> None:
        if not active_conds:
            return
        whens: dict[str, str] = {}
        bounds: list[tuple[str, Optional[int], Optional[int]]] = []

        for cond in active_conds:
            or_parts = split_bool(cond, "Or")
            if len(or_parts) != 1:
                continue
            for atom in split_bool(or_parts[0], "And"):
                part = str(atom or "").strip().strip("()").strip()
                if not part:
                    continue
                m_eq = re.match(r'^(.+?)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(-?\d+))\s*$', part, flags=re.I)
                if m_eq:
                    lhs = (m_eq.group(1) or "").strip()
                    rhs = m_eq.group(2) if m_eq.group(2) is not None else (m_eq.group(3) if m_eq.group(3) is not None else m_eq.group(4))
                    var = resolve_var(lhs)
                    if var and rhs is not None and str(rhs).strip() != "":
                        whens[str(var)] = str(rhs).strip()
                    continue

                m_num = re.match(r'^(.+?)\s*(<|<=|>|>=)\s*(-?\d+)\s*$', part, flags=re.I)
                if not m_num:
                    continue
                lhs = (m_num.group(1) or "").strip()
                op = m_num.group(2)
                n = int(m_num.group(3))
                var = resolve_var(lhs)
                if not var:
                    continue
                mn: Optional[int] = None
                mx: Optional[int] = None
                if op == "<":
                    mn = n
                elif op == "<=":
                    mn = n + 1
                elif op == ">":
                    mx = n
                elif op == ">=":
                    mx = n - 1
                bounds.append((str(var), mn, mx))

        for var, mn, mx in bounds:
            if whens and var not in whens:
                add_cond_rule(whens, var, mn=mn, mx=mx)
            else:
                add_global_bound(var, mn=mn, mx=mx)

    stack: list[Optional[str]] = []

    for raw in text.splitlines():
        line = raw.split("'", 1)[0].rstrip()
        st = line.strip()
        if not st:
            continue

        m_inline_if = re.match(r'^\s*If\s+(.+?)\s+Then\s+(.*)$', st, flags=re.I)
        if m_inline_if:
            cond = (m_inline_if.group(1) or "").strip()
            tail = (m_inline_if.group(2) or "").strip()
            stack.append(cond)
            if re.search(r'\bNEXTPAGE\b\s*=\s*["\']SCREEN["\']', tail, flags=re.I):
                process_active_conditions([x for x in stack if x])
            stack.pop()
            continue

        m_if = re.match(r'^\s*If\s+(.+?)\s+Then\s*$', st, flags=re.I)
        if m_if:
            stack.append((m_if.group(1) or "").strip())
            continue

        m_inline_elseif = re.match(r'^\s*ElseIf\s+(.+?)\s+Then\s+(.*)$', st, flags=re.I)
        if m_inline_elseif:
            cond = (m_inline_elseif.group(1) or "").strip()
            tail = (m_inline_elseif.group(2) or "").strip()
            if stack:
                stack[-1] = cond
            else:
                stack.append(cond)
            if re.search(r'\bNEXTPAGE\b\s*=\s*["\']SCREEN["\']', tail, flags=re.I):
                process_active_conditions([x for x in stack if x])
            continue

        m_elseif = re.match(r'^\s*ElseIf\s+(.+?)\s+Then\s*$', st, flags=re.I)
        if m_elseif:
            cond = (m_elseif.group(1) or "").strip()
            if stack:
                stack[-1] = cond
            else:
                stack.append(cond)
            continue

        if re.match(r'^\s*Else\b', st, flags=re.I):
            if stack:
                stack[-1] = None
            continue

        if re.match(r'^\s*End\s+If\b', st, flags=re.I):
            if stack:
                stack.pop()
            continue

        if re.search(r'\bNEXTPAGE\b\s*=\s*["\']SCREEN["\']', st, flags=re.I):
            process_active_conditions([x for x in stack if x])

    cleaned_num = {}
    for name, rule in num_cons.items():
        if not isinstance(rule, dict):
            continue
        slot: dict[str, int] = {}
        if "min" in rule:
            slot["min"] = int(rule["min"])
        if "max" in rule:
            slot["max"] = int(rule["max"])
        if slot:
            if "min" in slot and "max" in slot and int(slot["min"]) > int(slot["max"]):
                slot["max"] = int(slot["min"])
            cleaned_num[str(name)] = slot

    if cleaned_num:
        g["__NUM_CONSTRAINTS__"] = cleaned_num
    if cond_rules:
        g["__COND_NUM_RULES__"] = cond_rules
    return g


def extract_screen_guards_from_asp(asp_text: str) -> dict[str, Any]:
    base = _extract_screen_guards_from_asp_base(asp_text)
    try:
        excluded = _patched_collect_or_equal_exclusions(str(asp_text or ""))
    except Exception:
        excluded = {}
    if isinstance(excluded, dict):
        for var, vals in excluded.items():
            if not vals:
                continue
            existing = base.get(var)
            if isinstance(existing, str) and (existing.startswith('__NEQ__:') or existing.startswith('__NEQSET__:')):
                base[var] = _merge_neq_tokens(existing, set(vals))
            elif var not in base:
                base[var] = _merge_neq_tokens(None, set(vals))
    return _enhance_nested_numeric_screen_guards(asp_text, base)



def build_asp_runtime_bundle(asp_text: str) -> dict[str, Any]:
    """ASP 로직에서 런타임에 필요한 추론 결과를 한 번에 수집한다."""
    bundle: dict[str, Any] = {
        "guards": {},
        "check_count_rules": {},
    }

    text = str(asp_text or "")
    if not text.strip():
        return bundle

    try:
        guards = extract_screen_guards_from_asp(text)
        if isinstance(guards, dict) and guards:
            bundle["guards"] = guards
    except Exception:
        pass

    try:
        rules = extract_checkbox_count_branch_rules(text)
        if isinstance(rules, dict) and rules:
            bundle["check_count_rules"] = rules
    except Exception:
        pass

    return bundle
