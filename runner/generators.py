from __future__ import annotations
import re
import random
from typing import Optional, List

from .config import RunnerConfig


def clamp_len(s: str, maxlen: Optional[int]) -> str:
    if maxlen and maxlen > 0:
        return s[:maxlen]
    return s


def choose_select_value(values: List[str], cfg: RunnerConfig) -> Optional[str]:
    candidates = [v for v in values if v not in cfg.skip_select_values]
    if candidates:
        return random.choice(candidates)
    return values[0] if values else None


def _is_mobile_field(name: Optional[str], iid: Optional[str]) -> bool:
    s = f"{name or ''} {iid or ''}".lower()
    return bool(re.search(r"(dq5|mobile|phone|hand|hp|cell|tel)", s))


def _format_kr_mobile() -> str:
    prefixes = ["010", "011", "016", "017", "018", "019"]
    pre = random.choice(prefixes)
    mid_len = 4 if pre == "010" else random.choice([3, 4])
    mid = "".join(str(random.randint(0, 9)) for _ in range(mid_len))
    last = "".join(str(random.randint(0, 9)) for _ in range(4))
    return f"{pre}-{mid}-{last}"


def generate_tel_digits(
    maxlen: Optional[int],
    pattern: Optional[str] = None,
    name: Optional[str] = None,
    iid: Optional[str] = None,
) -> str:
    if _is_mobile_field(name, iid) or maxlen == 13:
        s = _format_kr_mobile()
        if maxlen and len(s) > maxlen:
            digits = re.sub(r"\D", "", s)
            return digits[:maxlen]
        return s

    if maxlen == 1:
        return str(random.randint(0, 9))
    n = maxlen if (maxlen and maxlen > 0) else 11
    if n <= 0:
        n = 11
    first = str(random.randint(1, 9)) if n > 1 else str(random.randint(0, 9))
    rest = "".join(str(random.randint(0, 9)) for _ in range(max(0, n - 1)))
    return first + rest


def generate_number(maxlen: Optional[int]) -> str:
    s = str(random.randint(1, 5))
    return clamp_len(s, maxlen)


def generate_email(maxlen: Optional[int], name: Optional[str] = None) -> str:
    base_tokens = ["user", "panel", "survey", "sample", "tester"]
    token = random.choice(base_tokens)
    if name:
        nm = re.sub(r"[^a-z0-9]+", "", str(name).lower())
        if nm:
            token = nm[:12]
    s = f"{token}{random.randint(100,9999)}@example.com"
    return clamp_len(s, maxlen)


_REASON_TEXTS = [
    "가격이 적절해서",
    "사용하기 편해서",
    "접근성이 좋아서",
    "필요한 기능이 있어서",
    "평소에 익숙해서",
]

_COMPLAINT_TEXTS = [
    "대기 시간이 길었습니다",
    "원하는 정보가 부족했습니다",
    "사용 방법이 조금 어려웠습니다",
    "가격이 다소 부담되었습니다",
    "선택지가 더 다양했으면 좋겠습니다",
]

_OPINION_TEXTS = [
    "전반적으로 만족합니다",
    "대체로 무난했습니다",
    "전반적으로 이용이 편리했습니다",
    "특별히 불편한 점은 없었습니다",
    "기회가 되면 다시 이용할 의향이 있습니다",
]

_ROUTE_TEXTS = [
    "온라인 검색",
    "지인 추천",
    "광고를 보고 알게 됨",
    "매장 방문 중 알게 됨",
    "SNS를 통해 알게 됨",
]

_ETC_TEXTS = [
    "기타",
    "해당 없음",
    "특별한 이유 없음",
    "기억나지 않음",
    "직접 입력",
]

_JOB_TEXTS = [
    "사무직",
    "전문직",
    "서비스직",
    "자영업",
    "학생",
]

_REGION_TEXTS = [
    "서울",
    "경기",
    "인천",
    "부산",
    "대전",
]

_BRAND_TEXTS = [
    "삼성",
    "애플",
    "LG",
    "나이키",
    "유니클로",
]

_PRODUCT_TEXTS = [
    "스마트폰",
    "의류",
    "식품",
    "생활용품",
    "가전제품",
]

