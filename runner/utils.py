from __future__ import annotations
import re
import os
import json
import time
import random
from typing import Any, Optional
from urllib.parse import urlparse

from .config import RunnerConfig

def sleep_jitter(cfg: RunnerConfig):
    time.sleep(random.uniform(cfg.min_delay_sec, cfg.max_delay_sec))

def safe_filename(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", s)[:160]

def click_gap(cfg: RunnerConfig):
    time.sleep(random.uniform(cfg.checkbox_click_gap_min, cfg.checkbox_click_gap_max))

def write_json(path: str, obj: Any):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def url_path_stem(url: str) -> str:
    try:
        path = urlparse(url).path or ""
        stem = os.path.splitext(os.path.basename(path))[0]
        return stem
    except Exception:
        return ""
