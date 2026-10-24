# Terminal Activity Monitor

A real-time terminal dashboard for CPU, memory, disk, network, and process activity, built with Python, psutil, and Rich.

> **Platform:** Designed and tested on macOS. It may also work on Linux, but the keyboard controls rely on the Unix-only `tty` and `termios` modules. Windows is not currently supported.

## Features

- Real-time CPU usage (overall and per-core)
- Memory and swap usage with visual bars
- Disk usage for mounted partitions
- Network download and upload speeds
- Top processes sorted by CPU, memory, PID, or name
- System uptime, load average, and boot time
- Live, colorful terminal interface built with Rich

## How it works

- `psutil` collects system and process statistics.
- `Rich` renders the continuously updating terminal dashboard.
- A background keyboard listener changes process sorting without stopping the display.

## Install

Requires Python 3 and a terminal on macOS.

```bash
git clone https://github.com/TheMoshiach/activity-monitor.git
cd activity-monitor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

- `q` or `Ctrl+C` — Quit
- `c` — Sort processes by CPU
- `m` — Sort processes by memory
- `p` — Sort processes by PID
- `n` — Sort processes by name
