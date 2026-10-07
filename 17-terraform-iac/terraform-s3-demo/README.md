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

State tracks the created resources and stays out of Git. Resource references tell Terraform the order to create or remove them.

Local static validation is shown below · [Session notes](../README.md)

## Local validation

The commands below ran from this Terraform project folder. Validation checks configuration; it does not provision cloud resources.

```bash
zephoryx@fedora$ terraform init -backend=false
Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 6.0"...
- Installing hashicorp/aws v6.67.0...
- Installed hashicorp/aws v6.67.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
# ... intermediate output omitted ...
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

zephoryx@fedora$ terraform validate
Success! The configuration is valid.

zephoryx@fedora$ terraform fmt -check -diff
```
