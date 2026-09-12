import os
import time
import datetime
import psutil


def get_uptime() -> str:
    """Return system uptime as a human-readable string."""
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    return str(datetime.timedelta(seconds=int(uptime_seconds)))


def get_load_average() -> tuple:
    """Return 1, 5, 15 minute load averages."""
    return os.getloadavg()


def get_boot_time() -> str:
    """Return system boot time as formatted string."""
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")


def get_cpu_count() -> dict:
    """Return logical and physical CPU counts."""
    return {
        "logical": psutil.cpu_count(logical=True),
        "physical": psutil.cpu_count(logical=False),
    }
