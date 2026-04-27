from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from playwright.sync_api import ConsoleMessage, Error as PlaywrightError, Page, Request, sync_playwright

from .autofill import autofill_page_by_dom
from .config import RunnerConfig
from .detect import is_completed, is_url_error
from .dom_actions import force_form_submit_timed, get_next_runtime_stats, try_click_next_timed, wait_nav_best_effort
from .form_parse import parse_form_fields
from .next_logic import apply_next_constraints, diagnose_next_failures, repair_after_alert
from .page_id import extract_page_id
from .snapshots import dump_snapshot
from .utils import sleep_jitter, write_json


def _norm_stop_token(s: str | None) -> str:
    if not s:
        return ""
    t = str(s).strip().lower()
    if not t:
        return ""
    return os.path.splitext(t)[0].strip()


def _hit_stop_page(page_id: str, url: str, stop_at_page: str | None) -> bool:
    stop = _norm_stop_token(stop_at_page)
    if not stop:
        return False

    if _norm_stop_token(page_id) == stop:
        return True

    try:
        path = urlparse(url).path or ""
        stem = os.path.splitext(os.path.basename(path))[0].strip().lower()
        if stem == stop:
            return True
    except Exception:
        pass
    return False


def _hold_visible_page(page: Page, logger: logging.Logger, max_seconds: int | None = None) -> None:
    logger.info("[breakpoint] holding page for manual input... (close the window to continue/end)")
    start = time.time()
    last_ok_ping = time.time()

    while True:
        if max_seconds is not None and (time.time() - start) >= max_seconds:
            logger.info(f"[breakpoint] max_seconds reached ({max_seconds}s). exit hold.")
            return

        try:
            if page.is_closed():
                logger.info("[breakpoint] page closed by user.")
                return
        except Exception as e:
            logger.info(f"[breakpoint] page handle lost. exit hold. err={e}")
            return

        try:
            br = page.context.browser
            if br is not None and hasattr(br, "is_connected") and (not br.is_connected()):
                logger.info("[breakpoint] browser disconnected. exit hold.")
                return
        except Exception:
            pass

        try:
            _ = page.url
            if (time.time() - last_ok_ping) > 5:
                _ = page.title()
                last_ok_ping = time.time()
        except Exception as e:
            logger.info(f"[breakpoint] page not reachable (probably closed). exit hold. err={e}")
            return

        time.sleep(1)


def _install_next_probe(page: Page) -> None:
    try:
        page.add_init_script(
            """() => {
            try {
                if (window.__SURVEY_DUMMY_NEXT_WRAP_INSTALLED) return;
                window.__SURVEY_DUMMY_NEXT_WRAP_INSTALLED = true;

                if (!window.__SURVEY_DUMMY_NEXT_STATS) {
                    window.__SURVEY_DUMMY_NEXT_STATS = {
                        call_count: 0,
                        slow_count: 0,
                        last_started_at: 0,
                        last_finished_at: 0,
                        last_duration_ms: 0,
                        max_duration_ms: 0,
                        last_error: '',
                        last_mode: ''
                    };
                }

                const push = (kind, message) => {
                    try {
                        if (!window.__SURVEY_DUMMY_LOGS) window.__SURVEY_DUMMY_LOGS = [];
                        window.__SURVEY_DUMMY_LOGS.push({
                            ts: new Date().toISOString(),
                            kind: String(kind || ''),
                            message: String(message || '')
                        });
                        if (window.__SURVEY_DUMMY_LOGS.length > 300) {
                            window.__SURVEY_DUMMY_LOGS = window.__SURVEY_DUMMY_LOGS.slice(-300);
                        }
                    } catch (e) {}
                };

                const stats = window.__SURVEY_DUMMY_NEXT_STATS;

                const wrapNext = () => {
                    try {
                        const cur = window.next;
                        if (typeof cur !== 'function') return;
                        if (cur.__surveyDummyWrapped === true) return;

                        const wrapped = function(...args) {
                            const t0 = performance.now();
                            stats.call_count = Number(stats.call_count || 0) + 1;
                            stats.last_started_at = Date.now();
                            stats.last_mode = 'wrapped_next';
                            stats.last_error = '';
                            try {
                                const ret = cur.apply(this, args);
                                const dt = performance.now() - t0;
                                stats.last_duration_ms = dt;
                                stats.last_finished_at = Date.now();
                                stats.max_duration_ms = Math.max(Number(stats.max_duration_ms || 0), dt);
                                if (dt >= 1000) stats.slow_count = Number(stats.slow_count || 0) + 1;
                                push('next.timing', `wrapped next() duration=${dt.toFixed(1)}ms`);
                                return ret;
                            } catch (err) {
                                const dt = performance.now() - t0;
                                stats.last_duration_ms = dt;
                                stats.last_finished_at = Date.now();
                                stats.max_duration_ms = Math.max(Number(stats.max_duration_ms || 0), dt);
                                stats.last_error = String((err && err.message) || err || '');
                                push('next.error', `wrapped next() duration=${dt.toFixed(1)}ms error=${stats.last_error}`);
                                throw err;
                            }
                        };

                        try { Object.defineProperty(wrapped, '__surveyDummyWrapped', { value: true }); } catch (e) { wrapped.__surveyDummyWrapped = true; }
                        try { Object.defineProperty(wrapped, '__surveyDummyOriginal', { value: cur }); } catch (e) { wrapped.__surveyDummyOriginal = cur; }
                        window.next = wrapped;
                    } catch (e) {}
                };

                wrapNext();
                setInterval(wrapNext, 250);
            } catch (e) {}
            }"""
        )
    except Exception:
        pass


