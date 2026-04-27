from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Optional

@dataclass
class RunnerConfig:
    start_url: str
    n_responses: int = 1
    max_steps_per_response: int = 200

    min_delay_sec: float = 0.03
    max_delay_sec: float = 0.10

    out_dir: str = "run_logs_pw"
    headless: bool = False
    navigation_timeout_ms: int = 60_000
    execution_timeout_sec: int = 3600

    checkbox_select_all: bool = False

    # Rank(순위) 문항 처리
    # - True: 최대 순위(need)까지 모두 선택
    # - False: 일부만 랜덤 선택 (rank_pick_min~rank_pick_max)
    rank_select_all: bool = False
    rank_pick_min: int = 1
    # 0이면 '제한 없음' -> need(순위 슬롯 수)로 해석
    rank_pick_max: int = 0

    checkbox_click_gap_min: float = 0.01
    checkbox_click_gap_max: float = 0.04

    skip_select_values: Tuple[str, ...] = ("", "0")

    other_text_default: str = "모름"

    # 케이스 기반 오버라이드 (app.py에서 주입)
    case_overrides: Optional[Dict[str, Any]] = None

    # =========================
    # Breakpoint / Manual takeover
    # =========================
    # 예: "SQ3" 또는 "SQ3.asp" -> SQ3.asp 도달 시 멈춤
    stop_at_page: str | None = None

    # None이면 사용자가 창 닫을 때까지 무제한 대기
    stop_hold_max_seconds: int | None = None

    # =========================
    # Fast-path execution
    # =========================
    # 다음 클릭 전 짧은 안정화 대기(ms)
    pre_next_click_delay_ms: int = 25

    # 일반 step에서 next() JS 제약 보정은 생략하고,
    # alert/같은 페이지 재시도 시점에만 수행
    apply_next_constraints_before_click: bool = False

    # submit 직전 FormData 덤프 로그 (느릴 수 있어 기본 OFF)
    log_submit_state: bool = False
