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

<!-- EVIDENCE -->

### argocd-install.txt

[Complete transcript](outputs/argocd-install.txt)

````text
customresourcedefinition.apiextensions.k8s.io/applications.argoproj.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/applicationsets.argoproj.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/appprojects.argoproj.io serverside-applied
serviceaccount/argocd-application-controller serverside-applied
serviceaccount/argocd-applicationset-controller serverside-applied
serviceaccount/argocd-redis serverside-applied
serviceaccount/argocd-repo-server serverside-applied
role.rbac.authorization.k8s.io/argocd-application-controller serverside-applied
role.rbac.authorization.k8s.io/argocd-applicationset-controller serverside-applied
role.rbac.authorization.k8s.io/argocd-redis serverside-applied
clusterrole.rbac.authorization.k8s.io/argocd-application-controller serverside-applied
rolebinding.rbac.authorization.k8s.io/argocd-application-controller serverside-applied
rolebinding.rbac.authorization.k8s.io/argocd-applicationset-controller serverside-applied
rolebinding.rbac.authorization.k8s.io/argocd-redis serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/argocd-application-controller serverside-applied
configmap/argocd-cm serverside-applied
configmap/argocd-cmd-params-cm serverside-applied
configmap/argocd-gpg-keys-cm serverside-applied
configmap/argocd-rbac-cm serverside-applied
configmap/argocd-ssh-known-hosts-cm serverside-applied
configmap/argocd-tls-certs-cm serverside-applied
secret/argocd-secret serverside-applied
service/argocd-applicationset-controller serverside-applied
service/argocd-metrics serverside-applied
service/argocd-redis serverside-applied
service/argocd-repo-server serverside-applied
deployment.apps/argocd-applicationset-controller serverside-applied
deployment.apps/argocd-redis serverside-applied
deployment.apps/argocd-repo-server serverside-applied
statefulset.apps/argocd-application-controller serverside-applied
networkpolicy.networking.k8s.io/argocd-application-controller-network-policy serverside-applied
networkpolicy.networking.k8s.io/argocd-applicationset-controller-network-policy serverside-applied
networkpolicy.networking.k8s.io/argocd-redis-network-policy serverside-applied
networkpolicy.networking.k8s.io/argocd-repo-server-network-policy serverside-applied
NAME                                                READY   STATUS              RESTARTS   AGE
argocd-application-controller-0                     0/1     ContainerCreating   0          1s
argocd-applicationset-controller-76fd8cdd4f-bgm65   0/1     ContainerCreating   0          1s
argocd-redis-bdbdffcb4-5v6fz                        0/1     Init:0/1            0          1s
argocd-repo-server-d89c7967d-2f575                  0/1     Init:0/1            0          1s
````

### monitoring.txt

[Complete transcript](outputs/monitoring.txt)

````text
Captured 2026-10-07T13:08:33.778261+00:00
$ curl http://127.0.0.1:19090/api/v1/targets
[
  {
    "job": "prometheus",
    "health": "up",
    "lastError": ""
  },
  {
    "job": "taskboard",
    "health": "down",
    "lastError": "Get \"http://backend.homework-final.svc.cluster.local:8000/metrics\": dial tcp 10.98.164.157:8000: connect: connection refused"
  }
]
$ curl http://127.0.0.1:19090/api/v1/alerts
{
  "status": "success",
  "data": {
    "alerts": [
      {
        "labels": {
          "alertname": "TaskBoardUnavailable",
          "instance": "backend.homework-final.svc.cluster.local:8000",
          "job": "taskboard",
          "severity": "warning"
        },
        "annotations": {
          "summary": "TaskBoard metrics endpoint cannot be scraped"
        },
        "state": "firing",
        "activeAt": "2026-10-07T13:02:57.196613459Z",
        "value": "0e+00"
      }
    ]
  }
}
$ curl http://127.0.0.1:19090/api/v1/query?query=up
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "up",
          "instance": "backend.homework-final.svc.cluster.local:8000",
          "job": "taskboard"
        },
        "value": [
          1791378513.793,
          "0"
        ]
      },
      {
        "metric": {
          "__name__": "up",
          "instance": "localhost:9090",
          "job": "prometheus"
        },
        "value": [
          1791378513.793,
          "1"
        ]
      }
    ]
  }
}
````