def _summarize_next_stat_delta(before: Dict[str, Any], after: Dict[str, Any]) -> str:
    bcount = int((before or {}).get("call_count") or 0)
    acount = int((after or {}).get("call_count") or 0)
    adur = float((after or {}).get("last_duration_ms") or 0.0)
    amax = float((after or {}).get("max_duration_ms") or 0.0)
    amode = str((after or {}).get("last_mode") or "")
    aerr = str((after or {}).get("last_error") or "")
    return (
        f"calls={bcount}->{acount} "
        f"last_duration_ms={adur:.1f} max_duration_ms={amax:.1f} "
        f"mode={amode or '-'} error={aerr or '-'}"
    )


def _quick_settle_after_repair(page: Page, cfg: RunnerConfig) -> None:
    try:
        page.wait_for_timeout(max(5, int(getattr(cfg, "pre_next_click_delay_ms", 25))))
    except Exception:
        pass


def _wait_after_submit(page: Page, trace: Dict[str, Any], timeout_ms: int = 120) -> None:
    if trace.get("last_alert"):
        try:
            page.wait_for_timeout(10)
        except Exception:
            pass
        return
    
    # Add a fixed wait because ASP form submittions often take > 200ms to respond for redirect
    try:
        page.wait_for_timeout(250)
    except Exception:
        pass
        
    wait_nav_best_effort(page, timeout_ms=max(300, int(timeout_ms * 3)))


def _safe_page_content(page: Page, timeout_ms: int = 120) -> str:
    try:
        return page.content() or ""
    except Exception:
        try:
            wait_nav_best_effort(page, timeout_ms=max(20, int(timeout_ms)))
            return page.content() or ""
        except Exception:
            return ""


def _current_page_state(page: Page, timeout_ms: int = 120) -> Tuple[str, str, str]:
    url = ""
    try:
        url = page.url or ""
    except Exception:
        url = ""
    html = _safe_page_content(page, timeout_ms=timeout_ms)
    page_id = extract_page_id(url, html)
    return url, html, page_id


def _page_signature(url: str, page_id: str) -> str:
    return f"{_norm_stop_token(page_id)}|{url}"


