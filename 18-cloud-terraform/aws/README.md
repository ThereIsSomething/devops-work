# AWS infrastructure

**Nitish Kumar Bhambu — 24BCS10589**

See the [session README](../README.md) for the architecture, cloud run and cleanup.

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
