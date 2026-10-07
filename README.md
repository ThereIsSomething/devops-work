# DevOps homework

**Nitish Kumar Bhambu — 24BCS10589**

This repository contains the coursework for Sessions 1–21. Each session has a README with explanations, commands and evidence from actual runs. Terminal transcripts provide command evidence, and the final project also includes a real Azure browser screenshot. Intentional failures and setup problems are retained alongside their fixes; no cloud outputs are mocked.

The local labs cover Linux, shell, networking, Git, Docker, Kubernetes, Helm, troubleshooting, metrics and GitOps. The TaskBoard project has nine passing API tests and a successful hosted pipeline that builds, scans, verifies a Helm deployment and publishes images tagged with the source commit SHA.

**Cloud substitution:** the assignment names AWS S3, AWS infrastructure and EKS. Those AWS configurations are included and validated, but were not applied. The executed cloud exercises use real Azure Blob Storage, a VNet/Ubuntu VM and AKS. Instructor acceptance of Azure is still unknown. **Cleanup verified:** the final Azure inventory contains zero resources and zero resource groups. [Destroy and inventory evidence](final-devops-project/outputs/azure-destroy.txt).

[Copy the 20 README links in submission-form order](docs/SUBMISSION-LINKS.md) · [Cloud access/setup notes](docs/AZURE-SETUP.md) · [Hosted CI evidence](final-devops-project/outputs/hosted-ci.md)

| Session | Submission README | Evidence |
|---|---|---|
| 1 & 2 | [Linux Fundamentals](01-linux-fundamentals/README.md) | Executed labs and terminal evidence |
| 3 | [Shell Scripting](02-shell-scripting/README.md) | Executed labs and terminal evidence |
| 4 | [Networking](03-networking/README.md) | Executed labs and terminal evidence |
| 5 | [Git and GitHub](04-git-github/README.md) | Executed labs and terminal evidence |
| 6 | [Docker Fundamentals](05-docker-fundamentals/README.md) | Executed labs and terminal evidence |
| 7 | [Docker Images](06-dockerfiles-and-images/README.md) | Executed labs and terminal evidence |
| 8 | [Docker Networking](07-docker-network-volumes/README.md) | Executed labs and terminal evidence |
| 9 | [Kubernetes Fundamentals](08-kubernetes-fundamentals/README.md) | Executed labs and terminal evidence |
| 10 | [Pods, ReplicaSets and Deployments](09-kubernetes-core-objects/README.md) | Executed labs and terminal evidence |
| 11 | [Networking and Services](10-kubernetes-services/README.md) | Executed labs and terminal evidence |
| 12 | [Ingress, ConfigMaps and Secrets](11-ingress-configmaps-secrets/README.md) | Executed labs and terminal evidence |
| 13 | [Storage, HPA and Probes](12-storage-hpa-probes/README.md) | Executed labs and terminal evidence |
| 14 | [Kubernetes Troubleshooting](13-kubernetes-troubleshooting/README.md) | Executed labs and terminal evidence |
| 15 | [Helm](14-helm/README.md) | Executed labs and terminal evidence |
| 16 | [CI/CD and GitHub Actions](15-github-actions/README.md) | Executed labs and terminal evidence |
| 17 | [Complete CI/CD and DevSecOps](16-devsecops/README.md) | Executed labs and terminal evidence |
| 18 | [Terraform and Infrastructure as Code](17-terraform-iac/README.md) | Real Azure alternative; AWS source validated |
| 19 | [Cloud and Terraform in Action](18-cloud-terraform/README.md) | Real Azure alternative; AWS source validated |
| 20 | [Monitoring, Observability and GitOps](19-monitoring-gitops/README.md) | Executed labs and terminal evidence |
| 21 | [Final DevOps Project](final-devops-project/README.md) | App, CI/CD, Helm, monitoring, GitOps and cloud evidence |

## Run locally

The recorded environment uses Linux, Docker, Minikube, Helm, Terraform, Azure CLI and GitHub CLI. `scripts/kubectl` wraps the Minikube kubectl client so non-interactive scripts do not depend on a shell alias. Existing non-homework workloads were left alone.

- `python3 scripts/run_basics.py` runs the Linux/Git/Docker exercises.
- `python3 scripts/run_kubernetes_labs.py` runs Sessions 9–15 in dedicated namespaces.
- `scripts/final-local.sh` builds TaskBoard, starts Compose and demonstrates a direct Helm installation. The checked-in GitOps Application can subsequently take ownership of the local release, as documented in the final project.
- `scripts/install-gitops.sh` installs the Argo CD core mini project.
- `scripts/cleanup-homework.sh` cleans the owned local homework namespaces and Compose stack. Cloud cleanup is separate and recorded in its Terraform transcripts.

The public example database password is only for this disposable classroom application. Real credentials, state, saved plans, local kubeconfigs and environment files are excluded from Git.
