# Session 17: CI/CD and DevSecOps

**Nitish Kumar Bhambu — 24BCS10589**

I added security checks to the same [TaskBoard demo](../demo-app/README.md) used in Session 16.

```text
Tests → SAST → dependency audit → secret scan → Docker build
      → image scans → Kubernetes check → GHCR
```

Bandit checks the Python source. pip-audit and npm audit check dependencies, Gitleaks checks for secrets, and Trivy scans both images. HIGH or CRITICAL image findings stop the pipeline. Images are published only after the checks pass.

The first image scans found vulnerable runtime packages. I updated those packages and removed unneeded pip tooling from the backend image. Both rebuilt images then passed the same scan gate.

- [Workflow](../.github/workflows/devops.yml)
- [Security checks and results](../demo-app/security/README.md)
- [Successful CI run](https://github.com/ThereIsSomething/devops-work/actions/runs/37630785578)
- [Successful Azure deployment](https://github.com/ThereIsSomething/devops-work/actions/runs/37631537431)

The Azure workflow uses OIDC and deploys the exact image SHA from a successful CI run. It checks application health, database readiness and the Ingress route.
