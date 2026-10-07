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

I used `upgrade --install` for the guestbook and also tested an explicit `helm install`, shown below. The generated chart is retained to demonstrate `helm create`; the authored guestbook chart is in `chart/`.

```bash
helm lint 14-helm/chart
helm list -n homework-s15
helm history guestbook -n homework-s15
```

Reference: [Helm commands](https://helm.sh/docs/helm/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

### Explicit Helm install

```bash
zephoryx@fedora$ helm install explicit-install 14-helm/chart -n homework-s15 --wait
NAME: explicit-install
LAST DEPLOYED: Wed Oct  7 18:32:23 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None

zephoryx@fedora$ helm uninstall explicit-install -n homework-s15
release "explicit-install" uninstalled
```

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s15
namespace/homework-s15 created

zephoryx@fedora$ helm create '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/14-helm/generated-example'
Creating /home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/14-helm/generated-example

zephoryx@fedora$ helm repo add traefik https://traefik.github.io/charts --force-update
"traefik" has been added to your repositories

zephoryx@fedora$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "traefik" chart repository
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈

zephoryx@fedora$ helm search repo traefik/traefik --versions
NAME                	CHART VERSION	APP VERSION	DESCRIPTION
traefik/traefik     	41.6.1       	v3.7.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.6.0       	v3.7.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.5.0       	v3.7.13    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.4.0       	v3.7.12    	A Traefik based Kubernetes ingress controller
traefik/traefik     	41.3.0       	v3.7.11    	A Traefik based Kubernetes ingress controller
# ... intermediate output omitted ...
traefik/traefikee   	0.1.7        	2.5.6      	Traefik Enterprise is a unified cloud-native ne...
traefik/traefikee   	0.1.6        	2.5.3      	Traefik Enterprise is a unified cloud-native ne...
traefik/traefikee   	0.1.5        	2.5.3      	Traefik Enterprise is a unified cloud-native ne...
traefik/traefikee   	0.1.4        	2.5.2      	Traefik Enterprise is a unified cloud-native ne...
traefik/traefikee   	0.1.3        	2.5.1      	Traefik Enterprise is a unified cloud-native ne...
traefik/traefikee   	0.1.2        	2.5.0      	Traefik Enterprise is a unified cloud-native ne...
traefik/traefikee   	0.1.1        	2.5.0      	Traefik Enterprise is a unified cloud-native ne...

zephoryx@fedora$ helm lint 14-helm/chart
==> Linting 14-helm/chart
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed

zephoryx@fedora$ helm template guestbook 14-helm/chart -n homework-s15
---
# Source: homework-web/templates/app.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: guestbook-page
# ... intermediate output omitted ...
          volumeMounts:
            - name: page
              mountPath: /usr/share/nginx/html
      volumes:
        - name: page
          configMap:
            name: guestbook-page

zephoryx@fedora$ helm upgrade --install guestbook 14-helm/chart -n homework-s15 --wait --timeout 180s
Release "guestbook" does not exist. Installing it now.
NAME: guestbook
LAST DEPLOYED: Wed Oct  7 18:29:33 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None

zephoryx@fedora$ kubectl -n homework-s15 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s15 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ helm list -n homework-s15
NAME     	NAMESPACE   	REVISION	UPDATED                                	STATUS  	CHART             	APP VERSION
guestbook	homework-s15	1       	2026-10-07 18:29:33.625287824 +0530 IST	deployed	homework-web-0.1.0	1.28

zephoryx@fedora$ helm status guestbook -n homework-s15
NAME: guestbook
LAST DEPLOYED: Wed Oct  7 18:29:33 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
# ... intermediate output omitted ...
guestbook   1/1     1            1           4s

==> v1/Pod(related)
NAME                         READY   STATUS    RESTARTS   AGE
guestbook-5d65948446-tmqdq   1/1     Running   0          3s

TEST SUITE: None

zephoryx@fedora$ helm get values guestbook -n homework-s15
USER-SUPPLIED VALUES:
null

zephoryx@fedora$ helm get manifest guestbook -n homework-s15
---
# Source: homework-web/templates/app.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: guestbook-page
# ... intermediate output omitted ...
          volumeMounts:
            - name: page
              mountPath: /usr/share/nginx/html
      volumes:
        - name: page
          configMap:
            name: guestbook-page

zephoryx@fedora$ kubectl -n homework-s15 exec client -- wget -qO- http://guestbook
Welcome to my guestbook - version one

zephoryx@fedora$ helm upgrade guestbook 14-helm/chart -n homework-s15 --set 'message=Welcome to my guestbook - version two' --wait --timeout 180s
Release "guestbook" has been upgraded. Happy Helming!
NAME: guestbook
LAST DEPLOYED: Wed Oct  7 18:29:38 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete
TEST SUITE: None

zephoryx@fedora$ kubectl -n homework-s15 exec client -- wget -qO- http://guestbook
Welcome to my guestbook - version two

zephoryx@fedora$ helm upgrade guestbook 14-helm/chart -n homework-s15 --set 'message=Welcome to my guestbook - version three' --wait --timeout 180s
Release "guestbook" has been upgraded. Happy Helming!
NAME: guestbook
LAST DEPLOYED: Wed Oct  7 18:29:51 2026
NAMESPACE: homework-s15
STATUS: deployed
REVISION: 3
DESCRIPTION: Upgrade complete
TEST SUITE: None

zephoryx@fedora$ kubectl -n homework-s15 exec client -- wget -qO- http://guestbook
wget: can't connect to remote host (10.104.209.237): Connection refused
command terminated with exit code 1
# Exit status: 1

zephoryx@fedora$ helm history guestbook -n homework-s15
REVISION	UPDATED                 	STATUS    	CHART             	APP VERSION	DESCRIPTION
1       	Wed Oct  7 18:29:33 2026	superseded	homework-web-0.1.0	1.28       	Install complete
2       	Wed Oct  7 18:29:38 2026	superseded	homework-web-0.1.0	1.28       	Upgrade complete
3       	Wed Oct  7 18:29:51 2026	deployed  	homework-web-0.1.0	1.28       	Upgrade complete

zephoryx@fedora$ helm rollback guestbook 1 -n homework-s15 --wait --timeout 180s
Rollback was a success! Happy Helming!

zephoryx@fedora$ kubectl -n homework-s15 exec client -- wget -qO- http://guestbook
Welcome to my guestbook - version one

zephoryx@fedora$ helm history guestbook -n homework-s15
REVISION	UPDATED                 	STATUS    	CHART             	APP VERSION	DESCRIPTION
1       	Wed Oct  7 18:29:33 2026	superseded	homework-web-0.1.0	1.28       	Install complete
2       	Wed Oct  7 18:29:38 2026	superseded	homework-web-0.1.0	1.28       	Upgrade complete
3       	Wed Oct  7 18:29:51 2026	superseded	homework-web-0.1.0	1.28       	Upgrade complete
4       	Wed Oct  7 18:30:04 2026	deployed  	homework-web-0.1.0	1.28       	Rollback to 1

zephoryx@fedora$ helm uninstall guestbook -n homework-s15
release "guestbook" uninstalled

zephoryx@fedora$ helm list -n homework-s15
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
```