def _log_submit_state_if_enabled(page: Page, cfg: RunnerConfig, logger: logging.Logger, idx: int, tag: str = "submit_state") -> None:
    if not bool(getattr(cfg, "log_submit_state", False)):
        return

    try:
        submit_state = page.evaluate(
            """() => {
              const f = document.querySelector("form[name='Survey']") || document.querySelector("form");
              if (!f) return { has_form: false };

              const fd = new FormData(f);
              const out = {};
              for (const [k, v] of fd.entries()) {
                if (Object.prototype.hasOwnProperty.call(out, k)) {
                  if (Array.isArray(out[k])) out[k].push(String(v));
                  else out[k] = [String(out[k]), String(v)];
                } else {
                  out[k] = String(v);
                }
              }

              return {
                has_form: true,
                action: f.getAttribute("action") || "",
                method: (f.getAttribute("method") || "get").toUpperCase(),
                data: out
              };
            }"""
        )

        if submit_state and submit_state.get("has_form"):
            data = submit_state.get("data", {}) or {}
            key_names = ["NextPage", "NPAGE", "PAGE", "QPAGE", "MOVEPAGE", "IDX", "ID", "AIDX", "InIDX", "ResType"]
            key_dump = {k: data.get(k) for k in key_names if k in data}
            a0_dump = {k: v for k, v in data.items() if str(k).startswith("A0")}
            logger.info(
                f"[{idx}] {tag} method={submit_state.get('method')} action={submit_state.get('action')} "
                f"keys={key_dump} a0={a0_dump}"
            )
        else:
            logger.warning(f"[{idx}] {tag} no form found")
    except Exception as e:
        logger.warning(f"[{idx}] {tag} log failed: {e}")


def _switch_to_headed_and_hold(pw, browser, context, page: Page, cfg, logger) -> None:
    url = ""
    try:
        url = page.url
    except Exception:
        pass

    out_dir = getattr(cfg, "out_dir", ".")
    os.makedirs(out_dir, exist_ok=True)
    st_path = os.path.join(out_dir, "storage_state.json")

    try:
        context.storage_state(path=st_path)
        logger.info(f"[breakpoint] storage_state saved: {st_path}")
    except Exception as e:
        logger.warning(f"[breakpoint] storage_state save failed: {e}")

    try:
        browser.close()
    except Exception:
        pass

    browser2 = pw.chromium.launch(headless=False)
    ctx2 = browser2.new_context(storage_state=st_path if os.path.exists(st_path) else None)
    p2 = ctx2.new_page()

    try:
        if url:
            p2.goto(url, wait_until="domcontentloaded")
    except Exception as e:
        logger.warning(f"[breakpoint] headed goto failed: {e}")

    _hold_visible_page(p2, logger, max_seconds=getattr(cfg, "stop_hold_max_seconds", None))

    try:
        browser2.close()
    except Exception:
        pass


def _trigger_submit(page: Page, logger: logging.Logger, idx: int, trace: Dict[str, Any], phase: str, wait_ms: int = 90) -> Tuple[dict[str, Any], str, str, str]:
    trace["last_alert"] = ""
    next_stats_before = get_next_runtime_stats(page)
    result = force_form_submit_timed(page, prefer_fast=True)
    logger.info(
        f"[{idx}] next_trigger {phase} method={result.get('method') or '-'} "
        f"duration_ms={float(result.get('duration_ms') or 0.0):.1f} "
        f"submitted={bool(result.get('submitted'))} error={result.get('error') or '-'}"
    )
    next_stats_after = get_next_runtime_stats(page)
    logger.info(f"[{idx}] next_runtime_{phase} {_summarize_next_stat_delta(next_stats_before, next_stats_after)}")
    _wait_after_submit(page, trace, timeout_ms=wait_ms)
    url, html, page_id = _current_page_state(page, timeout_ms=wait_ms)
    return result, url, html, page_id


def _trigger_after_repair(page: Page, logger: logging.Logger, idx: int, trace: Dict[str, Any], timeout_ms: int = 80) -> Tuple[str, str]:
    _trigger_submit(page, logger, idx, trace, phase="repair", wait_ms=timeout_ms)
    url, html, _ = _current_page_state(page, timeout_ms=timeout_ms)
    return url, html


def _maybe_apply_next_constraints(page: Page, cfg: RunnerConfig, logger: logging.Logger) -> None:
    if not bool(getattr(cfg, "apply_next_constraints_before_click", False)):
        return
    html_after_fill = _safe_page_content(page, timeout_ms=80)
    if not html_after_fill:
        return
    meta_after_fill = parse_form_fields(html_after_fill)
    if not meta_after_fill.get("has_form"):
        return
    meta_after_fill["case_overrides"] = getattr(cfg, "case_overrides", {}) or {}
    apply_next_constraints(page, meta_after_fill, cfg, logger)
    try:
        page.wait_for_timeout(max(5, int(getattr(cfg, "pre_next_click_delay_ms", 25))))
    except Exception:
        pass


