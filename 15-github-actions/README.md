# Session 16: CI/CD and GitHub Actions

**Nitish Kumar Bhambu — 24BCS10589**

I used the [TaskBoard demo](../demo-app/README.md) for this exercise. The [workflow](../.github/workflows/devops.yml) runs on pushes to `main` and pull requests.

CI runs the nine API tests, builds the frontend and checks the code and dependencies. The next job builds and scans both Docker images, installs the app in a temporary kind cluster and checks HTTP responses. Passing images are published to GHCR with the commit SHA as their tag.

| Term | What it means here |
|---|---|
| Workflow | The YAML file that defines the pipeline |
| Job | A group of steps on a fresh GitHub runner |
| Step | One command or action within a job |
| Artifact | Saved test, build or scan results |

`needs` makes the image job wait for the tests. `GITHUB_TOKEN` handles GHCR access. The separate [Azure workflow](../.github/workflows/azure-deploy.yml) uses OIDC to deploy a tested image SHA to AKS.

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

[Successful CI run](https://github.com/ThereIsSomething/devops-work/actions/runs/37630785578) · [Successful Azure deployment](https://github.com/ThereIsSomething/devops-work/actions/runs/37631537431)
