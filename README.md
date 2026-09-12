# Terminal Activity Monitor

A self-contained, beautiful terminal-based system activity monitor built with Python.

## Features

- Real-time CPU usage (overall + per-core)
- Memory usage with visual bars
- Disk usage for all mounted partitions
- Network I/O stats (download/upload speeds)
- Top processes by CPU or memory
- System info (uptime, load average, boot time)
- Clean, colorful TUI using Rich

## Install

```bash
cd activity-monitor
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

- `q` or `Ctrl+C` — Quit
- `c` — Sort processes by CPU
- `m` — Sort processes by Memory
- `p` — Sort processes by PID
- `n` — Sort processes by Name
