# Security checks

These checks run in [devops.yml](../../.github/workflows/devops.yml). A failed gate stops image publication.

| Stage | Tool | Failure condition |
|---|---|---|
| Tests | pytest | Any failing test |
| SAST | Bandit | Medium-or-higher severity and medium-or-higher confidence |
| SCA | pip-audit and npm audit | Any known Python finding; high-or-higher npm finding |
| Secrets | Gitleaks | A detected secret in Git history |
| Container scan | Trivy | Any HIGH or CRITICAL vulnerability, including unfixed findings |

## Scan results

The first backend scan found 44 HIGH OS findings and four HIGH packaging-tool findings. The frontend had 43 HIGH findings. I moved the backend to Alpine, upgraded the runtime packages and removed pip from the finished backend image. Both rebuilt images had zero HIGH or CRITICAL findings without ignoring advisories.

Gitleaks also passed. A clean result means the configured checks found no matching issues with the advisory data available during that run.

The example Kubernetes Secret is a dummy lab value. Real secrets, `.env` files and Terraform state stay out of Git.

[Successful pipeline](https://github.com/ThereIsSomething/devops-work/actions/runs/37630785578)
