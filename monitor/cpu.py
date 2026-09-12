import psutil
from typing import List


def get_cpu_percent(interval: float = 0.5) -> float:
    """Return overall CPU usage percentage."""
    return psutil.cpu_percent(interval=interval)


def get_per_cpu_percent(interval: float = 0.5) -> List[float]:
    """Return per-core CPU usage percentages."""
    return psutil.cpu_percent(interval=interval, percpu=True)


def get_cpu_freq():
    """Return CPU frequency info."""
    freq = psutil.cpu_freq()
    if freq:
        return {
            "current": round(freq.current, 0),
            "min": freq.min,
            "max": freq.max,
        }
    return None
