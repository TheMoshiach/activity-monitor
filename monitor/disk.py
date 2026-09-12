import psutil
from typing import List


def get_disk_partitions() -> List[dict]:
    """Return mounted disk partitions with usage stats."""
    partitions = []
    for part in psutil.disk_partitions(all=False):
        if part.fstype == "":
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except PermissionError:
            continue
    return partitions