def run_one(cfg: RunnerConfig, logger: logging.Logger, idx: int, verifier=None) -> bool:
    trace: Dict[str, Any] = {
        "idx": idx,
        "start_url": cfg.start_url,
        "ok": False,
        "completed": False,
        "screen_hit": False,
        "final_url": "",
        "visited_pages": [],
        "visited_edges": [],
        "last_alert": "",
        "alert_history": [],
    }

    visited_pages: List[str] = []
    visited_edges: List[str] = []
    started_at = time.monotonic()
    execution_timeout_sec = max(1, int(getattr(cfg, "execution_timeout_sec", 600) or 600))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=cfg.headless)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.set_default_navigation_timeout(cfg.navigation_timeout_ms)
        try:
            page.set_default_timeout(min(int(cfg.navigation_timeout_ms), execution_timeout_sec * 1000))
        except Exception:
            pass

        def _push_browser_event(kind: str, message: str) -> None:
            try:
                message = str(message or "").strip()
            except Exception:
                message = ""
            if not message:
                return
            line = f"[{kind}] {message}"
            try:
                hist = trace.setdefault("browser_event_history", [])
                hist.append(line)
                if len(hist) > 300:
                    del hist[:-300]
            except Exception:
                pass
            try:
                logger.warning(f"[{idx}] {line}")
            except Exception:
                pass

        def _install_page_log_bridge() -> None:
            try:
                page.add_init_script(
                    """() => {
                    try {
                        if (!window.__SURVEY_DUMMY_LOGS) window.__SURVEY_DUMMY_LOGS = [];
                        const push = (kind, message) => {
                            try {
                                window.__SURVEY_DUMMY_LOGS.push({
                                    ts: new Date().toISOString(),
                                    kind: String(kind || ''),
                                    message: String(message || '')
                                });
                                if (window.__SURVEY_DUMMY_LOGS.length > 300) {
                                    window.__SURVEY_DUMMY_LOGS = window.__SURVEY_DUMMY_LOGS.slice(-300);
                                }
                            } catch (e) {}
                        };

                        if (!window.__SURVEY_DUMMY_LOG_HOOKED) {
                            window.__SURVEY_DUMMY_LOG_HOOKED = true;
                            const origError = window.onerror;
                            window.onerror = function(message, source, lineno, colno, error) {
                                try {
                                    push('window.onerror', `${message || ''} @ ${source || ''}:${lineno || 0}:${colno || 0}`);
                                    if (error && error.stack) push('window.onerror.stack', String(error.stack));
                                } catch (e) {}
                                if (typeof origError === 'function') {
                                    try { return origError.apply(this, arguments); } catch (e) {}
                                }
                                return false;
                            };

                            window.addEventListener('unhandledrejection', function(ev) {
                                try {
                                    const reason = ev && ev.reason;
                                    const msg = reason && (reason.stack || reason.message) ? (reason.stack || reason.message) : String(reason || '');
                                    push('unhandledrejection', msg);
                                } catch (e) {}
                            });
                        }
                    } catch (e) {}
                    }"""
                )
            except Exception:
                pass

            try:
                page.evaluate(
                    """() => {
                    try {
                        if (!window.__SURVEY_DUMMY_LOGS) window.__SURVEY_DUMMY_LOGS = [];
                    } catch (e) {}
                    }"""
                )
            except Exception:
                pass

        def _handle_dialog(dialog):
            msg = ""
            dtype = ""
            try:
                msg = dialog.message or ""
            except Exception:
                msg = ""
            try:
                dtype = dialog.type or ""
            except Exception:
                dtype = ""

            logger.warning(f"[{idx}] dialog type={dtype or '?'} message={msg}")

            # 성공 알림(예: "성공적으로 업로드")은 validation 실패가 아니므로 last_alert에 기록하지 않음
            _SUCCESS_KEYWORDS = (
                "성공적으로",
                "업로드되었습니다",
                "successfully uploaded",
                "upload success",
            )
            is_success_msg = any(kw in msg for kw in _SUCCESS_KEYWORDS)

            if not is_success_msg:
                trace["last_alert"] = msg
                trace["last_dialog_type"] = dtype
            try:
                trace["alert_history"].append(msg)
            except Exception:
                pass

            try:
                dialog.accept()
            except Exception:
                try:
                    dialog.dismiss()
                except Exception:
                    pass

        def _handle_console(msg: ConsoleMessage):
            try:
                mtype = msg.type or "console"
            except Exception:
                mtype = "console"
            try:
                txt = msg.text or ""
            except Exception:
                txt = ""
            _push_browser_event(f"console.{mtype}", txt)

        def _handle_page_error(exc: PlaywrightError):
            _push_browser_event("pageerror", str(exc))

        def _handle_request_failed(req: Request):
            try:
                failure = req.failure() or {}
            except Exception:
                failure = {}
            err = ""
            try:
                err = str(failure.get("errorText") or "")
            except Exception:
                err = ""
            _push_browser_event("requestfailed", f"{req.method} {req.url} {err}".strip())

        page.on("dialog", _handle_dialog)
        page.on("console", _handle_console)
        page.on("pageerror", _handle_page_error)
        page.on("requestfailed", _handle_request_failed)

        _install_page_log_bridge()
        _install_next_probe(page)

        logger.info(f"[{idx}] START {cfg.start_url}")
        try:
            page.goto(cfg.start_url, wait_until="domcontentloaded")
        except Exception as e:
            logger.error(f"[{idx}] page.goto failed: {e}")
            trace["ok"] = False
            return False
        wait_nav_best_effort(page, timeout_ms=80)
        _install_page_log_bridge()
        _install_next_probe(page)

        for step in range(cfg.max_steps_per_response):
            is_stop_requested = getattr(cfg, "is_stop_requested", None)
            if is_stop_requested and is_stop_requested():
                logger.warning(f"[{idx}] User requested stop during run_one loop.")
                trace["final_url"] = page.url if not page.is_closed() else trace.get("final_url", "")
                try:
                    browser.close()
                except Exception:
                    pass
                break

            if (time.monotonic() - started_at) >= execution_timeout_sec:
                logger.error(f"[{idx}] Execution timeout exceeded ({execution_timeout_sec}s).")
                trace["final_url"] = page.url if not page.is_closed() else trace.get("final_url", "")
                try:
                    dump_snapshot(cfg, page, f"{idx:04d}_FAIL_TIMEOUT")
                except Exception:
                    pass
                try:
                    browser.close()
                except Exception:
                    pass
                break
            sleep_jitter(cfg)

            url, html, page_id_before = _current_page_state(page, timeout_ms=80)
            meta_before = parse_form_fields(html) if html else {"has_form": False}
            expected_next = ""
            form_action = ""
            if meta_before.get("has_form"):
                expected_next = (
                    meta_before.get("hidden", {}).get("NextPage")
                    or meta_before.get("hidden", {}).get("NPAGE")
                    or meta_before.get("hidden", {}).get("PAGE")
                    or ""
                )
                form_action = meta_before.get("form_action", "") or ""

            stop_at_page = getattr(cfg, "stop_at_page", None)
            if stop_at_page and (not visited_pages or visited_pages[-1] != page_id_before):
                logger.info(
                    f"[{idx}] stop_check stop={_norm_stop_token(stop_at_page)} "
                    f"page_id={_norm_stop_token(page_id_before)} url={url}"
                )

            if _hit_stop_page(page_id_before, url or "", stop_at_page):
                logger.info(
                    f"[{idx}] BREAKPOINT HIT stop_raw={stop_at_page} stop_norm={_norm_stop_token(stop_at_page)} "
                    f"page_id={page_id_before} url={url}"
                )
                trace["final_url"] = url
                trace["ok"] = True
                trace["completed"] = False
                trace["screen_hit"] = ("screen" in (url or "").lower())
                trace["breakpoint_hit"] = True
                trace["breakpoint_page_id"] = page_id_before
                trace["breakpoint_url"] = url

                if cfg.headless:
                    _switch_to_headed_and_hold(p, browser, context, page, cfg, logger)
                else:
                    _hold_visible_page(page, logger, max_seconds=getattr(cfg, "stop_hold_max_seconds", None))
                try:
                    browser.close()
                except Exception:
                    pass
                break

            if not visited_pages or visited_pages[-1] != page_id_before:
                visited_pages.append(page_id_before)

            if is_url_error(html, url):
                logger.error(f"[{idx}] URL ERROR url={url}")
                trace["screen_hit"] = ("screen" in (url or "").lower())
                trace["final_url"] = url
                try:
                    dump_snapshot(cfg, page, f"{idx:04d}_FAIL_URL_ERROR")
                except Exception:
                    pass
                browser.close()
                break

            if is_completed(html, url):
                logger.info(f"[{idx}] COMPLETED url={url}")
                trace["completed"] = True
                trace["ok"] = True
                trace["final_url"] = url
                browser.close()
                break

            autofill_page_by_dom(page, cfg, logger)
            _quick_settle_after_repair(page, cfg)
            _maybe_apply_next_constraints(page, cfg, logger)

            if verifier:
                try:
                    # Extract visible text from the page body
                    page_text_list = page.evaluate(
                        """() => {
                            const elements = document.querySelectorAll('p, span, div, label, td, th, li, h1, h2, h3, h4');
                            const texts = new Set();
                            elements.forEach(el => {
                                // Only get direct text nodes to avoid duplication from containers
                                Array.from(el.childNodes).forEach(node => {
                                    if (node.nodeType === Node.TEXT_NODE) {
                                        const txt = node.textContent.trim();
                                        if (txt.length > 2) {
                                            texts.add(txt);
                                        }
                                    }
                                });
                            });
                            return Array.from(texts);
                        }"""
                    )
                    verifier.verify_page(page_id_before, page_text_list)
                except Exception as e:
                    logger.warning(f"[{idx}] Verifier extraction failed: {e}")

            before_url = page.url
            before_sig = _page_signature(before_url, page_id_before)
            _log_submit_state_if_enabled(page, cfg, logger, idx, "submit_state")

            retry_alert_count = 0
            max_alert_retry = 3
            after_url = before_url
            after_html = html
            page_id_after = page_id_before

            while True:
                _, after_url, after_html, page_id_after = _trigger_submit(page, logger, idx, trace, phase="main", wait_ms=90)
                after_sig = _page_signature(after_url, page_id_after)
                hit_expected = bool(expected_next) and _norm_stop_token(page_id_after) == _norm_stop_token(expected_next)

                if trace.get("last_alert"):
                    logger.warning(f"[{idx}] validation alert detected: {trace['last_alert']}")
                    meta_alert = parse_form_fields(after_html) if after_html else {"has_form": False}
                    if retry_alert_count < max_alert_retry and meta_alert.get("has_form"):
                        repaired = repair_after_alert(page, meta_alert, cfg, logger, trace["last_alert"])
                        if repaired.get("changed"):
                            retry_alert_count += 1
                            logger.info(f"[{idx}] alert_retry={retry_alert_count} changed={repaired.get('changed')}")
                            _quick_settle_after_repair(page, cfg)
                            trace["last_alert"] = ""
                            after_url, after_html = _trigger_after_repair(page, logger, idx, trace=trace, timeout_ms=70)
                            page_id_after = extract_page_id(after_url, after_html)
                            after_sig = _page_signature(after_url, page_id_after)
                            if after_sig != before_sig or hit_expected:
                                break
                            continue
                    break

                if after_sig != before_sig or hit_expected:
                    break

                logger.warning(f"[{idx}] same-page after main submit -> one quick fallback")
                next_stats_before_fb = get_next_runtime_stats(page)
                click_result = try_click_next_timed(page)
                logger.info(
                    f"[{idx}] next_trigger fallback method={click_result.get('method') or '-'} "
                    f"duration_ms={float(click_result.get('duration_ms') or 0.0):.1f} "
                    f"clicked={bool(click_result.get('clicked'))} error={click_result.get('error') or '-'}"
                )
                next_stats_after_fb = get_next_runtime_stats(page)
                logger.info(f"[{idx}] next_runtime_fallback {_summarize_next_stat_delta(next_stats_before_fb, next_stats_after_fb)}")
                _wait_after_submit(page, trace, timeout_ms=70)
                after_url, after_html, page_id_after = _current_page_state(page, timeout_ms=70)
                after_sig = _page_signature(after_url, page_id_after)
                hit_expected = bool(expected_next) and _norm_stop_token(page_id_after) == _norm_stop_token(expected_next)
                if after_sig != before_sig or hit_expected or trace.get("last_alert"):
                    continue

                logger.warning(
                    f"[{idx}] URL unchanged and page unchanged. Validation-aware retry. "
                    f"(before={page_id_before}, after={page_id_after}, expected={expected_next or '-'})"
                )
                _log_submit_state_if_enabled(page, cfg, logger, idx, "stuck_submit_state")
                meta_same = parse_form_fields(after_html) if after_html else {"has_form": False}
                if meta_same.get("has_form"):
                    issues = diagnose_next_failures(page, meta_same, logger)
                    if issues:
                        logger.warning(f"[{idx}] stuck_diagnostics page={page_id_before} issues={issues}")
                    repaired = repair_after_alert(page, meta_same, cfg, logger, trace.get("last_alert", ""))
                    if repaired.get("changed"):
                        _quick_settle_after_repair(page, cfg)
                        trace["last_alert"] = ""
                        after_url, after_html = _trigger_after_repair(page, logger, idx, trace=trace, timeout_ms=70)
                        page_id_after = extract_page_id(after_url, after_html)
                break

            page_id_after = extract_page_id(after_url, after_html)
            edge = f"{page_id_before}->{page_id_after}"
            visited_edges.append(edge)
            logger.info(
                f"[{idx}] step={step} {page_id_before} -> {page_id_after} "
                f"(expected_next={expected_next or '-'} action={form_action or '-'} url={before_url} -> {after_url})"
            )

            same_url = after_url == before_url
            same_page = _norm_stop_token(page_id_after) == _norm_stop_token(page_id_before)
            hit_expected = bool(expected_next) and _norm_stop_token(page_id_after) == _norm_stop_token(expected_next)

            if same_url and same_page and not hit_expected:
                try:
                    next_src = page.evaluate(
                        """() => {
                            try {
                                return (typeof window.next === 'function') ? String(window.next) : '';
                            } catch (e) {
                                return '';
                            }
                        }"""
                    ) or ""
                    if next_src:
                        logger.warning(f"[{idx}] next_source_excerpt={next_src[:4000]}")
                except Exception as e:
                    logger.warning(f"[{idx}] next_source_excerpt log failed: {e}")

                try:
                    browser_hist = page.evaluate(
                        """() => {
                            try {
                                const arr = Array.isArray(window.__SURVEY_DUMMY_LOGS) ? window.__SURVEY_DUMMY_LOGS : [];
                                return arr.slice(-100).map(x => `[${x.ts || ''}] [${x.kind || ''}] ${x.message || ''}`);
                            } catch (e) {
                                return [];
                            }
                        }"""
                    ) or []
                    if browser_hist:
                        logger.warning(f"[{idx}] browser_log_tail=" + " | ".join([str(x) for x in browser_hist][-50:]))
                except Exception as e:
                    logger.warning(f"[{idx}] browser_log_tail log failed: {e}")

                logger.error(f"[{idx}] Stuck on same page. step={step} url={page.url}")
                trace["final_url"] = page.url
                try:
                    dump_snapshot(cfg, page, f"{idx:04d}_FAIL_STUCK")
                except Exception:
                    pass
                browser.close()
                break

        else:
            logger.error(f"[{idx}] Max steps exceeded.")
            trace["final_url"] = page.url
            try:
                dump_snapshot(cfg, page, f"{idx:04d}_FAIL_MAX_STEPS")
            except Exception:
                pass
            browser.close()

    trace["visited_pages"] = visited_pages
    trace["visited_edges"] = visited_edges
    write_json(os.path.join(cfg.out_dir, "coverage_trace.json"), trace)
    return bool(trace["ok"])


# backward-compatible alias
def run_one_sync(cfg: RunnerConfig, logger: logging.Logger, idx: int, verifier=None) -> bool:
    return run_one(cfg, logger, idx, verifier)
