# 📊 Prom Exporter Toolkit

[![CI](https://github.com/Dev-Guigs/prom-exporter-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Dev-Guigs/prom-exporter-toolkit/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Um **exporter Prometheus** customizado, escrito em Python, que expõe
métricas de host (CPU, memória, disco, rede, quantidade de processos) via
`psutil`, além de trazer um padrão pronto para instrumentar suas próprias
métricas de aplicação (contagem de requisições, histograma de latência,
gauges de fila).

Vem com uma **stack completa em Docker Compose**: exporter + Prometheus +
Grafana, para você ver dashboards reais em menos de um minuto.

## Por que este projeto existe

A maioria dos exporters "hello world" só mostra um contador que fica
incrementando para sempre. Este demonstra o formato real de exporters em
produção: uma camada de coleta limpa (testável, sem dependência do
Prometheus), uma camada fina de servidor HTTP, e um exemplo dos padrões de
counter/gauge/histogram que você usaria para instrumentar um serviço web de
verdade.

## Arquitetura

```
┌──────────────┐   psutil    ┌─────────────┐   /metrics   ┌────────────┐
│   Host OS    │────────────►│  Collector   │─────────────►│ Prometheus │
│ CPU/Mem/Disco│             │ (função pura)│   gauges     │  (scrape)  │
└──────────────┘             └─────────────┘               └─────┬──────┘
                                                                   │
                                                                   ▼
                                                              ┌─────────┐
                                                              │ Grafana │
                                                              └─────────┘
```

## Métricas expostas

| Métrica | Tipo | Descrição |
|---|---|---|
| `host_cpu_usage_percent` | gauge | Uso atual de CPU (%) |
| `host_memory_usage_percent` | gauge | Uso atual de memória (%) |
| `host_memory_used_bytes` | gauge | Memória usada em bytes |
| `host_load_average_1m` | gauge | Load average de 1 minuto |
| `host_disk_usage_percent{mountpoint}` | gauge | Uso de disco (%) por mount |
| `host_net_bytes_sent_total` | gauge | Total acumulado de bytes enviados |
| `host_net_bytes_recv_total` | gauge | Total acumulado de bytes recebidos |
| `host_process_count` | gauge | Número de processos em execução |
| `app_http_requests_total{method,endpoint,status}` | counter | Métrica de exemplo de aplicação |
| `app_http_request_duration_seconds{endpoint}` | histogram | Métrica de exemplo de aplicação |
| `app_job_queue_size` | gauge | Métrica de exemplo de aplicação |

## Início rápido (local)

```bash
pip install -r requirements.txt
python -m exporter.server --port 9100 --interval 5
curl localhost:9100/metrics
```

## Início rápido (stack completa com Docker Compose)

```bash
cd docker
docker compose up --build
```

- Exporter: http://localhost:9100/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (acesso anônimo habilitado, ou admin/admin)

No Grafana, adicione o Prometheus (`http://prometheus:9090`) como data
source e comece a montar gráficos de `host_cpu_usage_percent`,
`host_memory_usage_percent`, etc.

## Instrumentando sua própria aplicação

```python
from exporter.custom_metrics import record_request
import time

start = time.time()
# ... trate a requisição ...
record_request(method="GET", endpoint="/checkout", status=200, duration_seconds=time.time() - start)
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest --cov=exporter
```

## Roadmap

- [ ] Adicionar `docker/grafana-provisioning` para dashboards carregados automaticamente
- [ ] Exemplo de regras de alerta (`prometheus/alerts.yml`)
- [ ] Modo push-gateway para jobs em batch

## Licença

MIT — veja [LICENSE](LICENSE).
