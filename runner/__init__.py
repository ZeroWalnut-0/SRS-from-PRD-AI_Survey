from .config import RunnerConfig

__all__ = ["RunnerConfig", "run_one"]

def run_one(*args, **kwargs):
    from .core import run_one as _run_one
    return _run_one(*args, **kwargs)
