from __future__ import annotations

import re
from urllib.parse import urlparse


_COMPLETION_URL_PATTERNS = (
    "survey_end.asp",
    "survey_close.asp",
    "complete.asp",
    "finish.asp",
)
_COMPLETION_TEXT_PATTERNS = (
    "설문 완료",
    "참여해 주셔서 감사합니다",
    "응답해 주셔서 감사합니다",
    "thank you for completing",
    "survey completed",
)
_ERROR_URL_PATTERNS = (
    "urlerror.asp",
    "screenout.asp",
    "quotaout.asp",
)
_ERROR_TEXT_PATTERNS = (
    "정상적인 경로로 설문조사에 참여하지 않으셨습니다",
    "응답 quota가 모두 찼습니다",
    "할당이 종료되었습니다",
    "screen out",
    "quota full",
)


def _normalize_html_text(html: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", html or "", flags=re.I | re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def _url_path(url: str) -> str:
    try:
        return (urlparse(url or "").path or "").lower()
    except Exception:
        return (url or "").lower()


def _has_next_action_button(html: str) -> bool:
    """
    페이지에 '다음' 진행 버튼이 존재하면 True.
    INFO_END처럼 감사 문구가 있어도 다음 버튼이 있으면 아직 진행 가능한 페이지다.
    확인 기준:
      - <button...>다음</button>  (버튼 텍스트)
      - id="next"  (설문 페이지 표준 버튼 ID)
      - class="...btn-bottom..."  (공통 레이아웃 클래스)
    """
    h = html or ""
    # 버튼 텍스트 "다음"
    if re.search(r'<button[^>]*>\s*다음\s*</button', h, flags=re.I | re.S):
        return True
    # id="next" 버튼
    if re.search(r'<button[^>]+id=["\']next["\']', h, flags=re.I):
        return True
    # btn-bottom 클래스 (이 프로젝트 공통 레이아웃)
    if re.search(r'<button[^>]+class=["\'][^"\']*btn-bottom[^"\']*["\']', h, flags=re.I):
        return True
    return False


def is_completed(html: str, url: str) -> bool:
    path = _url_path(url)
    text = _normalize_html_text(html)

    strong_url = any(token in path for token in _COMPLETION_URL_PATTERNS)

    # strong URL(survey_end.asp 등)은 무조건 완료로 확정
    if strong_url:
        return True

    # '다음' 버튼이 보이면 아직 진행 가능한 페이지 → 완료 판단 건너뜀
    # (INFO_END처럼 감사 문구가 있어도 버튼이 있으면 중간 페이지)
    if _has_next_action_button(html):
        return False

    thank_you_text = any(token in text for token in _COMPLETION_TEXT_PATTERNS)
    no_form = "<form" not in (html or "").lower()

    weak_hits = 0
    if thank_you_text:
        weak_hits += 1
    if no_form:
        weak_hits += 1
    if re.search(r"\b(complete|completed|finish|finished)\b", path):
        weak_hits += 1

    return weak_hits >= 2


def is_url_error(html: str, url: str) -> bool:
    path = _url_path(url)
    text = _normalize_html_text(html)

    strong_url = any(token in path for token in _ERROR_URL_PATTERNS)
    strong_text = any(token in text for token in _ERROR_TEXT_PATTERNS)

    weak_hits = 0
    if strong_text:
        weak_hits += 1
    if re.search(r"(screen|quota)(?:[_-]?(?:out|error))?\.asp", path):
        weak_hits += 1
    if re.search(r"(screen out|quota out|invalid path|url error)", text):
        weak_hits += 1

    if strong_url:
        return True
    return weak_hits >= 2
