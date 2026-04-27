from __future__ import annotations
import re
import random
import logging
from typing import Any, Dict, Optional, List
from playwright.sync_api import Page


def detect_rank_question_from_var(meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    hidden.Var에 들어있는 슬롯 토큰으로 rank 문항을 감지한다.
    - 기존: Q숫자_숫자
    - 개선: D5_1, SQ16_2 같은 영문+숫자_숫자도 감지
    """
    hidden = meta.get("hidden", {})
    checks = meta.get("checks", {})

    var = hidden.get("Var")
    if not var:
        return None

    tokens = [t.strip() for t in str(var).split(",") if t.strip()]

    # ✅ Q34_1, D5_1, SQ16_2 뿐 아니라 C10D_1 같은 영숫자 혼합 base도 감지
    q_slots = [t for t in tokens if re.match(r"^[A-Za-z][A-Za-z0-9]*_\d+$", t)]
    if not q_slots:
        return None

    m = re.match(r"^([A-Za-z][A-Za-z0-9]*)_\d+$", q_slots[0])
    if not m:
        return None

    base = m.group(1)
    cols = [t for t in q_slots if re.match(rf"^{re.escape(base)}_\d+$", t)]
    if not cols:
        return None

    # 체크박스 V{base}_* 존재 여부로 rank 여부 재검증
    has_vq = any(name.startswith(f"V{base}_") for name in checks.keys())
    if not has_vq:
        return None

    return {"base": base, "need": len(cols)}


def fill_rank_question_dynamic(page: Page, base: str, need: int, cfg: Any, logger: logging.Logger) -> List[str]:
    """
    Rank 문항 자동 응답
    핵심 정책:
    1) cfg.case_overrides에 {base}_{slot} 형태가 있으면(예: D5_1=1) => forced 슬롯으로 간주하고 최우선 적용
       - 페이지 힌트(1순위 X 제외 탈락)보다 forced(ASP 가드)가 우선
    2) disabled/aria-disabled/.disabled/pointer-events:none 후보는 회피
    3) 슬롯 중간 공백은 normalize로 왼쪽으로 당김
    """

    # ------------------------------------------------------------
    # 후보 추출(JS)
    # ------------------------------------------------------------
    candidates = page.evaluate(
        """([base]) => {
          function norm(s){ return (s==null?"":String(s)).trim(); }

          function parseSetRankCall(s){
            const oc = norm(s);
            if(!oc) return null;
            const fnNames = ['setRank2', 'checkedRank2', 'setRank', 'checkedRank'];
            for(const fn of fnNames){
              const re1 = new RegExp(fn + String.raw`\(\s*['"]([^'"]+)['"]\s*,\s*['"]([^'"]*)['"]\s*,\s*['"]([^'"]*)['"]\s*,\s*['"]([^'"]*)['"]\s*\)`, 'i');
              let m = oc.match(re1);
              if(m){
                return { fn, base: norm(m[1]), v: norm(m[2]), opt3: norm(m[3]), needArg: norm(m[4]) };
              }
            }
            return null;
          }

          function vFromId(id){
            const s = norm(id);
            if(!s) return "";
            const m = s.match(/rank[_-]?(\\d+)/i);
            return m ? norm(m[1]) : "";
          }

          function vFromDataset(el){
            if(!el || !el.dataset) return "";
            const keys = ["value","v","rank","rankValue","code","id"];
            for(const k of keys){
              const vv = norm(el.dataset[k]);
              if(vv && /^\\d+$/.test(vv)) return vv;
            }
            return "";
          }

          function vFromInputsInside(el){
            if(!el) return "";
            const nodes = el.querySelectorAll('input,select,textarea');
            for(const n of nodes){
              const v = norm(n.value);
              if(v && /^\\d+$/.test(v)) return v;
            }
            return "";
          }

          function closestClickable(el){
            if(!el) return null;
            let cur = el;
            for(let i=0; i<4 && cur; i++){
              const oc = norm(cur.getAttribute && cur.getAttribute("onclick"));
              const id = norm(cur.id);
              const ds = vFromDataset(cur);
              if(oc || id || ds) return cur;
              cur = cur.parentElement;
            }
            return el;
          }

          function isDisabledLike(el){
            if(!el) return true;
            if (el.closest && el.closest('[aria-disabled="true"], .disabled')) return true;

            const tag = (el.tagName||"").toLowerCase();
            if (tag === "input" || tag === "select" || tag === "textarea" || tag === "button"){
              if (el.disabled === true) return true;
            }

            const ad = (el.getAttribute && (el.getAttribute("aria-disabled")||"").toLowerCase()) || "";
            if (ad === "true") return true;

            try{
              const st = window.getComputedStyle(el);
              if (st && st.pointerEvents === "none") return true;
            }catch(e){}
            return false;
          }

          const out = [];
          const seen = new Set();

          // Rank_*, onclick setRank2/checkedRank2 후보 풀
          const rankTds = Array.from(document.querySelectorAll('td[id^="Rank_"], td[id^="rank_"], td[id*="Rank_"], td[id*="rank_"]'));
          const onclickNodes = Array.from(document.querySelectorAll(
            '[onclick*="setRank2("], [onclick*="setRank2\("], [onclick*="checkedRank2("], [onclick*="checkedRank2\("], ' +
            '[onclick*="setRank("], [onclick*="setRank\("], [onclick*="checkedRank("], [onclick*="checkedRank\("]'
          ));
          const pool = Array.from(new Set([...rankTds, ...onclickNodes]));

          for(const el0 of pool){
            const el = closestClickable(el0);
            if(!el) continue;
            if (isDisabledLike(el)) continue;

            const oc = norm(el.getAttribute && el.getAttribute("onclick"));
            const parsed = parseSetRankCall(oc);

            let v = parsed && parsed.v ? parsed.v : "";
            if(!v) v = vFromId(el.id);
            if(!v) v = vFromDataset(el);
            if(!v) v = vFromInputsInside(el);

            v = norm(v);
            if(!v || !/^\\d+$/.test(v)) continue;

            const opt3 = parsed && parsed.opt3 ? parsed.opt3 : "";

            // Rank_v 자체가 disabled면 제외
            const td = document.getElementById("Rank_" + String(v));
            if (td && isDisabledLike(td)) continue;

            if(seen.has(v)) continue;
            seen.add(v);

            out.push({ v, opt3 });
          }

          return out;
        }""",
        [base],
    )

    if not candidates:
        logger.warning(f"rank({base}): candidates 비어있음")
        return []

    singles = [c for c in candidates if str(c.get("opt3", "")).strip() == "99"]
    normals = [c for c in candidates if str(c.get("opt3", "")).strip() != "99"]

    # ------------------------------------------------------------
    # 내부 유틸
    # ------------------------------------------------------------
    def _slot_values() -> List[str]:
        try:
            vals = page.evaluate(
                """([base, need]) => {
                  const out = [];
                  for(let i=1;i<=Number(need);i++){
                    const el = document.getElementById(base + '_' + String(i))
                           || document.querySelector('input[type="hidden"][name="'+base+'_'+String(i)+'"]');
                    out.push(el ? String(el.value||'').trim() : '');
                  }
                  return out;
                }""",
                [base, need],
            )
            return [str(v or "").strip() for v in (vals or [])]
        except Exception:
            return [""] * int(need)

    def _normalize_slots() -> List[str]:
        """
        슬롯 중간 공백 제거(왼쪽 당김) + UI 재렌더(initRank2 있으면 호출)
        """
        try:
            return page.evaluate(
                """([base, need]) => {
                  const vals = [];
                  for(let i=1;i<=Number(need);i++){
                    const el = document.getElementById(base + '_' + String(i))
                           || document.querySelector('input[type="hidden"][name="'+base+'_'+String(i)+'"]');
                    vals.push(el ? String(el.value||'').trim() : '');
                  }
                  const compact = vals.filter(v => v);
                  for(let i=1;i<=Number(need);i++){
                    const el = document.getElementById(base + '_' + String(i))
                           || document.querySelector('input[type="hidden"][name="'+base+'_'+String(i)+'"]');
                    if(!el) continue;
                    el.value = compact[i-1] || '';
                    try{ el.dispatchEvent(new Event('input', {bubbles:true})); }catch(e){}
                    try{ el.dispatchEvent(new Event('change', {bubbles:true})); }catch(e){}
                  }
                  const none = document.getElementById('NoneCheck');
                  if(none) none.value = 'N';

                  // ✅ UI 다시 그리기
                  if (typeof window.initRank2 === "function") {
                    try { window.initRank2(base); } catch(e){}
                  } else if (typeof window.initRank === "function") {
                    try { window.initRank(base); } catch(e){}
                  }

                  return compact;
                }""",
                [base, need],
            )
        except Exception:
            return [v for v in _slot_values() if v]

    def _reset_rank():
        """
        hidden/checkbox/ui까지 최대한 초기화 후 initRank2(base) 호출
        """
        page.evaluate(
            """([base]) => {
              // 1) hidden 슬롯 초기화
              document.querySelectorAll('input[type="hidden"][name^="'+base+'_"], input[type="hidden"][id^="'+base+'_"]').forEach(h => {
                h.value = "";
                try { h.dispatchEvent(new Event('input', {bubbles:true})); } catch(e){}
                try { h.dispatchEvent(new Event('change', {bubbles:true})); } catch(e){}
              });

              // 2) 체크박스(V{base}_*) 초기화
              document.querySelectorAll('input[type="checkbox"][id^="V'+base+'_"], input[type="checkbox"][name^="V'+base+'_"]').forEach(ch => {
                ch.checked = false;
                ch.removeAttribute("checked");
                try { ch.dispatchEvent(new Event('change', {bubbles:true})); } catch(e){}
              });

              // 3) Rank 텍스트가 남는 페이지가 있어 전체 Rank_ 텍스트 정리(보수적)
              document.querySelectorAll('td[id^="Rank_"]').forEach(td => {
                td.textContent = "";
              });

              // 4) initRank/initRank2로 최종 리셋/렌더
              if (typeof window.initRank2 === "function") {
                try { window.initRank2(base); } catch(e){}
              } else if (typeof window.initRank === "function") {
                try { window.initRank(base); } catch(e){}
              }

              const none = document.getElementById("NoneCheck");
              if (none) none.value="N";
            }""",
            [base],
        )

    def _forbidden_first_rank_values() -> set[str]:
        """
        페이지 문구에서 '1순위 X ... 제외/미선택 ... 탈락' 자동 감지
        (단, forced 슬롯이 있으면 forced가 우선)
        """
        try:
            txt = page.evaluate("""() => (document.body && (document.body.innerText || "")) || """"")
            t = str(txt or "")
            bad = set()
            for m in re.finditer(r"1\s*순위\s*(\d+)\s*.*?(제외|미선택).*?탈락", t):
                bad.add(m.group(1).strip())
            return bad
        except Exception:
            return set()

    def _forced_slots_from_overrides() -> dict[int, str]:
        """
        cfg.case_overrides에서 base_1, base_2 ... 형태를 자동 추출
        예) {"D5_1":"1"} -> {1:"1"}
        """
        forced: dict[int, str] = {}
        try:
            ov = getattr(cfg, "case_overrides", None) or {}
            if not isinstance(ov, dict):
                return forced
            for k, v in ov.items():
                if not isinstance(k, str):
                    continue
                m = re.match(rf"^{re.escape(base)}_(\d+)$", k.strip())
                if not m:
                    continue
                slot = int(m.group(1))
                if slot < 1 or slot > int(need):
                    continue
                if v is None:
                    continue
                sv = str(v).strip()
                if sv == "":
                    continue
                forced[slot] = sv
        except Exception:
            pass
        return forced

    def _is_rank_disabled(v: str) -> bool:
        try:
            ok = page.evaluate(
                """([v]) => {
                  const vv = String(v);
                  let el = document.getElementById("Rank_" + vv);
                  if (!el){
                    el = document.querySelector(`[data-value="${vv}"], [data-rank="${vv}"], [value="${vv}"]`);
                  }
                  if (!el) return false;

                  function isDisabledLike(x){
                    if(!x) return false;
                    if (x.closest && x.closest('[aria-disabled="true"], .disabled')) return true;
                    const tag = (x.tagName||"").toLowerCase();
                    if (tag === "input" || tag === "select" || tag === "textarea" || tag === "button"){
                      if (x.disabled === true) return true;
                    }
                    const ad = (x.getAttribute && (x.getAttribute("aria-disabled")||"").toLowerCase()) || "";
                    if (ad === "true") return true;
                    try{
                      const st = window.getComputedStyle(x);
                      if (st && st.pointerEvents === "none") return true;
                    }catch(e){}
                    return false;
                  }

                  return isDisabledLike(el);
                }""",
                [v],
            )
            return bool(ok)
        except Exception:
            return False

    def _applied(v: str) -> bool:
        sv = str(v).strip()
        if not sv:
            return False
        return any(str(s).strip() == sv for s in _slot_values())

    def _click_rank(v: str, opt3: str) -> bool:
        sv = str(v).strip()
        if not sv:
            return False

        # 중복/disabled 방지
        if sv in set(_slot_values()):
            return False
        if _is_rank_disabled(sv):
            return False

        # 1) Rank_칸 클릭 우선 (많은 페이지가 checkedRank2로 연결)
        try:
            ok = page.evaluate(
                """(v) => {
                  const td = document.getElementById("Rank_" + String(v));
                  if (!td) return false;
                  td.dispatchEvent(new MouseEvent("mousedown", {bubbles:true}));
                  td.dispatchEvent(new MouseEvent("mouseup", {bubbles:true}));
                  td.dispatchEvent(new MouseEvent("click", {bubbles:true}));
                  return true;
                }""",
                sv,
            )
            if ok:
                page.wait_for_timeout(60)
                _normalize_slots()
                if _applied(sv):
                    return True
        except Exception:
            pass

        # 2) JS 함수 (둘 중 하나만)
        try:
            page.evaluate(
                """([base, v, opt3, need]) => {
                  const sv = String(v);
                  if (typeof window.checkedRank2 === "function") {
                    try { window.checkedRank2(base, sv, String(opt3||""), String(need)); } catch(e){}
                    return;
                  }
                  if (typeof window.setRank2 === "function") {
                    try { window.setRank2(base, sv, String(opt3||""), String(need)); } catch(e){}
                    return;
                  }
                  if (typeof window.checkedRank === "function") {
                    try { window.checkedRank(base, sv, String(opt3||""), String(need)); } catch(e){}
                    return;
                  }
                  if (typeof window.setRank === "function") {
                    try { window.setRank(base, sv, String(opt3||""), String(need)); } catch(e){}
                    return;
                  }
                }""",
                [base, sv, str(opt3 or ""), need],
            )
            page.wait_for_timeout(60)
            _normalize_slots()
            if _applied(sv):
                return True
        except Exception:
            pass

        # 3) VD{base}_{v} 클릭 폴백
        try:
            page.click(f"#V{base}_{sv}", timeout=800)
            page.wait_for_timeout(60)
            _normalize_slots()
            return _applied(sv)
        except Exception:
            return False

    # ------------------------------------------------------------
    # pick 개수 정책
    # ------------------------------------------------------------
    rank_select_all = bool(getattr(cfg, "rank_select_all", False))
    rp_min = int(getattr(cfg, "rank_pick_min", 1) or 1)
    rp_max_raw = int(getattr(cfg, "rank_pick_max", 0) or 0)
    rp_max = need if rp_max_raw == 0 else rp_max_raw

    rp_min = max(1, min(rp_min, need))
    rp_max = max(1, min(rp_max, need))
    if rp_max < rp_min:
        rp_max = rp_min

    if rank_select_all:
        pick_need = need
    else:
        # ✅ need>=2이고 사용자가 pick_min/max 명시 안 했으면 => need개 채우기
        if need >= 2 and rp_min == 1 and rp_max_raw == 0:
            pick_need = need
        else:
            pick_need = random.randint(rp_min, rp_max)

    # normals 부족한 경우 보정
    pick_need = max(1, min(pick_need, len(normals) if normals else 1))

    # ------------------------------------------------------------
    # forced / forbid 계산
    # ------------------------------------------------------------
    forced_slots = _forced_slots_from_overrides()
    forbid_first = _forbidden_first_rank_values()

    # ✅ forced(slot1)가 있으면 forbid에 걸려도 무시(=ASP guard 우선)
    if forced_slots.get(1):
        fv = str(forced_slots.get(1)).strip()
        if fv in forbid_first:
            logger.info(f"rank({base}): forbid_first contains forced slot1={fv} -> ignore forbid for forced")
            forbid_first.discard(fv)

    if forbid_first:
        logger.info(f"rank({base}): forbid_first(slot1)={sorted(list(forbid_first))}")

    # ------------------------------------------------------------
    # 메인 시도 루프: forced 먼저 채우고 나머지 랜덤
    # ------------------------------------------------------------
    random.shuffle(normals)

    def _slots_ok() -> bool:
        slots = _slot_values()

        # forced 검증
        for slot, want in forced_slots.items():
            idx = slot - 1
            if idx < 0 or idx >= len(slots):
                return False
            if (slots[idx] or "").strip() != str(want).strip():
                return False

        # pick_need 만큼 앞 슬롯이 비어있지 않아야 함
        for i in range(min(pick_need, len(slots))):
            if not (slots[i] or "").strip():
                return False
        return True

    MAX_TRIES = 4
    best_slots: List[str] = []
    best_count = -1

    for attempt in range(1, MAX_TRIES + 1):
        _reset_rank()
        picked_vs: List[str] = []
        used_vs: set[str] = set()

        # 0) forced 슬롯 우선
        for slot in sorted(forced_slots.keys()):
            want_v = str(forced_slots[slot]).strip()
            if not want_v:
                continue
            if want_v in used_vs:
                continue
            if _is_rank_disabled(want_v):
                logger.info(f"rank({base}): forced v={want_v} disabled -> skip")
                continue

            opt3_w = ""
            for c in candidates:
                if str(c.get("v")) == want_v:
                    opt3_w = str(c.get("opt3", "") or "").strip()
                    break

            if _click_rank(want_v, opt3_w):
                _normalize_slots()
                slots_now = _slot_values()
                idx = slot - 1
                if idx < len(slots_now) and (slots_now[idx] or "").strip() == want_v:
                    picked_vs.append(want_v)
                    used_vs.add(want_v)
                else:
                    logger.warning(f"rank({base}) attempt {attempt}: forced slot{slot} mismatch slots={slots_now}")

        # 1) 나머지 랜덤 채우기
        batch = normals[:]
        random.shuffle(batch)

        for p in batch:
            slots_now = [s for s in _slot_values() if (s or "").strip()]
            if len(slots_now) >= pick_need:
                break

            v = str(p.get("v") or "").strip()
            if not v:
                continue
            if v in used_vs:
                continue
            if _is_rank_disabled(v):
                continue

            opt3 = str(p.get("opt3", "") or "").strip()
            if opt3 == "99":
                continue

            # slot1 비어있는 상태라면 forbid_first는 스킵
            cur_slots = _slot_values()
            if need >= 1 and not (cur_slots[0] or "").strip() and v in forbid_first:
                continue

            if _click_rank(v, opt3):
                _normalize_slots()
                used_vs.add(v)
                picked_vs.append(v)

        slots_final = _slot_values()
        filled = len([s for s in slots_final if (s or "").strip()])
        if filled > best_count:
            best_count = filled
            best_slots = slots_final

        if _slots_ok():
            logger.info(f"rank({base}) attempt {attempt}: OK slots={slots_final} forced={forced_slots}")
            return [s for s in slots_final if (s or "").strip()]

        logger.warning(f"rank({base}) attempt {attempt}: FAIL slots={slots_final} picked={picked_vs} forced={forced_slots}")

    # best-effort 반환
    if best_slots:
        logger.warning(f"rank({base}): giving best-effort slots={best_slots} forced={forced_slots}")
        return [s for s in best_slots if (s or "").strip()]

    # 그래도 실패면 single(99) 폴백
    enabled_singles = [s for s in singles if not _is_rank_disabled(str(s["v"]))]
    if enabled_singles:
        pick = random.choice(enabled_singles)
        v = str(pick["v"])
        logger.info(f"rank({base}): fallback single(99) v={v}")
        _reset_rank()
        _click_rank(v, "99")
        return [v]

    logger.warning(f"rank({base}): picked none (all disabled/failed).")
    return []