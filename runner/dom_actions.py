from __future__ import annotations

import re
from typing import Any, Dict

from playwright.sync_api import Page

from .config import RunnerConfig


def wait_nav_best_effort(page: Page, timeout_ms: int = 250):
    try:
        page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
    except Exception:
        pass
    try:
        page.wait_for_timeout(20)
    except Exception:
        pass


def set_checked(page: Page, selector: str, checked: bool = True) -> bool:
    """
    모든 프레임을 순회하며 체크/언체크를 시도합니다. 폴백 로직 포함.
    """
    targets = list(dict.fromkeys([page.main_frame] + page.frames))

    for frame in targets:
        try:
            loc = frame.locator(selector).first
            if loc.count() > 0:
                try:
                    if checked:
                        loc.check(timeout=500, force=True)
                    else:
                        loc.uncheck(timeout=500, force=True)
                except Exception:
                    try:
                        loc.click(timeout=500, force=True)
                    except Exception:
                        pass
                
                try:
                    frame.evaluate(
                        """([sel, want]) => {
                        const nodes = Array.from(document.querySelectorAll(sel));
                        const pickVisible = (arr) => {
                            for (const n of arr) {
                                try {
                                    if (!n) continue;
                                    const r = n.getClientRects();
                                    if (r && r.length > 0) return n;
                                } catch (e) {}
                            }
                            return arr[0] || null;
                        };

                        const el = pickVisible(nodes);
                        if (!el) return;
                        if ((!!el.checked) === (!!want)) return;

                        const isRadio = (el.type || "").toLowerCase() === "radio";
                        if (!want && isRadio) {
                            el.checked = false;
                            try { el.dispatchEvent(new Event('change', { bubbles: true })); } catch (e) {}
                            return;
                        }

                        // Disabled check completely removed to brute-force interaction

                        // Click TD/Label fallback for ASP surveys
                        const id = el.getAttribute("id") || "";
                        let wrapper = null;
                        if (id) wrapper = document.getElementById("TD_" + id);
                        if (!wrapper) wrapper = el.closest("label");
                        if (!wrapper) wrapper = el.closest("td");

                        try {
                            if (wrapper) {
                                wrapper.dispatchEvent(new MouseEvent("mousedown", { bubbles:true }));
                                wrapper.dispatchEvent(new MouseEvent("mouseup", { bubbles:true }));
                                wrapper.dispatchEvent(new MouseEvent("click", { bubbles:true }));
                            } else {
                                el.click();
                            }
                        } catch(e) {
                            try { el.click(); } catch(e2) {}
                        }

                        // Force state just in case wrapper click didn't propagate
                        if ((!!el.checked) !== (!!want)) {
                            el.checked = !!want;
                        }

                        try { el.dispatchEvent(new Event('input', { bubbles: true })); } catch (e) {}
                        try { el.dispatchEvent(new Event('change', { bubbles: true })); } catch (e) {}
                        }""",
                        [selector, checked]
                    )
                except Exception:
                    pass

                # 상태 검증
                is_checked = bool(frame.evaluate(
                    """([sel, want]) => {
                      const el = document.querySelector(sel);
                      return el ? (!!el.checked === !!want) : false;
                    }""",
                    [selector, checked]
                ))
                if is_checked:
                    return True
        except Exception:
            # 개별 프레임 실패 시 다음 프레임 시도
            pass

    return False



def click_with_td_fallback(page: Page, selector: str) -> bool:
    """
    radio/checkbox 클릭 시
    input 직접 클릭 + TD_<id> fallback + closest(td) fallback
    """
    try:
        ok = bool(
            page.evaluate(
                """(sel) => {
                    const el = document.querySelector(sel);
                    if (!el) return false;

                    const id = el.getAttribute("id") || "";
                    let td = null;

                    if (id) td = document.getElementById("TD_" + id);
                    if (!td) td = el.closest("td");

                    try {
                        if (td) {
                            td.dispatchEvent(new MouseEvent("mousedown", { bubbles:true }));
                            td.dispatchEvent(new MouseEvent("mouseup", { bubbles:true }));
                            td.dispatchEvent(new MouseEvent("click", { bubbles:true }));
                        } else {
                            el.click();
                        }
                    } catch(e) {
                        try { el.click(); } catch(e2) {}
                    }

                    try { el.dispatchEvent(new Event("input", { bubbles:true })); } catch(e) {}
                    try { el.dispatchEvent(new Event("change", { bubbles:true })); } catch(e) {}

                    return !!el.checked;
                }""",
                selector,
            )
        )
        return ok
    except Exception:
        return False


