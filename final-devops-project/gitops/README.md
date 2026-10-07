# TaskBoard GitOps

Argo CD watches the TaskBoard Helm chart through [application.yaml](application.yaml). The external database Secret was provisioned separately. After the direct Helm exercise, its release-history Secrets were removed and Argo CD became the local workload's owner. Use Git changes for subsequent configuration changes instead of issuing independent Helm upgrades against those same objects.

A migration Job is a Sync hook with BeforeHookCreation and HookSucceeded deletion policies, so each sync can run the idempotent Alembic upgrade without a TTL-deleted Job causing endless drift. Sync waves first wait for PostgreSQL, then run the migration, then apply the application resources. HPA owns backend replica count; the frontend count is declared in chart values.

The real run synchronized the chart from Git and repaired a manual frontend change from two replicas to one. [Terminal evidence](../outputs/gitops.txt). Session 20 separately demonstrates a Git commit changing its web workload from two replicas to three, then verifies the synced commit and replica count.

Argo reports the internal-only Ingress as Progressing because no external load-balancer address is assigned. Synchronization succeeded, the application Pods are ready, and an HTTP request through Traefik verifies `/health`, while a direct backend request verifies `/ready`. No public endpoint is claimed for this local Ingress.
