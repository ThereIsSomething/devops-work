# Real Azure storage alternative for Session 18

**Nitish Kumar Bhambu — 24BCS10589**

The assignment requests S3. Its AWS source is retained in `../terraform-s3-demo/` and validated, but no AWS apply is claimed. This separate project runs the Terraform lifecycle against Azure Blob Storage using the signed-in Azure account. Whether Azure is accepted in place of AWS is for the instructor to decide.

The lab created a private, versioned Standard LRS storage account, a private container and a small text blob. Shared-key access is disabled; the provider uses Entra authentication and the lab identity needs Storage Blob Data Contributor at the resource group. The group was created separately so the cloud exercises could share it.

```bash
export TF_VAR_subscription_id="$(az account show --query id -o tsv)"
export TF_VAR_resource_group_name=rg-devops-homework
export TF_VAR_storage_account_name=YOUR_UNIQUE_LOWERCASE_NAME
terraform init
terraform fmt
terraform validate
terraform plan -out=lab.tfplan
terraform apply lab.tfplan
terraform show
terraform output
# A small in-place update, followed by cleanup:
terraform plan -var=stage=reviewed -out=update.tfplan
terraform apply update.tfplan
terraform destroy -var=stage=reviewed
terraform state list
```

The actual run also listed the uploaded blob through Azure CLI. The tag update changed one resource in place. Destroy removed all three managed resources and `terraform state list` was empty. [Full terminal evidence](../outputs/azure-lifecycle.txt).

State and saved plans stay outside Git because they can contain sensitive values. The provider lock file is committed for repeatable dependency selection.
