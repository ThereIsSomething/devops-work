# Session 16: CI/CD and GitHub Actions

**Nitish Kumar Bhambu — 24BCS10589**

This demo uses the TaskBoard app in [the final project](../final-devops-project/README.md), adapted from the instructor's application. The executable [workflow](../.github/workflows/devops.yml) is in the repository root so GitHub can discover it.

CI checks each proposed change: install locked dependencies, run nine API tests, build the React frontend and run security checks. CD takes a passing build to an environment; here Helm deploys it into a temporary kind cluster and HTTP verifies the result. That cluster is deleted after the run. A separate workflow then deploys verified image tags to the real AKS lab cluster.

A workflow is the YAML automation; a job runs on a runner; steps share that job's filesystem. `needs` makes the deployment job wait for the test/security job. Each job gets a fresh Ubuntu runner, so images are built in the job that scans, deploys and pushes them. Test reports, frontend build output and scan reports are stored as workflow artifacts.

`GITHUB_TOKEN` is supplied by Actions and used with packages:write for GHCR. There is no laptop kubeconfig Secret because the runner creates its own temporary cluster. The Azure CD workflow uses the real AKS API and a scoped OIDC workload identity. Images are tagged with the Git commit SHA so a release can be traced back to source.

## Local evidence

The final project README includes API test results and security checks. The hosted runs are linked below.

The [Actions page](https://github.com/ThereIsSomething/devops-work/actions) contains the workflow runs and artifacts.

Reference: [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions).

## Checking the runs

I checked both runs from my terminal. The output below shows the workflow and job results; annotations are omitted here.

```bash
zephoryx@fedora$ gh run view 37630785578
✓ main TaskBoard CI, DevSecOps and deployment verification · 37630785578
Triggered via push about 1 hour ago

JOBS
✓ build-test-security in 32s (ID 112824778114)
✓ build-scan-deploy in 3m6s (ID 112825056983)

zephoryx@fedora$ gh run view 37631537431
✓ main Deploy verified TaskBoard images to Azure AKS · 37631537431
Triggered via workflow_dispatch about 1 hour ago

JOBS
✓ deploy in 7m30s (ID 112826801768)
```

## Hosted execution

[The actual CI run passed](https://github.com/ThereIsSomething/devops-work/actions/runs/37629099243), including tests, frontend build, source and image security checks, the kind/Helm deployment test, HTTP checks and SHA-tagged GHCR publication. [Run details and image tags](../final-devops-project/README.md#cicd-and-devsecops). The separate [Azure deployment workflow](../.github/workflows/azure-deploy.yml) uses GitHub OIDC to deploy a verified commit to AKS.

[The final hosted Azure deployment passed](https://github.com/ThereIsSomething/devops-work/actions/runs/37631537431) using the corrected chart and immutable images from the successful final CI run. [Deployment details](../final-devops-project/README.md#azure-browser-evidence).
