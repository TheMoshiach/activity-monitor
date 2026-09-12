#!/usr/bin/env python3
"""
Terminal Activity Monitor
A beautiful, real-time system monitor for your terminal.
"""

import sys
import threading
import time

from rich.console import Console

from monitor.ui import ActivityMonitor


def main():
    console = Console()

    try:
        import psutil
        import rich
    except ImportError:
        console.print("[red]Missing dependencies. Run:[/red]")
        console.print("  source .venv/bin/activate")
        console.print("  pip install -r requirements.txt")
        sys.exit(1)

    monitor = ActivityMonitor(sort_by="cpu")

    # Keyboard listener thread for controls
    def keyboard_listener():
        import tty
        import termios
        import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while monitor.running:
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch in ("q", "\x03"):  # q or Ctrl+C
                        monitor.running = False
                    elif ch == "c":
                        monitor.sort_by = "cpu"
                    elif ch == "m":
                        monitor.sort_by = "memory"
                    elif ch == "p":
                        monitor.sort_by = "pid"
                    elif ch == "n":
                        monitor.sort_by = "name"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Start keyboard listener
    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    try:
        monitor.run()
    except KeyboardInterrupt:
        monitor.running = False

    console.print("\n[dim]Goodbye![/dim]")


if __name__ == "__main__":
    main()
