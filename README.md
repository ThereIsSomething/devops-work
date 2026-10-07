# DevOps homework

**Nitish Kumar Bhambu — 24BCS10589**

These are my notes and lab results for Sessions 1–20. Each folder has the commands, source files and output for that session. Long build logs are not fully included

I used Fedora, Docker, Minikube and Helm for the local exercises. Sessions 16, 17 and 20 share the [TaskBoard demo](demo-app/README.md) for CI/CD, security checks and monitoring.

For Sessions 18–19, I ran the cloud exercises on Azure. The AWS files passed local validation but were not applied.

[README links for the submission form](docs/SUBMISSION-LINKS.md)

| Session | README |
|---|---|
| 1 & 2 | [Linux Fundamentals](01-linux-fundamentals/README.md) |
| 3 | [Shell Scripting](02-shell-scripting/README.md) |
| 4 | [Networking](03-networking/README.md) |
| 5 | [Git and GitHub](04-git-github/README.md) |
| 6 | [Docker Fundamentals](05-docker-fundamentals/README.md) |
| 7 | [Docker Images](06-dockerfiles-and-images/README.md) |
| 8 | [Docker Networking](07-docker-network-volumes/README.md) |
| 9 | [Kubernetes Fundamentals](08-kubernetes-fundamentals/README.md) |
| 10 | [Pods, ReplicaSets and Deployments](09-kubernetes-core-objects/README.md) |
| 11 | [Networking and Services](10-kubernetes-services/README.md) |
| 12 | [Ingress, ConfigMaps and Secrets](11-ingress-configmaps-secrets/README.md) |
| 13 | [Storage, HPA and Probes](12-storage-hpa-probes/README.md) |
| 14 | [Kubernetes Troubleshooting](13-kubernetes-troubleshooting/README.md) |
| 15 | [Helm](14-helm/README.md) |
| 16 | [CI/CD and GitHub Actions](15-github-actions/README.md) |
| 17 | [Complete CI/CD and DevSecOps](16-devsecops/README.md) |
| 18 | [Terraform and Infrastructure as Code](17-terraform-iac/README.md) |
| 19 | [Cloud and Terraform in Action](18-cloud-terraform/README.md) |
| 20 | [Monitoring, Observability and GitOps](19-monitoring-gitops/README.md) |

## Running the demo

```bash
export TASKBOARD_DB_PASSWORD=classroom-example-only
docker compose -f demo-app/docker/compose.yaml up --build -d
```

Open http://localhost:13000. The password above is only an example for this lab; real credentials and Terraform state stay out of Git.
