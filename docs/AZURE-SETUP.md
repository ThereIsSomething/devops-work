# Cloud access needed for this homework

Azure teaches the same infrastructure concepts, but it is a substitution. The assignment explicitly asks for AWS S3 in Session 18 and AWS infrastructure in Session 19. The instructor's Session 21 grading file also asks for EKS and a VPC with two public subnets. Ask whether Blob Storage, VNet and AKS are accepted before choosing Azure for the graded exercises.

## Azure Portal setup

1. Open https://portal.azure.com and sign in with your Microsoft account. Complete MFA yourself.
2. Search for **Subscriptions** in the top search bar. Open your subscription and check that its status is **Active**. A Microsoft account alone does not include an Azure subscription. If the list is empty, activate an eligible Azure for Students offer or arrange a subscription with your institution.
3. In the subscription, open **Access control (IAM)**, then **View my access**. You need permission to create the lab resources. Contributor on a dedicated lab resource group is sufficient for ordinary resource creation there; creating the resource group itself requires permission at subscription scope. Ask your subscription administrator if access is missing.
4. If using a shared subscription, have its administrator create a dedicated resource group such as `rg-devops-homework` and grant you Contributor on that group. Do not request Owner merely to create a storage account or VM.
5. Open **Cost Management + Billing → Cost Management → Budgets → Add**, choose the intended scope, and create a budget you can afford with email alerts. A budget alerts you; it does not automatically stop resources. Student credits and VM quotas do not guarantee that AKS can be provisioned in every region.
6. Do not manually create the storage account, VM or cluster for a Terraform exercise. Terraform should create them so the plan, state and destroy steps are meaningful.

## Connect the installed Azure CLI

Run these in your own terminal:

```bash
az version
az login
# If the browser cannot open:
# az login --use-device-code
az account list --query '[].{Name:name,ID:id,State:state,Default:isDefault}' -o table
az account set --subscription '<your subscription ID>'
az account show --query '{Name:name,ID:id,State:state}' -o table
export ARM_SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
```

Complete login and MFA in the browser; do not send passwords, tokens, device codes or private keys in chat. A subscription ID is an identifier, not a password, but it need not appear in the public homework logs. Terraform's Azure provider can use the local CLI session. This export applies to the current shell. GitHub Actions needs its own identity; your laptop's login is not transferred to a hosted runner. Prefer GitHub OIDC federation for cloud CI rather than a long-lived client secret.

## GitHub setup

```bash
gh auth login --hostname github.com --git-protocol ssh --web
gh auth status
```

Check that the existing repository `ThereIsSomething/devops-work` is public and that Actions is enabled. The workflows belong in the repository-root `.github/workflows/`; nested workflow folders alone do not execute. `GITHUB_TOKEN` is supplied automatically to Actions. Workflow package permissions allow GHCR publishing without a separate personal token.

A GitHub-hosted runner cannot reach this laptop's private Minikube API just because a kubeconfig is uploaded. The CI uses an ephemeral kind cluster for deployment verification. The separate Azure CD workflow then deploys verified image tags to AKS using a federated managed identity and an IP allowlist. The coursework cloud resources and federation are removed after evidence collection.

## Current setup and remaining student action

The submission identity is Nitish Kumar Bhambu, 24BCS10589. Azure CLI and GitHub CLI are authenticated locally, Git pushes work over SSH, and Docker Hub login is configured. The labs use a dedicated resource group in Central India, which is one of the student subscription's allowed regions. The subscription began with zero resources and was verified empty again after cleanup.

The remaining academic decision is whether the instructor accepts Azure for the AWS-specific exercises. Otherwise an AWS lab account is needed to run those exact provider-specific tasks. The AWS source files are retained and validated, but no AWS apply is claimed. Submit each README URL listed in [SUBMISSION-LINKS.md](SUBMISSION-LINKS.md).

## References

- [Azure CLI interactive login](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)
- [Check your Azure access](https://learn.microsoft.com/azure/role-based-access-control/check-access)
- [Create Azure budgets](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
- [Terraform Azure CLI authentication](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli)
