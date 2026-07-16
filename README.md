# 📊 Prom Exporter Toolkit

[![CI](https://github.com/Dev-Guigs/prom-exporter-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Dev-Guigs/prom-exporter-toolkit/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A custom **Prometheus exporter** written in Python, exposing host-level
metrics (CPU, memory, disk, network, process count) via `psutil`, plus a
ready-to-copy pattern for instrumenting your own application-level metrics
(request counts, latency histograms, queue gauges).

Ships with a full **Docker Compose stack**: exporter + Prometheus + Grafana,
so you can see real dashboards in under a minute.

## Why this exists

Most "hello world" exporters just show a counter that increments forever.
This one demonstrates the actual shape of production exporters: a clean
collector layer (testable, no Prometheus dependency), a thin HTTP server
layer, and an example of the counter/gauge/histogram patterns you'd use to
instrument a real web service.

## Architecture

```
┌──────────────┐   psutil    ┌─────────────┐   /metrics   ┌────────────┐
│   Host OS    │────────────►│  Collector   │─────────────►│ Prometheus │
│ CPU/Mem/Disk │             │  (pure func) │  gauges      │  (scrape)  │
└──────────────┘             └─────────────┘               └─────┬──────┘
                                                                   │
                                                                   ▼
                                                              ┌─────────┐
                                                              │ Grafana │
                                                              └─────────┘
```

## Metrics exposed

| Metric | Type | Description |
|---|---|---|
| `host_cpu_usage_percent` | gauge | Current CPU usage % |
| `host_memory_usage_percent` | gauge | Current memory usage % |
| `host_memory_used_bytes` | gauge | Memory used in bytes |
| `host_load_average_1m` | gauge | 1-minute load average |
| `host_disk_usage_percent{mountpoint}` | gauge | Disk usage % per mount |
| `host_net_bytes_sent_total` | gauge | Cumulative bytes sent |
| `host_net_bytes_recv_total` | gauge | Cumulative bytes received |
| `host_process_count` | gauge | Number of running processes |
| `app_http_requests_total{method,endpoint,status}` | counter | Example app metric |
| `app_http_request_duration_seconds{endpoint}` | histogram | Example app metric |
| `app_job_queue_size` | gauge | Example app metric |

## Quickstart (local)

```bash
pip install -r requirements.txt
python -m exporter.server --port 9100 --interval 5
curl localhost:9100/metrics
```

## Quickstart (full stack with Docker Compose)

```bash
cd docker
docker compose up --build
```

- Exporter: http://localhost:9100/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (anonymous access enabled, or admin/admin)

In Grafana, add Prometheus (`http://prometheus:9090`) as a data source and
start charting `host_cpu_usage_percent`, `host_memory_usage_percent`, etc.

## Instrumenting your own app

```python
from exporter.custom_metrics import record_request
import time

start = time.time()
# ... handle request ...
record_request(method="GET", endpoint="/checkout", status=200, duration_seconds=time.time() - start)
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest --cov=exporter
```

## Roadmap

- [ ] Add `docker/grafana-provisioning` for auto-loaded dashboards
- [ ] Add alerting rules example (`prometheus/alerts.yml`)
- [ ] Push-gateway mode for batch jobs

## License

MIT — see [LICENSE](LICENSE).
