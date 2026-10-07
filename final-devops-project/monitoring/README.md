# Monitoring and observability

This small local stack scrapes the backend /metrics endpoint and Prometheus itself every ten seconds. Grafana is provisioned with that data source and four panels: scrape health, request rate, process memory and process CPU rate. The Services are internal; use local port forwarding for viewing. Anonymous access is Viewer only and is intended for this disposable lab. Storage uses emptyDir, so monitoring history is lost when its Pod is replaced.

Metrics are numerical measurements over time. Logs describe events, such as an HTTP request or a startup error. Traces connect spans across the path of a request. This project captures metrics and container logs; distributed tracing is explained but is not implemented or claimed. OpenTelemetry with a backend such as Tempo or Jaeger would add tracing. Prometheus evaluates an alert rule when the backend cannot be scraped for 30 seconds; alert evaluation is demonstrated locally, while external notifications would need Alertmanager and a configured receiver.

```bash
scripts/kubectl create namespace homework-monitoring
scripts/kubectl -n homework-monitoring apply -f final-devops-project/monitoring/stack.yaml
scripts/kubectl -n homework-monitoring port-forward svc/grafana 13001:3000
# Open http://localhost:13001
```

Observe CPU/memory with kubectl top as well as application metrics. An up metric means the scrape succeeded, not that every business operation is healthy; /ready also checks database access.

References: [Prometheus](https://prometheus.io/docs/introduction/overview/), [Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/).
