import psutil
from typing import List


def get_top_processes(sort_by: str = "cpu", limit: int = 15) -> List[dict]:
    """Return top processes sorted by cpu or memory."""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "username", "cpu_percent", "memory_percent", "memory_info", "status"]):
        try:
            info = proc.info
            processes.append({
                "pid": info["pid"],
                "name": info["name"] or "",
                "username": info["username"] or "",
                "cpu_percent": info["cpu_percent"] or 0.0,
                "memory_percent": info["memory_percent"] or 0.0,
                "memory_rss": info["memory_info"].rss if info["memory_info"] else 0,
                "status": info["status"],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if sort_by == "cpu":
        processes.sort(key=lambda x: x["cpu_percent"], reverse=True)
    elif sort_by == "memory":
        processes.sort(key=lambda x: x["memory_percent"], reverse=True)
    elif sort_by == "pid":
        processes.sort(key=lambda x: x["pid"], reverse=False)
    elif sort_by == "name":
        processes.sort(key=lambda x: x["name"].lower(), reverse=False)

    return processes[:limit]
