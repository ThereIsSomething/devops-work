# Terraform S3 demo

**Nitish Kumar Bhambu — 24BCS10589**

Run the Terraform workflow from this folder after configuring temporary AWS/SSO credentials. The sample tfvars contains identifiers only, no access keys. `force_destroy = false` prevents accidental deletion of non-empty storage. The source and locally captured validation are ready; real AWS plan/apply/output/destroy evidence remains dependent on an AWS account.

```bash
terraform init
terraform fmt
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
terraform show
terraform output
# After collecting evidence and confirming resources are no longer needed:
terraform plan -destroy -out=tfplan
terraform apply tfplan
```

The final two commands execute a reviewed destroy plan. `terraform destroy` is the interactive shortcut for that destruction workflow. Do not apply or destroy a different person's state. State records resource identities and can include secrets; it is ignored here. References between resource attributes express dependencies, and Terraform orders operations from that graph.

[Static validation](validation.txt) · [Session notes](../README.md)