def can_set_value(page: Page, selector: str) -> bool:
    try:
        return bool(
            page.evaluate(
                """(sel) => {
                  const el = document.querySelector(sel);
                  if (!el) return false;

                  function isDisabledLike(node) {
                    if (!node) return true;
                    if (node.disabled === true) return true;
                    if (node.readOnly === true) return true;

                    let cur = node;
                    while (cur) {
                      try {
                        if (cur.getAttribute && cur.getAttribute("aria-disabled") === "true") return true;
                      } catch (e) {}
                      try {
                        if (cur.classList && cur.classList.contains("disabled")) return true;
                      } catch (e) {}
                      cur = cur.parentElement;
                    }

                    try {
                      const cs = window.getComputedStyle(node);
                      if (cs && (cs.pointerEvents === "none" || cs.visibility === "hidden" || cs.display === "none")) {
                        return true;
                      }
                    } catch (e) {}

                    return false;
                  }

                  return !isDisabledLike(el);
                }""",
                selector,
            )
        )
    except Exception:
        return False



def set_value(page: Page, selector: str, value: str) -> bool:
    """
    모든 프레임을 순회하며 값을 입력합니다.
    """
    targets = list(dict.fromkeys([page.main_frame] + page.frames))

    for frame in targets:
        try:
            loc = frame.locator(selector).first
            if loc.count() > 0:
                # 활성 상태 확인
                disabled = bool(frame.evaluate(
                    """(sel) => {
                      const el = document.querySelector(sel);
                      return el ? (el.disabled || el.readOnly) : true;
                    }""",
                    selector
                ))
                if disabled:
                    continue

                loc.fill(value, timeout=500, force=True)
                return True
        except Exception:
            pass

    return False



def _safe_has_selector(page: Page, selector: str) -> bool:
    """
    count()/queryCount()는 navigation 직후 execution context destroyed 에 취약하므로
    가벼운 JS querySelector 기반 존재 확인을 우선 사용.
    """
    try:
        return bool(
            page.evaluate(
                """(sel) => {
                  try {
                    return !!document.querySelector(sel);
                  } catch (e) {
                    return false;
                  }
                }""",
                selector,
            )
        )
    except Exception:
        return False



def _safe_click_first(page: Page, selector: str, timeout: int = 700) -> bool:
    try:
        page.locator(selector).first.click(force=True, timeout=timeout)
        return True
    except Exception:
        return False



def get_next_runtime_stats(page: Page) -> Dict[str, Any]:
    try:
        data = page.evaluate(
            """() => {
              const s = window.__SURVEY_DUMMY_NEXT_STATS || {};
              return {
                wrap_installed: !!window.__SURVEY_DUMMY_NEXT_WRAP_INSTALLED,
                call_count: Number(s.call_count || 0),
                slow_count: Number(s.slow_count || 0),
                last_started_at: Number(s.last_started_at || 0),
                last_finished_at: Number(s.last_finished_at || 0),
                last_duration_ms: Number(s.last_duration_ms || 0),
                max_duration_ms: Number(s.max_duration_ms || 0),
                last_error: String(s.last_error || ''),
                last_mode: String(s.last_mode || ''),
              };
            }"""
        )
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {
        "wrap_installed": False,
        "call_count": 0,
        "slow_count": 0,
        "last_started_at": 0,
        "last_finished_at": 0,
        "last_duration_ms": 0,
        "max_duration_ms": 0,
        "last_error": "",
        "last_mode": "",
    }



