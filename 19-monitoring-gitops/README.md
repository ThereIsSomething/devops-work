# Session 20: Monitoring, Observability and GitOps

**Nitish Kumar Bhambu — 24BCS10589**

Monitoring checks known signals such as CPU, memory, error rate and application health. Observability helps explain an unexpected failure by relating those signals to logs and request context. Metrics are numerical time series; logs are individual events; traces join spans across a request's journey. This demo implements metrics and logs; distributed tracing is described, not implemented.

The [monitoring stack](../final-devops-project/monitoring/README.md) uses Prometheus to scrape TaskBoard and evaluate an application-unavailable alert. Grafana has a provisioned dashboard for health, request rate, process memory and CPU rate. `kubectl top` provides separate Kubernetes resource measurements.

## GitOps mini project

`gitops/app/` contains a Namespace, a three-replica Deployment and a Service. The Argo CD Application is outside that watched folder. Git is the source of desired configuration; the cluster is the actual state; Argo CD compares them and applies changes. `selfHeal: true` lets it repair a manual replica change, and `prune: true` removes managed resources deleted from Git.

This exercise uses the existing Minikube cluster. It does not create another kind cluster just to repeat the same concepts. Argo CD core is installed at version v3.5.4 in homework-gitops. Its controller and repository server perform reconciliation; there is no public dashboard exposure.

```bash
scripts/install-gitops.sh
# After sync, deliberately introduce drift:
scripts/kubectl -n homework-gitops-demo scale deployment/web --replicas=1
# Wait for Argo CD to restore the committed count of 3.
```

A real GitOps demonstration requires the watched files to be pushed first. Creating an Application YAML without a successful reconciliation is not sufficient evidence. The actual run is captured in outputs/.

The same principle applies to a Git change: change the committed count from 2 to 3, push it, and verify three replicas after reconciliation. The actual run did this and recorded the resulting commit SHA. Reconciliation is the compare-and-correct loop. Self-healing fixes cluster drift toward Git; it does not guess whether a committed change was a good idea.

