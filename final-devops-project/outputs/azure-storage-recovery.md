# AKS disk initialization recovery

The actual PostgreSQL log reported:

```text
initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
initdb: detail: It contains a lost+found directory, perhaps due to it being a mount point.
initdb: hint: Using a mount point directly as the data directory is not recommended.
Create a subdirectory under the mount point.
```

The managed-csi PVC was Bound, so this was an initialization failure on the mounted filesystem, not a missing volume. I set `PGDATA=/var/lib/postgresql/data/pgdata`. The StatefulSet retained its broken old Pod while waiting for readiness; deleting that failed Pod let the replacement use the corrected template.

```bash
kubectl -n homework-final set env statefulset/postgres PGDATA=/var/lib/postgresql/data/pgdata
kubectl -n homework-final delete pod postgres-0
kubectl -n homework-final rollout status statefulset/postgres --timeout=120s
```

The fix is committed in the chart. Argo sync waves make the database Service and StatefulSet ready before the migration hook runs. The final Azure workflow is rerun against the corrected source so the submitted deployment does not depend on this manual recovery.
