# Session 20: Monitoring, Observability and GitOps

**Nitish Kumar Bhambu — 24BCS10589**

Monitoring checks known signals such as CPU, memory, error rate and application health. Observability helps explain an unexpected failure by relating those signals to logs and request context. Metrics are numerical time series; logs are individual events; traces join spans across a request's journey. This demo implements metrics and logs; distributed tracing is described, not implemented.

The [monitoring stack](../final-devops-project/monitoring/README.md) uses Prometheus to scrape TaskBoard and evaluate an application-unavailable alert. Grafana has a provisioned dashboard for health, request rate, process memory and CPU rate. `kubectl top` provides separate Kubernetes resource measurements.

## GitOps mini project

`gitops/app/` contains a Namespace, a three-replica Deployment and a Service. The Argo CD Application is outside that watched folder. Git is the source of desired configuration; the cluster is the actual state; Argo CD compares them and applies changes. `selfHeal: true` lets it repair a manual replica change, and `prune: true` removes managed resources deleted from Git.

I used my existing Minikube cluster. Argo CD core is installed at version v3.5.4 in homework-gitops. Its controller and repository server perform reconciliation; there is no public dashboard exposure.

```bash
scripts/install-gitops.sh
# After sync, deliberately introduce drift:
kubectl -n homework-gitops-demo scale deployment/web --replicas=1
# Wait for Argo CD to restore the committed count of 3.
```

I pushed the watched manifests, created the Application and checked its sync status. The command blocks below show the reconciliation results.

The same principle applies to a Git change: change the committed count from 2 to 3, push it, and verify three replicas after reconciliation. I checked the resulting commit SHA and replica count after the push. Reconciliation is the compare-and-correct loop. Self-healing restores the configuration committed in Git.

References: [Argo CD](https://argo-cd.readthedocs.io/en/stable/), [Prometheus](https://prometheus.io/docs/introduction/overview/).

## Results

Argo CD synchronized the web workload, restored its manually reduced replica count and then applied the committed change from two replicas to three. The command blocks record the Git revision and the resulting 3/3 Deployment. Prometheus also recorded a real TaskBoard-unavailable alert during the database outage; after recovery its target was up and the alert cleared. The final TaskBoard chart has its own Argo Application and replica-repair evidence.

The monitoring stack was also deployed on Azure AKS. [Cloud metrics and target health](../final-devops-project/monitoring/README.md#azure-results) · [TaskBoard GitOps](../final-devops-project/gitops/README.md).

### Repairing manual replica drift

```bash
zephoryx@fedora$ kubectl get application homework-web -n homework-gitops -o wide
NAME           SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
homework-web   Synced        Healthy         28424dbac1f9cef8f395e608e8471a137a2ca7f4   homework

zephoryx@fedora$ kubectl get deploy web -n homework-gitops-demo
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     2            2           2m5s

zephoryx@fedora$ kubectl scale deploy web -n homework-gitops-demo --replicas=1
deployment.apps/web scaled

zephoryx@fedora$ kubectl get deploy web -n homework-gitops-demo
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     2            2           2m25s

zephoryx@fedora$ kubectl get application homework-web -n homework-gitops -o wide
NAME           SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
homework-web   Synced        Healthy         28424dbac1f9cef8f395e608e8471a137a2ca7f4   homework
```

### Git change: two replicas to three

```bash
zephoryx@fedora$ git log -1 --oneline
1924ccc Change GitOps web deployment to three replicas

zephoryx@fedora$ kubectl get application homework-web -n homework-gitops -o wide
NAME           SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
homework-web   Synced        Healthy         1924ccc230469d4a03a143cf3e063f72b6aa28b1   homework

zephoryx@fedora$ kubectl get deploy web -n homework-gitops-demo
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    3/3     3            3           4m59s
```

### Alert during the database outage

```bash
zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/targets
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

zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/alerts
{
  "status": "success",
  "data": {
    "alerts": [
# ... output shortened ...
      }
    ]
  }
}

zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/query?query=up
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
# ... intermediate output omitted ...
          1791378513.793,
          "1"
        ]
      }
    ]
  }
}
```

### Metrics after recovery

```bash
zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/targets
{
  "status": "success",
  "data": {
    "activeTargets": [
      {
        "discoveredLabels": {
# ... intermediate output omitted ...
    "droppedTargets": [],
    "droppedTargetCounts": {
      "prometheus": 0,
      "taskboard": 0
    }
  }
}

zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/alerts
{
  "status": "success",
  "data": {
    "alerts": []
  }
}

zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/query?query=up
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
# ... intermediate output omitted ...
          1791379483.728,
          "1"
        ]
      }
    ]
  }
}

zephoryx@fedora$ curl http://127.0.0.1:19090/api/v1/query?query=process_resident_memory_bytes
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
# ... intermediate output omitted ...
          1791379483.73,
          "86941696"
        ]
      }
    ]
  }
}

zephoryx@fedora$ kubectl top pods -n homework-final
NAME                        CPU(cores)   MEMORY(bytes)
backend-8584bc89c8-8p4ml    2m           64Mi
backend-8584bc89c8-ddktr    2m           67Mi
frontend-6f65884958-gmm5s   1m           10Mi
frontend-6f65884958-xgw2h   1m           10Mi
postgres-0                  3m           31Mi

zephoryx@fedora$ kubectl logs deployment/backend -n homework-final --tail=15
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

zephoryx@fedora$ curl -fsS http://127.0.0.1:13001/api/health
{
  "database": "ok",
  "version": "13.2.3",
  "commit": "90ffed056f0884267356c12a0eeb72a022af53f1"
}
```
