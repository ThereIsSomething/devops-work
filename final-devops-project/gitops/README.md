# GitOps connection

The runnable GitOps mini project is in [Session 20](../../19-monitoring-gitops/README.md). Argo CD watches a dedicated workload path in this repository, synchronizes it and repairs replica drift. That workload is separate from the manually Helm-managed TaskBoard release; two controllers should not compete for the same desired state.

To move TaskBoard itself to GitOps after GHCR publishing, set the published SHA image tags in a committed Helm values file, configure an Argo CD Application using `path: final-devops-project/helm/taskboard` and that values file, provision its external Secret, and transfer management to Argo CD. The current final deployment remains managed by Helm.
