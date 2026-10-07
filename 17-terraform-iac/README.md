# Session 18: Terraform and Infrastructure as Code

**Nitish Kumar Bhambu — 24BCS10589**

The required [terraform-s3-demo](terraform-s3-demo/) contains provider.tf, main.tf, variables.tf, outputs.tf and a sample terraform.tfvars. Change the sample bucket name to a globally unique name before planning. It creates an AWS S3 bucket with versioning, encryption and public access blocked.

Static validation can run without an AWS account. A real plan/apply/show/output/destroy requires AWS credentials and creates billable resources. The AWS configuration was validated locally. I used Azure Blob Storage for the live cloud exercise; this provider substitution needs instructor acceptance.

```bash
cd 17-terraform-iac/terraform-s3-demo
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
The required service research is split into separate files:

- [IAM](aws-services/01-iam/README.md)
- [EC2](aws-services/02-ec2/README.md)
- [S3](aws-services/03-s3/README.md)
- [VPC](aws-services/04-vpc/README.md)
- [DynamoDB and RDS](aws-services/05-dynamodb-rds/README.md)

The [S3 project README](terraform-s3-demo/README.md) includes the local validation result.

## Real cloud run

I ran the complete Terraform create, inspect, update and destroy lifecycle against the [Azure storage alternative](azure-storage-alternative/README.md). The storage account, private container and blob were real Azure resources; all three were destroyed afterward. The AWS S3 source is validated but was not applied because AWS credentials were unavailable. Azure is a provider substitution and needs instructor acceptance. The create, update and destroy results are shown below.

### Create, update and destroy

```bash
zephoryx@fedora$ cd 17-terraform-iac/azure-storage-alternative

zephoryx@fedora$ terraform init
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 4.0"...
# ... output shortened ...

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

zephoryx@fedora$ terraform fmt -check

zephoryx@fedora$ terraform validate
Success! The configuration is valid.

zephoryx@fedora$ terraform plan -out=lab.tfplan
data.azurerm_resource_group.lab: Reading...
data.azurerm_resource_group.lab: Read complete after 2s [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework]

Terraform used the selected providers to generate the following execution
# ... output shortened ...
Plan: 3 to add, 0 to change, 0 to destroy.
# ... output shortened ...
Saved the plan to: lab.tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "lab.tfplan"

zephoryx@fedora$ terraform apply lab.tfplan
azurerm_storage_account.lab: Creating...
azurerm_storage_account.lab: Still creating... [00m10s elapsed]
azurerm_storage_account.lab: Still creating... [00m20s elapsed]
azurerm_storage_account.lab: Still creating... [00m30s elapsed]
azurerm_storage_account.lab: Still creating... [00m40s elapsed]
azurerm_storage_account.lab: Still creating... [00m50s elapsed]
# ... intermediate output omitted ...

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

blob_url = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt"
storage_account = "nitishiac1791379467"

zephoryx@fedora$ terraform show
# data.azurerm_resource_group.lab:
data "azurerm_resource_group" "lab" {
    id         = "/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework"
    location   = "centralindia"
    managed_by = null
    name       = "rg-devops-homework"
# ... intermediate output omitted ...
    url                               = "https://nitishiac1791379467.blob.core.windows.net/homework"
}

Outputs:

blob_url = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt"
storage_account = "nitishiac1791379467"

zephoryx@fedora$ terraform output
blob_url = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt"
storage_account = "nitishiac1791379467"

zephoryx@fedora$ az storage blob list --account-name nitishiac1791379467 --container-name homework --auth-mode login --query '[].{name:name,size:properties.contentLength}' -o json
[
  {
    "name": "hello.txt",
    "size": 63
  }
]

zephoryx@fedora$ terraform plan -out=update.tfplan
data.azurerm_resource_group.lab: Reading...
data.azurerm_resource_group.lab: Read complete after 0s [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework]
azurerm_storage_account.lab: Refreshing state... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467]
azurerm_storage_container.homework: Refreshing state... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467/blobServices/default/containers/homework]
# ... output shortened ...
Plan: 0 to add, 1 to change, 0 to destroy.
# ... output shortened ...
Saved the plan to: update.tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "update.tfplan"

zephoryx@fedora$ terraform apply update.tfplan
azurerm_storage_account.lab: Modifying... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467]
azurerm_storage_account.lab: Still modifying... [id=/subscriptions/d2fb80fc-da87-4e40-8e95-...ge/storageAccounts/nitishiac1791379467, 00m10s elapsed]
azurerm_storage_account.lab: Modifications complete after 14s [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467]

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.

Outputs:

blob_url = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt"
storage_account = "nitishiac1791379467"

zephoryx@fedora$ terraform destroy -auto-approve
data.azurerm_resource_group.lab: Reading...
data.azurerm_resource_group.lab: Read complete after 0s [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework]
azurerm_storage_account.lab: Refreshing state... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467]
azurerm_storage_container.homework: Refreshing state... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467/blobServices/default/containers/homework]
# ... output shortened ...
Plan: 0 to add, 0 to change, 3 to destroy.
# ... output shortened ...
azurerm_storage_account.lab: Destroying... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467]
azurerm_storage_account.lab: Destruction complete after 4s

Destroy complete! Resources: 3 destroyed.

zephoryx@fedora$ terraform state list
```
