from __future__ import annotations

import html as html_lib
import os
from urllib.parse import urlparse

from playwright.sync_api import Page

from .config import RunnerConfig
from .utils import safe_filename
from .dom_actions import wait_nav_best_effort
from .form_parse import parse_form_fields
from .next_logic import diagnose_next_failures, extract_next_source


def _safe_title(page: Page) -> str:
    try:
        return page.title() or ""
    except Exception:
        return ""


def _safe_content(page: Page) -> str:
    try:
        return page.content() or ""
    except Exception:
        try:
            wait_nav_best_effort(page)
            return page.content() or ""
        except Exception:
            return ""


def _safe_text_excerpt(page: Page, max_len: int = 5000) -> str:
    try:
        txt = page.evaluate(
            """() => {
                try {
                    const el = document.body || document.documentElement;
                    return (el && (el.innerText || el.textContent) || "").trim();
                } catch(e) {
                    return "";
                }
            }"""
        ) or ""
        txt = str(txt).strip()
        if len(txt) > max_len:
            txt = txt[:max_len] + "\n...(truncated)"
        return txt
    except Exception:
        return ""



def _safe_form_snapshot(page: Page, max_items: int = 300) -> str:
    try:
        data = page.evaluate(
            """(maxItems) => {
                try {
                    const f = document.querySelector("form[name='Survey']") || document.querySelector("form");
                    if (!f) {
                        return {
                            has_form: false,
                            action: "",
                            method: "",
                            data: {}
                        };
                    }

                    const fd = new FormData(f);
                    const out = {};
                    let count = 0;

                    for (const [k, v] of fd.entries()) {
                        count += 1;
                        if (count > maxItems) break;

                        const sv = String(v);
                        if (Object.prototype.hasOwnProperty.call(out, k)) {
                            if (Array.isArray(out[k])) out[k].push(sv);
                            else out[k] = [String(out[k]), sv];
                        } else {
                            out[k] = sv;
                        }
                    }

                    return {
                        has_form: true,
                        action: f.getAttribute("action") || "",
                        method: (f.getAttribute("method") || "get").toUpperCase(),
                        data: out,
                        truncated: count > maxItems
                    };
                } catch (e) {
                    return {
                        has_form: false,
                        error: String(e && e.message ? e.message : e)
                    };
                }
            }""",
            max_items,
        )
    except Exception as e:
        return f"(form snapshot unavailable)\n{e}"

    if not isinstance(data, dict):
        return "(form snapshot unavailable)"

    try:
        if not data.get("has_form"):
            if data.get("error"):
                return f"(no form / error) {data.get('error')}"
            return "(no form found)"

        action = str(data.get("action") or "")
        method = str(data.get("method") or "")
        items = data.get("data") or {}
        lines = [f"method={method}", f"action={action}", "", "[form data]"]

        if isinstance(items, dict):
            for k in sorted(items.keys(), key=lambda x: str(x)):
                lines.append(f"{k} = {items[k]}")

        if data.get("truncated"):
            lines.append("...(truncated)")

        return "\n".join(lines).strip()
    except Exception as e:
        return f"(form snapshot render failed)\n{e}"



def _safe_browser_log_snapshot(page: Page, max_items: int = 120) -> str:
    try:
        rows = page.evaluate(
            """(maxItems) => {
                try {
                    const arr = Array.isArray(window.__SURVEY_DUMMY_LOGS) ? window.__SURVEY_DUMMY_LOGS : [];
                    return arr.slice(-maxItems).map(x => ({
                        ts: String((x && x.ts) || ''),
                        kind: String((x && x.kind) || ''),
                        message: String((x && x.message) || '')
                    }));
                } catch (e) {
                    return [];
                }
            }""",
            max_items,
        ) or []
    except Exception as e:
        return f"(browser log unavailable)\n{e}"

    if not isinstance(rows, list) or not rows:
        return "(no browser log entries)"

    lines: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ts = str(row.get("ts") or "")
        kind = str(row.get("kind") or "")
        msg = str(row.get("message") or "")
        lines.append(f"[{ts}] [{kind}] {msg}".strip())
    return "\n".join(lines).strip() or "(no browser log entries)"



