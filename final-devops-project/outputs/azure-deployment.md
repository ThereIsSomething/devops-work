# Hosted Azure deployment

[Final Azure Actions run 37631537431](https://github.com/ThereIsSomething/devops-work/actions/runs/37631537431) completed successfully against the corrected chart, using the verified application image commit `e45aaec63c7220da29f099eecb0f16d6f30ceb21`. [Complete job log](azure-deploy-final.txt).

The runner authenticated with OIDC, added only its current source IP to the API allowlist, retrieved user credentials, deployed the SHA-tagged GHCR images with Helm, verified health, database readiness and API responses, tested the Traefik route, installed Prometheus/Grafana and restored the original API allowlist. No manual patch was needed in this final rerun.

An earlier [Azure run 37629943927](https://github.com/ThereIsSomething/devops-work/actions/runs/37629943927) completed after manual recovery of the managed-disk initialization issue. The corrected source was then redeployed to remove that dependency on manual intervention.

The [public-IP and storage test](azure-functional.txt) created a task, replaced the PostgreSQL Pod, read the same task back from the persistent disk and deleted it. The real browser screenshot is in `../screenshots/azure-taskboard.jpg`. The temporary LoadBalancer service was restored to ClusterIP. [Cloud monitoring evidence](azure-monitoring.txt) shows both scrape targets up and no active unavailable alert.

The lab is destroyed after these checks. [Terraform destroy and final Azure inventory](azure-destroy.txt) record cleanup; the public IP is historical evidence.
