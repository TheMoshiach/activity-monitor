import psutil
import time
from typing import Dict


class NetworkTracker:
    """Track network I/O and calculate speeds."""

    def __init__(self):
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        self.last_time = time.time()
        self._init_counters()

    def _init_counters(self):
        counters = psutil.net_io_counters()
        self.last_bytes_sent = counters.bytes_sent
        self.last_bytes_recv = counters.bytes_recv
        self.last_time = time.time()

    def get_speeds(self) -> Dict[str, float]:
        """Return upload and download speeds in bytes/sec."""
        counters = psutil.net_io_counters()
        now = time.time()
        elapsed = now - self.last_time

        if elapsed <= 0:
            return {"upload": 0.0, "download": 0.0}

        upload_speed = (counters.bytes_sent - self.last_bytes_sent) / elapsed
        download_speed = (counters.bytes_recv - self.last_bytes_recv) / elapsed

        self.last_bytes_sent = counters.bytes_sent
        self.last_bytes_recv = counters.bytes_recv
        self.last_time = now

        return {
            "upload": upload_speed,
            "download": download_speed,
            "total_sent": counters.bytes_sent,
            "total_recv": counters.bytes_recv,
        }


def format_bytes(bytes_val: float) -> str:
    """Format bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(bytes_val) < 1024.0:
            return f"{bytes_val:6.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"