_NAME_TEXTS = ["김민수", "이서준", "박지윤", "최유진", "정하윤"]


def _normalize_context(*parts: Optional[str]) -> str:
    text = " ".join(str(x or "") for x in parts)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def _matches_any(ctx: str, keywords: List[str]) -> bool:
    return any(k in ctx for k in keywords)


def _pick_text_by_context(ctx: str, multiline: bool = False) -> str:
    if _matches_any(ctx, ["이름", "성명", "name"]):
        return random.choice(_NAME_TEXTS)
    if _matches_any(ctx, ["직업", "occupation", "job"]):
        return random.choice(_JOB_TEXTS)
    if _matches_any(ctx, ["지역", "거주", "시/도", "주소", "region", "city"]):
        return random.choice(_REGION_TEXTS)
    if _matches_any(ctx, ["브랜드", "brand"]):
        return random.choice(_BRAND_TEXTS)
    if _matches_any(ctx, ["제품", "상품", "품목", "product"]):
        return random.choice(_PRODUCT_TEXTS)
    if _matches_any(ctx, ["경로", "어디서", "알게", "인지", "유입", "route", "channel", "source"]):
        return random.choice(_ROUTE_TEXTS)
    if _matches_any(ctx, ["추천", "recommend"]):
        return random.choice(["주변에 추천할 의향이 있습니다", "전반적으로 추천할 만합니다", "상황에 따라 추천할 수 있습니다"])
    if _matches_any(ctx, ["이유", "사유", "왜", "reason"]):
        return random.choice(_REASON_TEXTS)
    if _matches_any(ctx, ["불편", "불만", "개선", "문제", "아쉬", "complaint", "issue"]):
        return random.choice(_COMPLAINT_TEXTS)
    if _matches_any(ctx, ["의견", "소감", "평가", "comment", "review", "opinion"]):
        return random.choice(_OPINION_TEXTS)
    if _matches_any(ctx, ["기타", "etc", "other", "직접입력"]):
        return random.choice(_ETC_TEXTS)

    if multiline:
        return random.choice(_OPINION_TEXTS + _REASON_TEXTS + _COMPLAINT_TEXTS)
    return random.choice(_ETC_TEXTS + ["없음", "보통", "해당 없음"])


_SIMPLE_PATTERN_MAP = [
    (re.compile(r"^\d\{4\}$"), lambda: f"{random.randint(2000, 2025):04d}"),
    (re.compile(r"^\d\{2\}$"), lambda: f"{random.randint(1, 12):02d}"),
    (re.compile(r"^\d\{1,2\}$"), lambda: str(random.randint(1, 12))),
    (re.compile(r"^[a-zA-Z]\{2\}$"), lambda: random.choice(["AB", "CD", "EF", "GH"])),
]


def _generate_from_simple_pattern(pattern: Optional[str]) -> Optional[str]:
    if not pattern:
        return None
    p = str(pattern).strip().strip("^").strip("$")
    for rx, fn in _SIMPLE_PATTERN_MAP:
        if rx.match(p):
            return fn()
    if re.fullmatch(r"\[0-9\]\*", p) or re.fullmatch(r"\[0-9\]\+", p):
        return str(random.randint(10, 9999))
    return None



def generate_text(
    maxlen: Optional[int],
    name: Optional[str] = None,
    iid: Optional[str] = None,
    pattern: Optional[str] = None,
    context_text: Optional[str] = None,
    multiline: bool = False,
) -> str:
    pat_val = _generate_from_simple_pattern(pattern)
    if pat_val:
        return clamp_len(pat_val, maxlen)

    ctx = _normalize_context(name, iid, context_text)
    s = _pick_text_by_context(ctx, multiline=multiline)

    if maxlen is not None and maxlen > 0:
        if len(s) > maxlen:
            s = s[:maxlen]
        elif multiline and maxlen >= 12 and len(s) < min(12, maxlen):
            extras = [
                "전반적으로 만족합니다",
                "필요한 점은 충족되었습니다",
                "추가 개선이 있으면 더 좋겠습니다",
            ]
            for extra in extras:
                merged = f"{s}. {extra}" if s else extra
                if len(merged) <= maxlen:
                    s = merged
                    break

    return clamp_len(s, maxlen)
