"""System metric collectors, decoupled from the Prometheus client library.

Each collector returns plain Python data structures. This keeps the logic
trivially unit-testable without needing a real prometheus_client registry,
and mockable without touching `/proc` or psutil in tests.
"""
from __future__ import annotations

from dataclasses import dataclass

import psutil


@dataclass
class DiskUsage:
    mountpoint: str
    total_bytes: int
    used_bytes: int
    percent: float


@dataclass
class SystemSnapshot:
    """A single point-in-time reading of host resource usage."""

    cpu_percent: float
    memory_percent: float
    memory_used_bytes: int
    memory_total_bytes: int
    load_avg_1m: float
    disks: list[DiskUsage]
    net_bytes_sent: int
    net_bytes_recv: int
    process_count: int


def collect_system_snapshot() -> SystemSnapshot:
    """Gather a snapshot of CPU, memory, disk, network, and process metrics."""
    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()
    try:
        load1, _, _ = psutil.getloadavg()
    except (OSError, AttributeError):
        # getloadavg() is unavailable on some platforms (e.g. Windows).
        load1 = 0.0

    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        disks.append(
            DiskUsage(
                mountpoint=part.mountpoint,
                total_bytes=usage.total,
                used_bytes=usage.used,
                percent=usage.percent,
            )
        )

    return SystemSnapshot(
        cpu_percent=psutil.cpu_percent(interval=None),
        memory_percent=mem.percent,
        memory_used_bytes=mem.used,
        memory_total_bytes=mem.total,
        load_avg_1m=load1,
        disks=disks,
        net_bytes_sent=net.bytes_sent,
        net_bytes_recv=net.bytes_recv,
        process_count=len(psutil.pids()),
    )
