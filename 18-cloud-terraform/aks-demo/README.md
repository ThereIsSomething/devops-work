# AKS deployment demo

This configuration created the AKS cluster used for the [CI/CD demo](../../demo-app/README.md). It ran one Standard_D2s_v3 node in Central India, with Entra authentication, Azure RBAC and a restricted API allowlist.

The GitHub identity uses OIDC. Its role assignments are limited to the lab cluster. The [Azure workflow](../../.github/workflows/azure-deploy.yml) deploys a previously tested image SHA.

The cluster, managed identity and role assignments were destroyed after the exercise. [Deployment and cleanup results](../../demo-app/README.md#cloud-cleanup-results).

Copy `terraform.tfvars.example` to a local `terraform.tfvars`, fill in the subscription and allowed source CIDRs, then run:

```bash
terraform init
terraform validate
terraform plan
terraform apply
# After the exercise:
terraform destroy
```

Local variables, kubeconfigs and state are excluded from Git.
