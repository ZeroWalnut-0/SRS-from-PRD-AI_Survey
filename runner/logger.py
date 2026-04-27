from __future__ import annotations

import logging
import os
import threading
from typing import Optional

_LOGGER_LOCK = threading.Lock()
_DEFAULT_FORMAT = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")


def _logger_name(out_dir: str, client_ip: Optional[str] = None, run_id: Optional[str] = None) -> str:
    safe_dir = os.path.abspath(out_dir or "run_logs_pw")
    parts = ["survey_pw_autofill", safe_dir]
    if client_ip:
        parts.append(str(client_ip))
    if run_id:
        parts.append(str(run_id))
    return "|".join(parts)


def _normalize_path(path: str) -> str:
    return os.path.abspath(path)


def _file_handler_key(path: str) -> tuple[str, str]:
    return ("file", _normalize_path(path))


def _stream_handler_key() -> tuple[str, str]:
    return ("stream", "stderr")


def _set_handler_key(handler: logging.Handler, key: tuple[str, str]) -> None:
    setattr(handler, "_survey_handler_key", key)


def _get_handler_key(handler: logging.Handler):
    return getattr(handler, "_survey_handler_key", None)


def _find_handler(logger: logging.Logger, key: tuple[str, str]) -> Optional[logging.Handler]:
    for handler in logger.handlers:
        if _get_handler_key(handler) == key:
            return handler
    return None


def _ensure_file_handler(logger: logging.Logger, path: str, formatter: logging.Formatter) -> logging.Handler:
    key = _file_handler_key(path)
    existing = _find_handler(logger, key)
    if existing is not None:
        existing.setFormatter(formatter)
        return existing

    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(formatter)
    _set_handler_key(fh, key)
    logger.addHandler(fh)
    return fh


def _ensure_stream_handler(logger: logging.Logger, formatter: logging.Formatter) -> logging.Handler:
    key = _stream_handler_key()
    existing = _find_handler(logger, key)
    if existing is not None:
        existing.setFormatter(formatter)
        return existing

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    _set_handler_key(sh, key)
    logger.addHandler(sh)
    return sh


def setup_logger(out_dir: str, client_ip: Optional[str] = None, run_id: Optional[str] = None) -> logging.Logger:
    os.makedirs(out_dir, exist_ok=True)
    name = _logger_name(out_dir=out_dir, client_ip=client_ip, run_id=run_id)

    with _LOGGER_LOCK:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        run_log_path = os.path.join(out_dir, "run.log")
        _ensure_file_handler(logger, run_log_path, _DEFAULT_FORMAT)
        _ensure_stream_handler(logger, _DEFAULT_FORMAT)
        return logger
