"""Prometheus HTTP exporter entry point.

Exposes system metrics (CPU, memory, disk, network) collected via psutil,
plus the example app-level metrics from custom_metrics.py, on /metrics.
"""
from __future__ import annotations

import argparse
import logging
import time

from prometheus_client import Gauge, start_http_server

from exporter.collectors import collect_system_snapshot

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("prom-exporter-toolkit")

CPU_USAGE = Gauge("host_cpu_usage_percent", "Host CPU usage percent")
MEMORY_USAGE_PERCENT = Gauge("host_memory_usage_percent", "Host memory usage percent")
MEMORY_USED_BYTES = Gauge("host_memory_used_bytes", "Host memory used in bytes")
LOAD_AVG_1M = Gauge("host_load_average_1m", "1 minute load average")
DISK_USAGE_PERCENT = Gauge(
    "host_disk_usage_percent", "Disk usage percent", ["mountpoint"]
)
NET_BYTES_SENT = Gauge("host_net_bytes_sent_total", "Total network bytes sent")
NET_BYTES_RECV = Gauge("host_net_bytes_recv_total", "Total network bytes received")
PROCESS_COUNT = Gauge("host_process_count", "Number of running processes")


def update_metrics() -> None:
    """Take one snapshot and push the values into the Prometheus gauges."""
    snapshot = collect_system_snapshot()

    CPU_USAGE.set(snapshot.cpu_percent)
    MEMORY_USAGE_PERCENT.set(snapshot.memory_percent)
    MEMORY_USED_BYTES.set(snapshot.memory_used_bytes)
    LOAD_AVG_1M.set(snapshot.load_avg_1m)
    NET_BYTES_SENT.set(snapshot.net_bytes_sent)
    NET_BYTES_RECV.set(snapshot.net_bytes_recv)
    PROCESS_COUNT.set(snapshot.process_count)

    for disk in snapshot.disks:
        DISK_USAGE_PERCENT.labels(mountpoint=disk.mountpoint).set(disk.percent)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Prometheus system exporter.")
    parser.add_argument("--port", type=int, default=9100, help="Port to expose /metrics on")
    parser.add_argument(
        "--interval", type=float, default=5.0, help="Seconds between metric refreshes"
    )
    return parser


def run(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    start_http_server(args.port)
    logger.info("Exporter listening on :%d/metrics", args.port)

    while True:
        update_metrics()
        time.sleep(args.interval)


if __name__ == "__main__":
    run()