def _safe_failure_question_log(page: Page, raw_html: str) -> str:
    meta = parse_form_fields(raw_html or "") if raw_html else {"has_form": False}
    if not meta.get("has_form"):
        return "(no failed-question log available)"

    class _SnapshotLogger:
        def __init__(self):
            self.lines: list[str] = []

        def warning(self, *args, **kwargs):
            self._push(*args)

        def info(self, *args, **kwargs):
            self._push(*args)

        def _push(self, *args):
            try:
                msg = " ".join(str(x) for x in args if x is not None).strip()
            except Exception:
                msg = ""
            if msg:
                self.lines.append(msg)

    sink = _SnapshotLogger()
    try:
        issues = diagnose_next_failures(page, meta, sink) or []
    except Exception as e:
        return f"(failed-question diagnostics unavailable)\n{e}"

    parts: list[str] = []
    if issues:
        parts.append("[failed question issues]")
        parts.extend(str(x) for x in issues)

    if sink.lines:
        if parts:
            parts.append("")
        parts.append("[failed question logs]")
        parts.extend(sink.lines)

    return "\n".join(parts).strip() or "(no failed-question log available)"



def _safe_next_diagnostics(page: Page, raw_html: str) -> tuple[str, str]:
    src = ""
    issues_text = ""
    try:
        src = extract_next_source(page) or ""
    except Exception:
        src = ""

    try:
        meta = parse_form_fields(raw_html or "") if raw_html else {"has_form": False}
        if meta.get("has_form"):
            class _SnapshotLogger:
                def warning(self, *args, **kwargs):
                    return None
                def info(self, *args, **kwargs):
                    return None
            issues = diagnose_next_failures(page, meta, _SnapshotLogger()) or []
            if issues:
                issues_text = "\n".join(str(x) for x in issues)
    except Exception as e:
        issues_text = f"(next diagnostics unavailable)\n{e}"

    if src and len(src) > 12000:
        src = src[:12000] + "\n...(truncated)"
    return src.strip(), (issues_text.strip() or "(no next() issues detected)")



def dump_snapshot(cfg: RunnerConfig, page: Page, prefix: str):
    url = ""
    try:
        url = page.url or ""
    except Exception:
        url = ""

    base = f"{prefix}_{safe_filename(urlparse(url).path or 'page')}"
    os.makedirs(cfg.out_dir, exist_ok=True)
    path = os.path.join(cfg.out_dir, base + ".html")

    title = _safe_title(page)
    raw_html = _safe_content(page)
    text_excerpt = _safe_text_excerpt(page)
    form_snapshot = _safe_form_snapshot(page)
    browser_log_snapshot = _safe_browser_log_snapshot(page)
    failed_question_log = _safe_failure_question_log(page, raw_html)
    next_source, next_issues = _safe_next_diagnostics(page, raw_html)

    wrapped = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>Failure Snapshot</title>
  <style>
    body {{ font-family: Arial, 'Malgun Gothic', sans-serif; margin: 24px; line-height: 1.5; color:#222; background:#fafafa; }}
    .box {{ background:#fff; border:1px solid #ddd; border-radius:10px; padding:16px; margin-bottom:16px; }}
    pre {{ white-space:pre-wrap; word-break:break-word; background:#f6f6f6; border:1px solid #e2e2e2; border-radius:8px; padding:12px; overflow:auto; }}
  </style>
</head>
<body>
  <div class="box">
    <h2 style="margin-top:0;">Failure Snapshot</h2>
    <div><b>URL</b> {html_lib.escape(url)}</div>
    <div><b>Title</b> {html_lib.escape(title)}</div>
  </div>
  <div class="box">
    <h3 style="margin-top:0;">Visible Text Excerpt</h3>
    <pre>{html_lib.escape(text_excerpt or '(empty text)')}</pre>
  </div>
  <div class="box">
    <details open>
      <summary><b>Form Snapshot</b></summary>
      <pre>{html_lib.escape(form_snapshot or '(empty form snapshot)')}</pre>
    </details>
  </div>
  <div class="box">
    <details open>
      <summary><b>Failed Question Log</b></summary>
      <pre>{html_lib.escape(failed_question_log or '(no failed question log)')}</pre>
    </details>
  </div>
  <div class="box">
    <details open>
      <summary><b>Browser Log Snapshot</b></summary>
      <pre>{html_lib.escape(browser_log_snapshot or '(empty browser log)')}</pre>
    </details>
  </div>
  <div class="box">
    <details open>
      <summary><b>next() Diagnostics</b></summary>
      <pre>{html_lib.escape(next_issues or '(no diagnostics)')}</pre>
    </details>
  </div>
  <div class="box">
    <details open>
      <summary><b>next() Source</b></summary>
      <pre>{html_lib.escape(next_source or '(next() not found)')}</pre>
    </details>
  </div>
  <div class="box">
    <details open>
      <summary><b>Raw HTML (escaped)</b></summary>
      <pre>{html_lib.escape(raw_html or '(empty html)')}</pre>
    </details>
  </div>
</body>
</html>"""

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(wrapped)
    except Exception:
        pass

    return path
