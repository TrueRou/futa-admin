from typing import Any


def safe_execute(func, default: Any, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return default
