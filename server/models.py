from __future__ import annotations
import threading
import time
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobState:
    def __init__(self):
        self.lock = threading.Lock()
        self.running: bool = False
        self.job_id: Optional[str] = None
        self.started_at: Optional[float] = None
        self.finished_at: Optional[float] = None
        self.ok: Optional[bool] = None
        self.error: Optional[str] = None
        self.stop_requested: bool = False
        self.out_dir: str = "run_logs_pw"
        self.mode: str = ""
        self.planned_total: int = 0
        self.current_run: int = 0
        self.remaining_cases: int = 0
        self.progress: int = 0
        self.message: str = ""
        self.asp_logic: str = ""
        self.concurrency: int = 5
        self.execution_timeout_sec: int = 3600
        self.ref_doc_path: Optional[str] = None

    @staticmethod
    def make_job_id() -> str:
        return datetime.now().strftime("job_%Y%m%d_%H%M%S_%f")

    def reset_for_start(self, job_id: str, out_dir: str):
        self.running = True
        self.job_id = job_id
        self.started_at = time.time()
        self.finished_at = None
        self.ok = None
        self.error = None
        self.stop_requested = False
        self.out_dir = out_dir
        self.mode = ""
        self.planned_total = 0
        self.current_run = 0
        self.remaining_cases = 0
        self.progress = 0
        self.message = "starting"
        self.ref_doc_path = None

    def finish(self, ok: bool, error: Optional[str] = None):
        self.running = False
        self.finished_at = time.time()
        self.ok = ok
        self.error = error
        self.progress = 100 if ok else self.progress


class RunRequest(BaseModel):
    mode: str = "random"  # "random" | "coverage"
    tie_break: str = "stable"  # "stable" | "random"
    asp_logic: str = ""
    max_cases: int = 50

    auto_until_done: bool = True
    max_total_runs: int = 200
    persist_state: bool = True
    include_default_paths: bool = True
    include_screen_cases: bool = False

    test_url: str = Field(..., min_length=5)
    repeat: int = Field(1, ge=1, le=500)
    concurrency: int = Field(5, ge=1, le=10)

    headless: bool = False
    out_dir: str = "run_logs_pw"
    ref_doc_path: Optional[str] = None

    max_steps_per_response: int = 200
    min_delay_sec: float = 0.15
    max_delay_sec: float = 0.45
    execution_timeout_sec: int = Field(3600, ge=1)

    checkbox_select_all: bool = False

    rank_select_all: bool = False
    rank_pick_min: int = 1
    rank_pick_max: int = 0

    other_text_default: str = "모름"
    navigation_timeout_ms: int = 60_000

    stop_at_page: str | None = None
    stop_hold_max_seconds: int | None = None

    pre_next_click_delay_ms: int = 25
    apply_next_constraints_before_click: bool = False
    log_submit_state: bool = False

class ResetRequest(BaseModel):
    asp_logic: str = ""
    out_dir: str = "run_logs_pw"
    # test_url은 프론트에서 넘어올 수 있으나 validation을 하지 않음
    test_url: str = ""

