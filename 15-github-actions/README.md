# Session 16: CI/CD and GitHub Actions

**Nitish Kumar Bhambu — 24BCS10589**

This demo uses the TaskBoard app in [the final project](../final-devops-project/README.md), adapted from the instructor's application. The executable [workflow](../.github/workflows/devops.yml) is in the repository root so GitHub can discover it.

CI checks each proposed change: install locked dependencies, run nine API tests, build the React frontend and run security checks. CD takes a passing build to an environment; here Helm deploys it into a temporary kind cluster and HTTP verifies the result. That cluster is deleted after the run. It demonstrates deployment automation, but it is not a persistent cloud deployment.

A workflow is the YAML automation; a job runs on a runner; steps share that job's filesystem. `needs` makes the deployment job wait for the test/security job. Each job gets a fresh Ubuntu runner, so images are built in the job that scans, deploys and pushes them. Test reports, frontend build output and scan reports are stored as workflow artifacts.

`GITHUB_TOKEN` is supplied by Actions and used with packages:write for GHCR. There is no laptop kubeconfig Secret because the runner creates its own temporary cluster. Real cloud CD would use a reachable cluster and a scoped workload identity. Images are tagged with the Git commit SHA so a release can be traced back to source.

## Local evidence

API tests, dependency audit and migration output are linked from the final project. Hosted execution needs its real Actions run URL; local pytest success alone is not evidence of a green Actions run.

After publishing, inspect the [Actions page](https://github.com/ThereIsSomething/devops-work/actions) and record the run URL and its conclusion.

Reference: [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions).
