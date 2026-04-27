from __future__ import annotations

import logging
import os
import threading

from runner.logger import setup_logger

_LOCK = threading.Lock()


def get_admin_ips() -> set[str]:
    raw = os.getenv("ADMIN_IPS", "").strip()
    s = {x.strip() for x in raw.split(",") if x.strip()}
    s.update({"127.0.0.1", "::1"})
    return s


ADMIN_IPS = get_admin_ips()


def ip_to_dirname(ip: str) -> str:
    return str(ip or "unknown").replace(":", "_").replace(".", "_")


def _normalize_path(path: str) -> str:
    return os.path.abspath(path)


def _find_file_handler(logger: logging.Logger, path: str) -> logging.Handler | None:
    target = _normalize_path(path)
    for handler in logger.handlers:
        base = getattr(handler, "baseFilename", None)
        if base and _normalize_path(str(base)) == target:
            return handler
    return None


def _ensure_file_handler(logger: logging.Logger, path: str, formatter: logging.Formatter) -> logging.Handler:
    existing = _find_file_handler(logger, path)
    if existing is not None:
        existing.setFormatter(formatter)
        return existing

    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return fh


def setup_logger_dual(out_dir: str, client_ip: str, run_id: str | None = None):
    os.makedirs(out_dir, exist_ok=True)
    logger = setup_logger(out_dir=out_dir, client_ip=client_ip, run_id=run_id)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    all_path = os.path.join(out_dir, "run_all.log")
    client_dir = os.path.join(out_dir, "clients", ip_to_dirname(client_ip))
    os.makedirs(client_dir, exist_ok=True)
    client_path = os.path.join(client_dir, "run.log")

    with _LOCK:
        _ensure_file_handler(logger, all_path, fmt)
        _ensure_file_handler(logger, client_path, fmt)

    return logger
