# Session 15: Helm

**Nitish Kumar Bhambu — 24BCS10589**

A chart is a package of templates; values are its inputs; a release is an installed instance. My mini project is a small guestbook welcome page stored in a ConfigMap and served by Nginx. The Deployment includes a checksum of the message so a values change triggers a rollout.

The complete sequence is install version one → verify page → upgrade to version two → verify → upgrade to version three → verify → rollback to revision 1 → verify the original page → uninstall. A rollback creates a new release revision; it does not erase the upgrade history.

| Command | Purpose |
|---|---|
| helm create | Generate a chart scaffold in generated-example/ |
| helm repo add/update | Register and refresh a remote chart index |
| helm search repo | Find charts in that index |
| helm lint/template | Validate chart structure and inspect rendered resources |
| helm install / upgrade --install | Install a release; upgrade --install is convenient for repeated deployments |
| helm list/status/get | Inspect releases, status, values and manifests |
| helm upgrade/history/rollback | Apply changes, inspect revisions and restore earlier configuration |
| helm uninstall | Remove release resources |

The transcript uses `upgrade --install` for the guestbook; a separate explicit `helm install` command is recorded in the supplementary output. The generated chart is retained to demonstrate `helm create`; the authored guestbook chart is in `chart/`.

```bash
python3 scripts/run_kubernetes_labs.py 15
```

