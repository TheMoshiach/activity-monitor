import time
from typing import List

from rich import box
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text

from monitor import cpu, disk, memory, network, processes, system_info


def make_bar(percent: float, width: int = 30) -> str:
    """Create a simple ASCII progress bar."""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent:5.1f}%"


def color_percent(percent: float) -> str:
    """Return color name based on percentage."""
    if percent < 50:
        return "green"
    elif percent < 80:
        return "yellow"
    return "red"


def build_cpu_table(per_cpu: List[float]) -> Table:
    """Build CPU usage table."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Core", style="cyan", width=6)
    table.add_column("Usage", style="bold")

    for i, pct in enumerate(per_cpu):
        color = color_percent(pct)
        table.add_row(f"CPU{i}", f"[{color}]{make_bar(pct)}[/]")

    return table


def build_memory_panel(mem: dict, swap: dict) -> Panel:
    """Build memory info panel."""
    mem_total_gb = mem["total"] / (1024 ** 3)
    mem_used_gb = mem["used"] / (1024 ** 3)
    swap_total_gb = swap["total"] / (1024 ** 3)
    swap_used_gb = swap["used"] / (1024 ** 3)

    color = color_percent(mem["percent"])

    content = (
        f"RAM:   [{color}]{make_bar(mem['percent'])}[/]  "
        f"{mem_used_gb:.1f} / {mem_total_gb:.1f} GB\n"
        f"Swap:  [{color_percent(swap['percent'])}]{make_bar(swap['percent'])}[/]  "
        f"{swap_used_gb:.1f} / {swap_total_gb:.1f} GB"
    )
    return Panel(content, title="[bold magenta]Memory[/]", border_style="magenta")


def build_disk_table(partitions: List[dict]) -> Table:
    """Build disk usage table."""
    table = Table(show_header=True, box=box.SIMPLE_HEAD, padding=(0, 1))
    table.add_column("Mount", style="cyan", width=12)
    table.add_column("Used", style="bold", width=20)
    table.add_column("Size", justify="right", width=10)
    table.add_column("Free", justify="right", width=10)

    for part in partitions:
        color = color_percent(part["percent"])
        used_gb = part["used"] / (1024 ** 3)
        total_gb = part["total"] / (1024 ** 3)
        free_gb = part["free"] / (1024 ** 3)
        table.add_row(
            part["mountpoint"],
            f"[{color}]{make_bar(part['percent'])}[/]",
            f"{used_gb:.1f}/{total_gb:.1f}G",
            f"{free_gb:.1f}G",
        )

    return table


def build_network_panel(net_stats: dict) -> Panel:
    """Build network stats panel."""
    download = network.format_bytes(net_stats["download"]) + "/s"
    upload = network.format_bytes(net_stats["upload"]) + "/s"
    total_down = network.format_bytes(net_stats["total_recv"])
    total_up = network.format_bytes(net_stats["total_sent"])

    content = (
        f"↓ Download: [green]{download:>12}[/]  (total: {total_down})\n"
        f"↑ Upload:   [blue]{upload:>12}[/]  (total: {total_up})"
    )
    return Panel(content, title="[bold cyan]Network[/]", border_style="cyan")


def build_process_table(procs: List[dict]) -> Table:
    """Build top processes table."""
    table = Table(show_header=True, box=box.SIMPLE_HEAD, padding=(0, 1))
    table.add_column("PID", justify="right", style="dim", width=7)
    table.add_column("Name", style="cyan", width=20)
    table.add_column("User", style="dim", width=10)
    table.add_column("CPU%", justify="right", width=7)
    table.add_column("MEM%", justify="right", width=7)
    table.add_column("RSS", justify="right", width=10)
    table.add_column("Status", width=10)

    for proc in procs:
        cpu_color = color_percent(proc["cpu_percent"])
        mem_color = color_percent(proc["memory_percent"])
        rss = network.format_bytes(proc["memory_rss"])
        table.add_row(
            str(proc["pid"]),
            proc["name"][:19],
            (proc["username"] or "")[:9],
            f"[{cpu_color}]{proc['cpu_percent']:5.1f}[/]",
            f"[{mem_color}]{proc['memory_percent']:5.1f}[/]",
            rss,
            proc["status"],
        )

    return table


def build_system_header() -> Text:
    """Build system info header."""
    uptime = system_info.get_uptime()
    load1, load5, load15 = system_info.get_load_average()
    cpu_count = system_info.get_cpu_count()

    header = Text()
    header.append(f"Uptime: {uptime}  ", style="bold green")
    header.append(f"Load: {load1:.2f} {load5:.2f} {load15:.2f}  ", style="bold yellow")
    header.append(f"CPUs: {cpu_count['physical']}P/{cpu_count['logical']}L", style="bold blue")
    return header


class ActivityMonitor:
    """Main activity monitor TUI."""

    def __init__(self, sort_by: str = "cpu"):
        self.console = Console()
        self.net_tracker = network.NetworkTracker()
        self.sort_by = sort_by
        self.running = True

    def make_layout(self) -> Layout:
        """Create the screen layout."""
        layout = Layout(name="root")
        layout.split_column(
            Layout(name="header", size=1),
            Layout(name="main"),
            Layout(name="processes", size=18),
        )
        layout["main"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=2),
        )
        layout["left"].split_column(
            Layout(name="cpu", ratio=2),
            Layout(name="memory", ratio=1),
        )
        layout["right"].split_column(
            Layout(name="disk"),
            Layout(name="network", size=5),
        )
        return layout

    def update(self) -> Layout:
        """Fetch fresh data and build layout."""
        layout = self.make_layout()

        # Header
        layout["header"].update(build_system_header())

        # CPU
        per_cpu = cpu.get_per_cpu_percent(interval=0.1)
        cpu_table = build_cpu_table(per_cpu)
        layout["cpu"].update(
            Panel(cpu_table, title="[bold green]CPU[/]", border_style="green")
        )

        # Memory
        mem = memory.get_memory_stats()
        swap = memory.get_swap_stats()
        layout["memory"].update(build_memory_panel(mem, swap))

        # Disk
        partitions = disk.get_disk_partitions()
        disk_table = build_disk_table(partitions)
        layout["disk"].update(
            Panel(disk_table, title="[bold yellow]Disk[/]", border_style="yellow")
        )

        # Network
        net_stats = self.net_tracker.get_speeds()
        layout["network"].update(build_network_panel(net_stats))

        # Processes
        procs = processes.get_top_processes(sort_by=self.sort_by, limit=15)
        proc_table = build_process_table(procs)
        layout["processes"].update(
            Panel(proc_table, title=f"[bold red]Top Processes (sort: {self.sort_by})[/]", border_style="red")
        )

        return layout

    def run(self):
        """Run the live monitor."""
        with Live(self.update(), screen=True, refresh_per_second=2) as live:
            while self.running:
                time.sleep(0.5)
                live.update(self.update())
