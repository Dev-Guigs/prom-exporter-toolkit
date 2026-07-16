"""Example of application/business-level metrics alongside system metrics.

In a real service you'd increment these from inside your request handlers,
background jobs, queue consumers, etc. This module shows the pattern so the
exporter isn't just "system metrics" but demonstrates the full use case
recruiters actually care about: instrumenting an app for Prometheus.
"""
from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

# Counts total HTTP requests, labeled by method/endpoint/status.
HTTP_REQUESTS_TOTAL = Counter(
    "app_http_requests_total",
    "Total number of HTTP requests processed",
    ["method", "endpoint", "status"],
)

# Tracks request latency distribution.
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
)

# Point-in-time gauge, e.g. size of a job queue.
JOB_QUEUE_SIZE = Gauge(
    "app_job_queue_size",
    "Current number of pending jobs in the queue",
)


def record_request(method: str, endpoint: str, status: int, duration_seconds: float) -> None:
    """Call this from a request middleware/decorator in a real application."""
    HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    HTTP_REQUEST_DURATION_SECONDS.labels(endpoint=endpoint).observe(duration_seconds)


def set_queue_size(size: int) -> None:
    JOB_QUEUE_SIZE.set(size)