def try_click_next(page: Page) -> bool:
    return bool(try_click_next_timed(page).get("clicked"))



def try_click_next_timed(page: Page) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "clicked": False,
        "method": "",
        "duration_ms": 0.0,
        "error": "",
    }

    try:
        data = page.evaluate(
            """() => {
              const out = { clicked:false, method:'', duration_ms:0, error:'' };

              const clickEl = (el, method) => {
                if (!el) return null;
                try {
                  if (el.disabled === true) return null;
                } catch (e) {}
                const t0 = performance.now();
                try {
                  el.click();
                  return { clicked:true, method, duration_ms:(performance.now() - t0), error:'' };
                } catch (e) {
                  try {
                    el.dispatchEvent(new MouseEvent('click', { bubbles:true }));
                    return { clicked:true, method:method + ':dispatch', duration_ms:(performance.now() - t0), error:'' };
                  } catch (e2) {
                    return { clicked:false, method, duration_ms:(performance.now() - t0), error:String((e2 && e2.message) || e2 || '') };
                  }
                }
              };

              try {
                if (typeof window.next === 'function') {
                  const t0 = performance.now();
                  window.next();
                  return { clicked:true, method:'window.next()', duration_ms:(performance.now() - t0), error:'' };
                }
              } catch (e) {
                return { clicked:false, method:'window.next()', duration_ms:0, error:String((e && e.message) || e || '') };
              }

              const direct = clickEl(document.querySelector('#next'), '#next');
              if (direct) return direct;

              const formSubmit = clickEl(document.querySelector("form button[type='submit']"), "form button[type='submit']");
              if (formSubmit) return formSubmit;

              const textCandidates = Array.from(document.querySelectorAll("button, input[type='button'], input[type='submit'], a"));
              for (const el of textCandidates) {
                const txt = ((el.innerText || el.value || el.textContent || '') + '').trim();
                if (/(다음|Next|계속)/i.test(txt)) {
                  const row = clickEl(el, 'text_candidate');
                  if (row) return row;
                }
              }

              return out;
            }"""
        ) or {}
        if isinstance(data, dict):
            result.update(data)
            if result.get("clicked"):
                return result
    except Exception as e:
        result.update({"clicked": False, "method": "try_click_next", "error": str(e)})

    try:
        btn = page.locator("button", has_text=re.compile(r"다음|Next|계속", re.I)).first
        t0 = page.evaluate("() => performance.now()")
        btn.click(force=True, timeout=700)
        t1 = page.evaluate("() => performance.now()")
        return {
            "clicked": True,
            "method": "text_button",
            "duration_ms": float(t1) - float(t0),
            "error": "",
        }
    except Exception as e:
        result.update({"clicked": False, "method": "text_button", "error": str(e)})

    return result



def force_form_submit(page: Page, prefer_fast: bool = True):
    force_form_submit_timed(page, prefer_fast=prefer_fast)



