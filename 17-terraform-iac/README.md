# Session 18: Terraform and Infrastructure as Code

**Nitish Kumar Bhambu — 24BCS10589**

The required [terraform-s3-demo](terraform-s3-demo/) contains provider.tf, main.tf, variables.tf, outputs.tf and a non-secret terraform.tfvars. Change the sample bucket name to a globally unique name before planning. It creates an AWS S3 bucket with versioning, encryption and public access blocked.

Static validation can run without an AWS account. A real plan/apply/show/output/destroy requires AWS credentials and creates billable resources. No AWS provisioning result is claimed until that workflow has actually run. Azure Blob Storage is a possible alternative only if the instructor approves it.

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
The required service research is split into separate files:

- [IAM](aws-services/01-iam/README.md)
- [EC2](aws-services/02-ec2/README.md)
- [S3](aws-services/03-s3/README.md)
- [VPC](aws-services/04-vpc/README.md)
- [DynamoDB and RDS](aws-services/05-dynamodb-rds/README.md)

See [cloud authentication setup](../docs/AZURE-SETUP.md). Actual static validation output is in [validation.txt](terraform-s3-demo/validation.txt).

## Real cloud run

I ran the complete Terraform create, inspect, update and destroy lifecycle against the [Azure storage alternative](azure-storage-alternative/README.md). The storage account, private container and blob were real Azure resources; all three were destroyed afterward. The AWS S3 source is validated but was not applied because AWS credentials were unavailable. Azure is a provider substitution and needs instructor acceptance. [Terminal transcript](outputs/azure-lifecycle.txt).

<!-- EVIDENCE -->

### azure-lifecycle.txt

[Complete transcript](outputs/azure-lifecycle.txt)

````text

$ terraform -chdir=17-terraform-iac/azure-storage-alternative init -input=false -no-color
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 4.0"...
- Installing hashicorp/azurerm v4.81.0...
- Installed hashicorp/azurerm v4.81.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

[exit 0]

$ terraform -chdir=17-terraform-iac/azure-storage-alternative fmt -check

[exit 0]

$ terraform -chdir=17-terraform-iac/azure-storage-alternative validate -no-color
Success! The configuration is valid.


[exit 0]

$ terraform -chdir=17-terraform-iac/azure-storage-alternative plan -input=false -no-color -out=lab.tfplan
data.azurerm_resource_group.lab: Reading...
data.azurerm_resource_group.lab: Read complete after 2s [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_storage_account.lab will be created
  + resource "azurerm_storage_account" "lab" {
      + access_tier                        = (known after apply)
      + account_kind                       = "StorageV2"
      + account_replication_type           = "LRS"
      + account_tier                       = "Standard"
      + allow_nested_items_to_be_public    = false
      + cross_tenant_replication_enabled   = false
      + default_to_oauth_authentication    = false
      + dns_endpoint_type                  = "Standard"
      + https_traffic_only_enabled         = true
      + id                                 = (known after apply)
      + infrastructure_encryption_enabled  = false
      + is_hns_enabled                     = false
      + large_file_share_enabled           = (known after apply)
      + local_user_enabled                 = true
      + location                           = "centralindia"
      + min_tls_version                    = "TLS1_2"
      + name                               = "nitishiac1791379467"

[Excerpt: 553 intermediate lines omitted; complete transcript linked above.]

              - retention_policy_days = 0 -> null
              - version               = "1.0" -> null
            }
          - logging {
              - delete                = false -> null
              - read                  = false -> null
              - retention_policy_days = 0 -> null
              - version               = "1.0" -> null
              - write                 = false -> null
            }
          - minute_metrics {
              - enabled               = false -> null
              - include_apis          = false -> null
              - retention_policy_days = 0 -> null
              - version               = "1.0" -> null
            }
        }

      - share_properties {
          - retention_policy {
              - days = 7 -> null
            }
        }
    }

  # azurerm_storage_blob.evidence will be destroyed
  - resource "azurerm_storage_blob" "evidence" {
      - access_tier            = "Hot" -> null
      - content_type           = "application/octet-stream" -> null
      - id                     = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt" -> null
      - metadata               = {} -> null
      - name                   = "hello.txt" -> null
      - parallelism            = 8 -> null
      - size                   = 0 -> null
      - source_content         = <<-EOT
            Terraform storage exercise by Nitish Kumar Bhambu, 24BCS10589.
        EOT -> null
      - storage_account_name   = "nitishiac1791379467" -> null
      - storage_container_id   = "/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467/blobServices/default/containers/homework" -> null
      - storage_container_name = "homework" -> null
      - type                   = "Block" -> null
      - url                    = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt" -> null
        # (3 unchanged attributes hidden)
    }

  # azurerm_storage_container.homework will be destroyed
  - resource "azurerm_storage_container" "homework" {
      - container_access_type             = "private" -> null
      - default_encryption_scope          = "$account-encryption-key" -> null
      - encryption_scope_override_enabled = true -> null
      - has_immutability_policy           = false -> null
      - has_legal_hold                    = false -> null
      - id                                = "/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467/blobServices/default/containers/homework" -> null
      - metadata                          = {} -> null
      - name                              = "homework" -> null
      - resource_manager_id               = "/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467/blobServices/default/containers/homework" -> null
      - storage_account_id                = "/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467" -> null
      - url                               = "https://nitishiac1791379467.blob.core.windows.net/homework" -> null
        # (1 unchanged attribute hidden)
    }

Plan: 0 to add, 0 to change, 3 to destroy.

Changes to Outputs:
  - blob_url        = "https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt" -> null
  - storage_account = "nitishiac1791379467" -> null
azurerm_storage_blob.evidence: Destroying... [id=https://nitishiac1791379467.blob.core.windows.net/homework/hello.txt]
azurerm_storage_blob.evidence: Destruction complete after 1s
azurerm_storage_container.homework: Destroying... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467/blobServices/default/containers/homework]
azurerm_storage_container.homework: Destruction complete after 0s
azurerm_storage_account.lab: Destroying... [id=/subscriptions/<subscription-id>/resourceGroups/rg-devops-homework/providers/Microsoft.Storage/storageAccounts/nitishiac1791379467]
azurerm_storage_account.lab: Destruction complete after 4s

Destroy complete! Resources: 3 destroyed.

[exit 0]

$ terraform -chdir=17-terraform-iac/azure-storage-alternative state list

[exit 0]
````
