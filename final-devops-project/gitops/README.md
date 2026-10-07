# TaskBoard GitOps

Argo CD watches the TaskBoard Helm chart through [application.yaml](application.yaml). The external database Secret was provisioned separately. After the direct Helm exercise, its release-history Secrets were removed and Argo CD became the local workload's owner. Use Git changes for subsequent configuration changes instead of issuing independent Helm upgrades against those same objects.

A migration Job is a Sync hook with BeforeHookCreation and HookSucceeded deletion policies, so each sync can run the idempotent Alembic upgrade without a TTL-deleted Job causing endless drift. Sync waves first wait for PostgreSQL, then run the migration, then apply the application resources. HPA owns backend replica count; the frontend count is declared in chart values.

The real run synchronized the chart from Git and repaired a manual frontend change from two replicas to one. The commands and results are below. Session 20 separately demonstrates a Git commit changing its web workload from two replicas to three, then verifies the synced commit and replica count.

Argo reports the internal-only Ingress as Progressing because no external load-balancer address is assigned. Synchronization succeeded, the application Pods are ready, and an HTTP request through Traefik verifies `/health`, while a direct backend request verifies `/ready`. No public endpoint is claimed for this local Ingress.

## Commands and results

```bash
zephoryx@fedora$ kubectl get applications -n homework-gitops
NAME           SYNC STATUS   HEALTH STATUS
homework-web   Synced        Healthy
taskboard      Synced        Progressing

zephoryx@fedora$ kubectl delete secret -n homework-final -l owner=helm,name=taskboard
secret "sh.helm.release.v1.taskboard.v1" deleted from homework-final namespace
secret "sh.helm.release.v1.taskboard.v2" deleted from homework-final namespace
secret "sh.helm.release.v1.taskboard.v3" deleted from homework-final namespace

zephoryx@fedora$ kubectl scale deployment/frontend -n homework-final --replicas=1
deployment.apps/frontend scaled

zephoryx@fedora$ kubectl get deployment/frontend -n homework-final
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
frontend   2/2     2            2           31m

zephoryx@fedora$ kubectl get application taskboard -n homework-gitops -o wide
NAME        SYNC STATUS   HEALTH STATUS   REVISION                                   PROJECT
taskboard   Synced        Progressing     9d85fe3d871c2ba5ce87c77e33181978a1112fc0   homework

zephoryx@fedora$ curl -f -H 'Host: taskboard.local' http://localhost:18082/ready
<!doctype html><html><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/><title>TaskBoard</title>  <script type="module" crossorigin src="/assets/index-BhcRVjeF.js"></script>
  <link rel="stylesheet" crossorigin href="/assets/index-DkMuKOF6.css">
</head><body><div id="root"></div></body></html>

The frontend serves the SPA for unknown paths; /ready is a backend endpoint. Verify /health through the frontend and /ready directly on the backend.

zephoryx@fedora$ curl -f -H 'Host: taskboard.local' http://localhost:18082/health
{"status":"UP"}

zephoryx@fedora$ kubectl exec -n homework-final deployment/backend -- python -c 'import urllib.request; print(urllib.request.urlopen("http://localhost:8000/ready").read().decode())'
{"status":"READY"}
```
