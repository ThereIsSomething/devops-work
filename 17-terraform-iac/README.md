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
