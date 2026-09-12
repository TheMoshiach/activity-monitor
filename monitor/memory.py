import psutil


def get_memory_stats() -> dict:
    """Return virtual memory stats."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "free": mem.free,
        "percent": mem.percent,
        "active": getattr(mem, "active", 0),
        "inactive": getattr(mem, "inactive", 0),
    }


def get_swap_stats() -> dict:
    """Return swap memory stats."""
    swap = psutil.swap_memory()
    return {
        "total": swap.total,
        "used": swap.used,
        "free": swap.free,
        "percent": swap.percent,
    }