def force_form_submit_timed(page: Page, prefer_fast: bool = True) -> Dict[str, Any]:
    try:
        data = page.evaluate(
            """(preferFast) => {
              const out = { submitted:false, method:'', duration_ms:0, error:'' };

              const clickEl = (el, method) => {
                if (!el) return null;
                try {
                  if (el.disabled === true) return null;
                } catch (e) {}
                const t0 = performance.now();
                try {
                  el.click();
                  return { submitted:true, method, duration_ms:(performance.now() - t0), error:'' };
                } catch (e) {
                  try {
                    el.dispatchEvent(new MouseEvent('click', { bubbles:true }));
                    return { submitted:true, method:method + ':dispatch', duration_ms:(performance.now() - t0), error:'' };
                  } catch (e2) {
                    return { submitted:false, method, duration_ms:(performance.now() - t0), error:String((e2 && e2.message) || e2 || '') };
                  }
                }
              };

              // #upload \ube84\ud0bc\uc774 \uc788\uc73c\uba74 \uba3c\uc800 \ud074\ub9ad\ud558\uc5ec \uc11c\uba85 \uc5c5\ub85c\ub4dc\ud55c \ub4a4, window.next()\ub85c \ud3fc \uc81c\uc5c4\uc9c4
              // #upload 버튼이 있으면 클릭하여 서명 업로드를 진행한다.
              // 해당 문항의 성격상 전송 후 alert이 뜨거나 async 처리가 많으므로
              // window.next()를 즉시 강제 호출하지 않고 클릭 이벤트 발생에 집중한다.
              const uploadBtn = document.querySelector('#upload, #btn_upload');
              if (uploadBtn && uploadBtn.disabled !== true) {
                const t0 = performance.now();
                try {
                  uploadBtn.click();
                  return { submitted:true, method:'custom_upload_btn:click', duration_ms:(performance.now() - t0), error:'' };
                } catch (e) {
                  try {
                    uploadBtn.dispatchEvent(new MouseEvent('click', { bubbles:true }));
                    return { submitted:true, method:'custom_upload_btn:dispatch', duration_ms:(performance.now() - t0), error:'' };
                  } catch (e2) {
                    return { submitted:false, method:'custom_upload_btn', duration_ms:(performance.now() - t0), error:String((e2 && e2.message) || e2 || '') };
                  }
                }
              }

              try {
                if (typeof window.next === 'function') {
                  const t0 = performance.now();
                  window.next();
                  return { submitted:true, method:'window.next()', duration_ms:(performance.now() - t0), error:'' };
                }
              } catch (e) {
                return { submitted:false, method:'window.next()', duration_ms:0, error:String((e && e.message) || e || '') };
              }

              const nextBtn = clickEl(document.querySelector('#next'), '#next.click()');
              if (nextBtn) return nextBtn;

              const namedSubmit = clickEl(document.querySelector("form button[type='submit']"), "form button[type='submit']");
              if (namedSubmit) return namedSubmit;

              const textCandidates = Array.from(document.querySelectorAll("button, input[type='submit'], input[type='button'], a"));
              for (const el of textCandidates) {
                const txt = String(el.innerText || el.value || el.textContent || '').trim();
                if (/(다음|next|계속)/i.test(txt)) {
                  const row = clickEl(el, 'text_submitter');
                  if (row) return row;
                }
              }

              const form = document.querySelector("form[name='Survey']") || document.querySelector('form');
              if (!form) {
                out.method = 'form.submit()';
                out.error = 'form not found';
                return out;
              }

              if (preferFast) {
                const t0 = performance.now();
                try {
                  if (typeof form.requestSubmit === 'function') {
                    form.requestSubmit();
                    return { submitted:true, method:'form.requestSubmit()', duration_ms:(performance.now() - t0), error:'' };
                  }
                } catch (e) {}

                try {
                  const ev = new Event('submit', { bubbles:true, cancelable:true });
                  const notCancelled = form.dispatchEvent(ev);
                  if (notCancelled) {
                    form.submit();
                    return { submitted:true, method:'dispatch+submit(form)', duration_ms:(performance.now() - t0), error:'' };
                  }
                  return { submitted:false, method:'dispatch_submit_blocked', duration_ms:(performance.now() - t0), error:'submit event cancelled' };
                } catch (e) {
                  return { submitted:false, method:'dispatch+submit(form)', duration_ms:(performance.now() - t0), error:String((e && e.message) || e || '') };
                }
              }

              try {
                const t0 = performance.now();
                form.submit();
                return { submitted:true, method:'form.submit()', duration_ms:(performance.now() - t0), error:'' };
              } catch (e) {
                return { submitted:false, method:'form.submit()', duration_ms:0, error:String((e && e.message) || e || '') };
              }
            }""",
            prefer_fast,
        )
        if isinstance(data, dict):
            return data
    except Exception as e:
        return {
            "submitted": False,
            "method": "force_form_submit",
            "duration_ms": 0.0,
            "error": str(e),
        }
    return {
        "submitted": False,
        "method": "force_form_submit",
        "duration_ms": 0.0,
        "error": "unknown",
    }
