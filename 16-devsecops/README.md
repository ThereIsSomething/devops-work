# Session 17: Complete CI/CD and DevSecOps

**Nitish Kumar Bhambu — 24BCS10589**

This session extends the same working TaskBoard app so the pipeline checks something useful rather than a disconnected sample.

```text
Source → tests → SAST → SCA → secret scan → image build → image scans
                                                        ↓
                           Helm deployment test → GHCR publication
```

The pipeline deliberately verifies deployment before publishing the images. All security gates must pass; a failed gate prevents deployment and publication. This is a small variation on the assignment's ordering, with the same required stages. HIGH and CRITICAL findings block the release.

- [Application, Dockerfiles and Kubernetes/Helm implementation](../final-devops-project/README.md)
- [Executable GitHub Actions workflow](../.github/workflows/devops.yml)
- [Security tools, thresholds and explanations](../final-devops-project/security/README.md)
- [Test and security results](../final-devops-project/README.md#test-and-security-results)

The linked Actions runs show the checks and published images.

## Hosted execution

[The actual CI run passed](https://github.com/ThereIsSomething/devops-work/actions/runs/37629099243), including tests, frontend build, source and image security checks, the kind/Helm deployment test, HTTP checks and SHA-tagged GHCR publication. [Run details and image tags](../final-devops-project/README.md#cicd-and-devsecops). The separate [Azure deployment workflow](../.github/workflows/azure-deploy.yml) uses GitHub OIDC to deploy a verified commit to AKS.

The Azure release step accepts only an image commit with a successful CI run. It uses OIDC for cloud login, pulls the exact GHCR tags, deploys with Helm and checks process health, database readiness, API data and the Ingress route. The final project's [Azure deployment results](../final-devops-project/README.md#azure-browser-evidence) records its actual hosted run.
