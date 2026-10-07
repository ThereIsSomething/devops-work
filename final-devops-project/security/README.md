# Security gates

The executable workflow is at the repository root: [devops.yml](../../.github/workflows/devops.yml). The nested copy is a reference for the required final-project folder layout; GitHub does not execute workflows from this nested folder.

| Stage | Tool | Failure condition |
|---|---|---|
| Tests | pytest | Any failing test |
| SAST | Bandit | Medium-or-higher severity and medium-or-higher confidence |
| SCA | pip-audit and npm audit | Any known Python finding; high-or-higher npm finding |
| Secrets | Gitleaks | A detected secret in Git history |
| Container scan | Trivy | Any HIGH or CRITICAL vulnerability, including unfixed findings |

Images are published only after tests, source checks, both image scans and a deployment smoke test pass. There are no `continue-on-error` bypasses on these gates. An unfixed vulnerability can legitimately prevent a release; retain the report and investigate rather than calling a failed scan successful.

`secret.example.yaml` contains a labelled, disposable classroom value. Real credentials are created outside Git and referenced by name. Base64 is reversible encoding, not encryption. Terraform state and real `.env` files are ignored. Kubernetes Secret access also needs RBAC and suitable encryption-at-rest configuration in a real cluster.

A passing scan means the configured checks found no matching issue using the available rules and advisory databases at that time. It does not prove that the application has no vulnerabilities. This classroom API has no user authentication and should not be exposed as a production service.

References: [Bandit](https://bandit.readthedocs.io/), [pip-audit](https://github.com/pypa/pip-audit), [Gitleaks](https://github.com/gitleaks/gitleaks), [Trivy](https://github.com/aquasecurity/trivy).

## Findings fixed during this run

The first image scans failed: the Debian-based backend had 44 HIGH operating-system findings and four HIGH Python packaging-tool findings; the frontend had 43 HIGH Alpine findings. I moved the backend to Alpine, upgraded the runtime OS packages in both images, and removed pip from the finished backend image after installing its locked dependencies. The application does not need pip at runtime. Both rebuilt application images then passed the same HIGH/CRITICAL gate with zero matching findings. No advisory was ignored to make the gate pass.

The hosted Gitleaks history scan also passed. See the [final project results](../README.md#test-and-security-results) and the linked Actions run for the checks.
