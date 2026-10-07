# Hosted CI evidence

The successful run for commit `9d85fe3d871c2ba5ce87c77e33181978a1112fc0` is [GitHub Actions run 37629099243](https://github.com/ThereIsSomething/devops-work/actions/runs/37629099243). Both jobs passed: tests/build/source security checks, then both image scans, a real Helm deployment in kind, HTTP verification, GHCR publication and temporary-cluster cleanup. [Complete job log](hosted-ci-latest.txt).

Published images:

```text
ghcr.io/thereissomething/devops-work-backend:9d85fe3d871c2ba5ce87c77e33181978a1112fc0
ghcr.io/thereissomething/devops-work-frontend:9d85fe3d871c2ba5ce87c77e33181978a1112fc0
```

An earlier successful run for commit `1924ccc230469d4a03a143cf3e063f72b6aa28b1` is [run 37628274945](https://github.com/ThereIsSomething/devops-work/actions/runs/37628274945); its [log](hosted-ci-success.txt) is also retained. An initial run was cancelled by a later source push and is not counted as a passing deployment.

The corrected managed-disk and GitOps ordering changes also passed [run 37630785578](https://github.com/ThereIsSomething/devops-work/actions/runs/37630785578), commit `e45aaec63c7220da29f099eecb0f16d6f30ceb21`. [Complete final CI log](hosted-ci-final.txt). Its application images use that same SHA tag and are the images used in the final Azure rerun.
