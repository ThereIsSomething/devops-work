# Session 20: Monitoring, Observability and GitOps

**Nitish Kumar Bhambu — 24BCS10589**

Monitoring checks known signals such as CPU, memory, error rate and application health. Observability helps explain an unexpected failure by relating those signals to logs and request context. Metrics are numerical time series; logs are individual events; traces join spans across a request's journey. This demo implements metrics and logs; distributed tracing is described, not implemented.

The [monitoring stack](../final-devops-project/monitoring/README.md) uses Prometheus to scrape TaskBoard and evaluate an application-unavailable alert. Grafana has a provisioned dashboard for health, request rate, process memory and CPU rate. `kubectl top` provides separate Kubernetes resource measurements.

## GitOps mini project

`gitops/app/` contains a Namespace, a two-replica Deployment and a Service. The Argo CD Application is outside that watched folder. Git is the source of desired configuration; the cluster is the actual state; Argo CD compares them and applies changes. `selfHeal: true` lets it repair a manual replica change, and `prune: true` removes managed resources deleted from Git.

This exercise uses the existing Minikube cluster. It does not create another kind cluster just to repeat the same concepts. Argo CD core is installed at version v3.5.4 in homework-gitops. Its controller and repository server perform reconciliation; there is no public dashboard exposure.

```bash
curl -fLsS https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/core-install.yaml -o /tmp/argocd-core.yaml
scripts/kubectl create namespace homework-gitops
scripts/kubectl -n homework-gitops apply --server-side -f /tmp/argocd-core.yaml
scripts/kubectl apply -f 19-monitoring-gitops/gitops/application.yaml
scripts/kubectl -n homework-gitops get applications
# After sync, deliberately introduce drift:
scripts/kubectl -n homework-gitops-demo scale deployment/web --replicas=1
# Wait for Argo CD to restore the committed count of 2.
```

A real GitOps demonstration requires the watched files to be pushed first. Creating an Application YAML without a successful reconciliation is not sufficient evidence. The actual run is captured in outputs/.

The same principle applies to a Git change: commit replicas=3, push it, and verify three replicas after reconciliation. Reconciliation is the compare-and-correct loop. Self-healing fixes cluster drift toward Git; it does not guess whether a committed change was a good idea.

References: [Argo CD](https://argo-cd.readthedocs.io/en/stable/), [Prometheus](https://prometheus.io/docs/introduction/overview/).