References: [Argo CD](https://argo-cd.readthedocs.io/en/stable/), [Prometheus](https://prometheus.io/docs/introduction/overview/).


## Actual results

Argo CD synchronized the web workload, restored its manually reduced replica count and then applied the committed change from two replicas to three. The transcript records the Git revision and the resulting 3/3 Deployment. Prometheus also recorded a real TaskBoard-unavailable alert during the database outage; after recovery its target was up and the alert cleared. The final TaskBoard chart has its own Argo Application and replica-repair evidence.

The monitoring stack was also deployed on Azure AKS. [Cloud metrics and target health](../final-devops-project/outputs/azure-monitoring.txt) · [TaskBoard GitOps](../final-devops-project/gitops/README.md).

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

### gitops-git-change.txt

[Complete transcript](outputs/gitops-git-change.txt)

````text
$ git log -1 --oneline
1924ccc Change GitOps web deployment to three replicas
$ scripts/kubectl get application homework-web -n homework-gitops -o wide
NAME           SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
homework-web   Synced        Healthy         1924ccc230469d4a03a143cf3e063f72b6aa28b1   homework
$ scripts/kubectl get deploy web -n homework-gitops-demo
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    3/3     3            3           4m59s
````

### gitops-selfheal.txt

[Complete transcript](outputs/gitops-selfheal.txt)

````text
$ scripts/kubectl get application homework-web -n homework-gitops -o wide
NAME           SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
homework-web   Synced        Healthy         28424dbac1f9cef8f395e608e8471a137a2ca7f4   homework
[exit 0]
$ scripts/kubectl get deploy web -n homework-gitops-demo
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     2            2           2m5s
[exit 0]
$ scripts/kubectl scale deploy web -n homework-gitops-demo --replicas=1
deployment.apps/web scaled
[exit 0]
$ scripts/kubectl get deploy web -n homework-gitops-demo
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     2            2           2m25s
[exit 0]
$ scripts/kubectl get application homework-web -n homework-gitops -o wide
NAME           SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
homework-web   Synced        Healthy         28424dbac1f9cef8f395e608e8471a137a2ca7f4   homework
[exit 0]
````

### monitoring-recovery.txt

[Complete transcript](outputs/monitoring-recovery.txt)

````text
$ curl http://127.0.0.1:19090/api/v1/targets
{
  "status": "success",
  "data": {
    "activeTargets": [
      {
        "discoveredLabels": {
          "__address__": "localhost:9090",
          "__always_scrape_classic_histograms__": "false",
          "__convert_classic_histograms_to_nhcb__": "false",
          "__metrics_path__": "/metrics",
          "__scheme__": "http",
          "__scrape_interval__": "10s",
          "__scrape_native_histograms__": "false",
          "__scrape_timeout__": "10s",
          "job": "prometheus"
        },
        "labels": {
          "instance": "localhost:9090",
          "job": "prometheus"
        },
        "scrapePool": "prometheus",
        "scrapeUrl": "http://localhost:9090/metrics",
        "globalUrl": "http://prometheus-76b49b8495-t7q28:9090/metrics",
        "lastError": "",
        "lastScrape": "2026-10-07T13:24:40.13637094Z",
        "lastScrapeDuration": 0.00289942,
        "health": "up",
        "scrapeInterval": "10s",
        "scrapeTimeout": "10s"
      },
      {
        "discoveredLabels": {
          "__address__": "backend.homework-final.svc.cluster.local:8000",
          "__always_scrape_classic_histograms__": "false",
          "__convert_classic_histograms_to_nhcb__": "false",
          "__metrics_path__": "/metrics",
          "__scheme__": "http",
          "__scrape_interval__": "10s",
          "__scrape_native_histograms__": "false",
          "__scrape_timeout__": "10s",
          "job": "taskboard"
        },
        "labels": {
          "instance": "backend.homework-final.svc.cluster.local:8000",
          "job": "taskboard"
        },
        "scrapePool": "taskboard",
        "scrapeUrl": "http://backend.homework-final.svc.cluster.local:8000/metrics",
        "globalUrl": "http://backend.homework-final.svc.cluster.local:8000/metrics",
        "lastError": "",
        "lastScrape": "2026-10-07T13:24:38.914555745Z",
        "lastScrapeDuration": 0.003580358,
        "health": "up",
        "scrapeInterval": "10s",
        "scrapeTimeout": "10s"
      }
    ],
    "droppedTargets": [],
    "droppedTargetCounts": {
      "prometheus": 0,
      "taskboard": 0
    }
  }
}
$ curl http://127.0.0.1:19090/api/v1/alerts
{
  "status": "success",
  "data": {
    "alerts": []
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
          1791379483.728,
          "1"
        ]
      },
      {
        "metric": {
          "__name__": "up",
          "instance": "localhost:9090",
          "job": "prometheus"
        },
        "value": [
          1791379483.728,
          "1"
        ]
      }
    ]
  }
}
$ curl http://127.0.0.1:19090/api/v1/query?query=process_resident_memory_bytes
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "process_resident_memory_bytes",
          "instance": "localhost:9090",
          "job": "prometheus"
        },
        "value": [
          1791379483.73,
          "43200512"
        ]
      },
      {
        "metric": {
          "__name__": "process_resident_memory_bytes",
          "instance": "backend.homework-final.svc.cluster.local:8000",
          "job": "taskboard"
        },
        "value": [
          1791379483.73,
          "86941696"
        ]
      }
    ]
  }
}
$ scripts/kubectl top pods -n homework-final
NAME                        CPU(cores)   MEMORY(bytes)
backend-8584bc89c8-8p4ml    2m           64Mi
backend-8584bc89c8-ddktr    2m           67Mi
frontend-6f65884958-gmm5s   1m           10Mi
frontend-6f65884958-xgw2h   1m           10Mi
postgres-0                  3m           31Mi

$ scripts/kubectl logs deployment/backend -n homework-final --tail=15
INFO:     10.244.0.1:42106 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:42112 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.1:42120 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.1:55938 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:55952 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.108:43244 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:55964 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.1:40044 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40060 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.83:36966 - "GET /metrics HTTP/1.1" 200 OK
INFO:     10.244.0.1:40062 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.1:57558 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57574 - "GET /ready HTTP/1.1" 200 OK
INFO:     10.244.0.83:43920 - "GET /metrics HTTP/1.1" 200 OK
INFO:     10.244.0.1:57580 - "GET /ready HTTP/1.1" 200 OK
Found 2 pods, using pod/backend-8584bc89c8-ddktr

$ curl -fsS http://127.0.0.1:13001/api/health
{
  "database": "ok",
  "version": "13.2.3",
  "commit": "90ffed056f0884267356c12a0eeb72a022af53f1"
}
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