Reference: [Helm commands](https://helm.sh/docs/helm/).

## Execution evidence

Actual local transcripts are included below after the runs finish. A missing or incomplete transcript is not a completed exercise.

<!-- EVIDENCE -->

### explicit-install.txt

[Complete transcript](outputs/explicit-install.txt)

````text
$ helm install explicit-install 14-helm/chart -n homework-s15 --wait
NAME: explicit-install
LAST DEPLOYED: Wed Oct  7 18:32:23 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
$ helm uninstall explicit-install -n homework-s15
release "explicit-install" uninstalled
````

### run.txt

[Complete transcript](outputs/run.txt)

````text
Captured 2026-10-07T12:58:51.875277+00:00
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' create namespace homework-s15
namespace/homework-s15 created
[exit 0]
$ helm create '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/14-helm/generated-example'
Creating /home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/14-helm/generated-example
[exit 0]
$ helm repo add traefik https://traefik.github.io/charts --force-update
"traefik" has been added to your repositories
[exit 0]
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "traefik" chart repository
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈
[exit 0]
$ helm search repo traefik/traefik --versions
NAME                	CHART VERSION	APP VERSION	DESCRIPTION
traefik/traefik     	41.6.1       	v3.7.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.6.0       	v3.7.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.5.0       	v3.7.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.4.0       	v3.7.12    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.3.0       	v3.7.11    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.2.0       	v3.7.10    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.1.1       	v3.7.9     	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.1.0       	v3.7.9     	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.0.2       	v3.7.6     	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.0.1       	v3.7.5     	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.0.0       	v3.7.5     	A Traefik based Kubernetes ingress controller
traefik/traefik     	40.3.0       	v3.7.4     	A Traefik based Kubernetes ingress controller
traefik/traefik     	40.2.0       	v3.7.1     	A Traefik based Kubernetes ingress controller
traefik/traefik     	40.1.0       	v3.7.1     	A Traefik based Kubernetes ingress controller
traefik/traefik     	40.0.1       	v3.7.0     	A Traefik based Kubernetes ingress controller
traefik/traefik     	40.0.0       	v3.7.0     	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.9       	v3.6.15    	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.8       	v3.6.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.7       	v3.6.12    	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.6       	v3.6.11    	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.5       	v3.6.10    	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.4       	v3.6.9     	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.3       	v3.6.9     	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.2       	v3.6.8     	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.1       	v3.6.8     	A Traefik based Kubernetes ingress controller
traefik/traefik     	39.0.0       	v3.6.7     	A Traefik based Kubernetes ingress controller
traefik/traefik     	38.0.2       	v3.6.6     	A Traefik based Kubernetes ingress controller
traefik/traefik     	38.0.1       	v3.6.5     	A Traefik based Kubernetes ingress controller
traefik/traefik     	38.0.0       	v3.6.5     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.4.0       	v3.6.2     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.3.0       	v3.6.0     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.2.0       	v3.5.3     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.1.2       	v3.5.3     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.1.1       	v3.5.2     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.1.0       	v3.5.1     	A Traefik based Kubernetes ingress controller
traefik/traefik     	37.0.0       	v3.5.0     	A Traefik based Kubernetes ingress controller
traefik/traefik     	36.3.0       	v3.4.3     	A Traefik based Kubernetes ingress controller
traefik/traefik     	36.2.0       	v3.4.1     	A Traefik based Kubernetes ingress controller
traefik/traefik     	36.1.0       	v3.4.1     	A Traefik based Kubernetes ingress controller
traefik/traefik     	36.0.0       	v3.4.1     	A Traefik based Kubernetes ingress controller
traefik/traefik     	35.4.0       	v3.4.0     	A Traefik based Kubernetes ingress controller
traefik/traefik     	35.3.0       	v3.4.0     	A Traefik based Kubernetes ingress controller
traefik/traefik     	35.2.0       	v3.3.6     	A Traefik based Kubernetes ingress controller
traefik/traefik     	35.1.0       	v3.3.6     	A Traefik based Kubernetes ingress controller
traefik/traefik     	35.0.1       	v3.3.6     	A Traefik based Kubernetes ingress controller
traefik/traefik     	35.0.0       	v3.3.5     	A Traefik based Kubernetes ingress controller
traefik/traefik     	34.5.0       	v3.3.4     	A Traefik based Kubernetes ingress controller

[Excerpt: 590 intermediate lines omitted; complete transcript linked above.]

      containers:
        - name: nginx
          image: "nginx:1.28-alpine"
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
          resources:
            requests:
              cpu: 25m
              memory: 16Mi
            limits:
              cpu: 250m
              memory: 64Mi
          volumeMounts:
            - name: page
              mountPath: /usr/share/nginx/html
      volumes:
        - name: page
          configMap:
            name: guestbook-page
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s15 exec client -- wget -qO- http://guestbook
Welcome to my guestbook - version one
[exit 0]
$ helm upgrade guestbook 14-helm/chart -n homework-s15 --set 'message=Welcome to my guestbook - version two' --wait --timeout 180s
Release "guestbook" has been upgraded. Happy Helming!
NAME: guestbook
LAST DEPLOYED: Wed Oct  7 18:29:38 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete
TEST SUITE: None
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s15 exec client -- wget -qO- http://guestbook
Welcome to my guestbook - version two
[exit 0]
$ helm upgrade guestbook 14-helm/chart -n homework-s15 --set 'message=Welcome to my guestbook - version three' --wait --timeout 180s
Release "guestbook" has been upgraded. Happy Helming!
NAME: guestbook
LAST DEPLOYED: Wed Oct  7 18:29:51 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 3
DESCRIPTION: Upgrade complete
TEST SUITE: None
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s15 exec client -- wget -qO- http://guestbook
wget: can't connect to remote host (10.104.209.237): Connection refused
command terminated with exit code 1
[exit 1]
$ helm history guestbook -n homework-s15
REVISION	UPDATED                 	STATUS    	CHART             	APP VERSION	DESCRIPTION
1       	Wed Oct  7 18:29:33 2026	superseded	homework-web-0.1.0	1.28       	Install complete
2       	Wed Oct  7 18:29:38 2026	superseded	homework-web-0.1.0	1.28       	Upgrade complete
3       	Wed Oct  7 18:29:51 2026	deployed  	homework-web-0.1.0	1.28       	Upgrade complete
[exit 0]
$ helm rollback guestbook 1 -n homework-s15 --wait --timeout 180s
Rollback was a success! Happy Helming!
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s15 exec client -- wget -qO- http://guestbook
Welcome to my guestbook - version one
[exit 0]
$ helm history guestbook -n homework-s15
REVISION	UPDATED                 	STATUS    	CHART             	APP VERSION	DESCRIPTION
1       	Wed Oct  7 18:29:33 2026	superseded	homework-web-0.1.0	1.28       	Install complete
2       	Wed Oct  7 18:29:38 2026	superseded	homework-web-0.1.0	1.28       	Upgrade complete
3       	Wed Oct  7 18:29:51 2026	superseded	homework-web-0.1.0	1.28       	Upgrade complete
4       	Wed Oct  7 18:30:04 2026	deployed  	homework-web-0.1.0	1.28       	Rollback to 1
[exit 0]
$ helm uninstall guestbook -n homework-s15
release "guestbook" uninstalled
[exit 0]
$ helm list -n homework-s15
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
[exit 0]
LAB EXECUTION FINISHED
````
