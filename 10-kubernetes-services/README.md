# Session 11: Kubernetes Networking and Services

**Nitish Kumar Bhambu — 24BCS10589**

| Service | What I use it for | Verification |
|---|---|---|
| ClusterIP | Stable internal address for Pods | HTTP request from client Pod |
| NodePort | Node IP plus an allocated port | HTTP request from this laptop to Minikube IP |
| LoadBalancer | Request an external load balancer from an implementation | Service inspected; internal HTTP tested |
| ExternalName | Return a DNS alias for an external name | nslookup shows the alias; it does not proxy traffic |
| Headless | Discover individual endpoint IPs without a virtual ClusterIP | DNS returns Pod IPs; HTTP tested |

Headless is a configuration (`clusterIP: None`), not an additional value of `spec.type`. On Minikube without a tunnel or load-balancer implementation, EXTERNAL-IP remains `<pending>`. I also tested a public LoadBalancer on AKS; its results are linked below.

## Object comparisons

| Object | Main job | Scaling and updates | Networking/storage |
|---|---|---|---|
| Deployment | Manage stateless application revisions | Creates ReplicaSets; supports rolling updates and rollback | Replaceable Pod identities; storage can be attached |
| ReplicaSet | Keep the requested number of matching Pods alive | Scales Pods; does not implement Deployment-style rollout history | Uses labels; does not provide a traffic entry point |
| DaemonSet | Run a Pod on each eligible node, e.g. log collector | Node membership controls count | Usually node-local identity/data |
| StatefulSet | Manage stateful replicas, e.g. database members | Ordered identities and controlled scaling/update | Stable names; commonly one PVC per replica with a headless Service |
| Service | Provide discovery/access to selected ready endpoints | Does not create or scale Pods | Stable DNS/address; routes to endpoints selected by labels |

A Deployment owns ReplicaSets; each ReplicaSet owns Pods. A Service selects Pods using labels, independently of that ownership chain. Traffic goes to a Service address and is forwarded to an eligible endpoint through the cluster's networking implementation. Replacing a Pod does not require clients to discover its new IP themselves.

See [FQDN notes](fqdn/README.md) and [CoreDNS notes](coredns/README.md).

```bash
kubectl -n homework-s11 apply -f 10-kubernetes-services/
kubectl -n homework-s11 get svc
```

Reference: [Service](https://kubernetes.io/docs/concepts/services-networking/service/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

## Real cloud LoadBalancer verification

The Minikube LoadBalancer Service initially remained Pending because it had no cloud load-balancer controller or active tunnel. The real AKS deployment supplies that controller. Its temporary frontend LoadBalancer, assigned public IP and HTTP response are recorded in the [Azure LoadBalancer and persistence test](../final-devops-project/README.md#azure-browser-evidence). The service is restored to ClusterIP before cloud cleanup.

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s11
namespace/homework-s11 created

zephoryx@fedora$ kubectl -n homework-s11 apply -f 10-kubernetes-services/app.yaml
deployment.apps/web created

zephoryx@fedora$ kubectl -n homework-s11 rollout status deployment/web
Waiting for deployment "web" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web" rollout to finish: 1 of 2 updated replicas are available...
deployment "web" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s11 apply -f 10-kubernetes-services/clusterip.yaml
service/clusterip created

zephoryx@fedora$ kubectl -n homework-s11 apply -f 10-kubernetes-services/nodeport.yaml
service/nodeport created

zephoryx@fedora$ kubectl -n homework-s11 apply -f 10-kubernetes-services/loadbalancer.yaml
service/loadbalancer created

zephoryx@fedora$ kubectl -n homework-s11 apply -f 10-kubernetes-services/externalname.yaml
service/externalname created

zephoryx@fedora$ kubectl -n homework-s11 apply -f 10-kubernetes-services/headless.yaml
service/headless created

zephoryx@fedora$ kubectl -n homework-s11 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s11 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ kubectl -n homework-s11 get svc -o wide
NAME           TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE   SELECTOR
clusterip      ClusterIP      10.111.252.56    <none>        80/TCP         4s    app=web
externalname   ExternalName   <none>           example.com   <none>         2s    <none>
headless       ClusterIP      None             <none>        80/TCP         2s    app=web
loadbalancer   LoadBalancer   10.98.166.22     <pending>     80:31600/TCP   3s    app=web
nodeport       NodePort       10.108.135.157   <none>        80:30183/TCP   4s    app=web

zephoryx@fedora$ kubectl -n homework-s11 exec client -- wget -qO- http://clusterip
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s11 exec client -- wget -qO- http://nodeport
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s11 exec client -- wget -qO- http://loadbalancer
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s11 exec client -- wget -qO- http://headless
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s11 exec client -- nslookup clusterip.homework-s11.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10:53

Name:	clusterip.homework-s11.svc.cluster.local
Address: 10.111.252.56

zephoryx@fedora$ kubectl -n homework-s11 exec client -- nslookup headless.homework-s11.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10:53

Name:	headless.homework-s11.svc.cluster.local
Address: 10.244.0.52
Name:	headless.homework-s11.svc.cluster.local
Address: 10.244.0.51

zephoryx@fedora$ kubectl -n homework-s11 exec client -- nslookup externalname.homework-s11.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10:53

externalname.homework-s11.svc.cluster.local	canonical name = example.com
Name:	example.com
Address: 172.66.147.243
Name:	example.com
Address: 104.20.23.154

externalname.homework-s11.svc.cluster.local	canonical name = example.com
Name:	example.com
Address: 2606:4700:10::6814:179a
Name:	example.com
Address: 2606:4700:10::ac42:93f3

zephoryx@fedora$ kubectl -n homework-s11 get svc nodeport -o 'jsonpath={.spec.ports[0].nodePort}'
30183

zephoryx@fedora$ minikube ip
192.168.49.2

zephoryx@fedora$ curl -f --max-time 10 http://192.168.49.2:30183
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s11 describe svc loadbalancer
Name:                     loadbalancer
Namespace:                homework-s11
Labels:                   <none>
Annotations:              <none>
# ... output shortened ...
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>

zephoryx@fedora$ kubectl -n homework-s11 get configmap coredns -n kube-system -o yaml
apiVersion: v1
data:
  Corefile: |
    .:53 {
        log
        errors
# ... intermediate output omitted ...
kind: ConfigMap
metadata:
  creationTimestamp: "2026-09-08T11:34:57Z"
  name: coredns
  namespace: kube-system
  resourceVersion: "324"
  uid: fc9370fa-d33b-4958-ba9f-33855261a450

zephoryx@fedora$ kubectl -n homework-s11 logs -n kube-system -l k8s-app=kube-dns --tail=20
[INFO] 10.244.0.34:46446 - 51521 "AAAA IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 148 0.000423986s
[INFO] 10.244.0.34:46446 - 60760 "A IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 108 0.000612513s
[INFO] 10.244.0.34:44347 - 62414 "AAAA IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 148 0.000471602s
[INFO] 10.244.0.34:44347 - 27845 "A IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 108 0.001237907s
# ... output shortened ...
[INFO] 10.244.0.53:54156 - 52534 "A IN headless.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 167 0.000762242s
[INFO] 10.244.0.53:54945 - 12001 "A IN example.com. udp 29 false 512" NOERROR qr,rd,ra 83 0.116803615s
[INFO] 10.244.0.53:54945 - 12001 "A IN externalname.homework-s11.svc.cluster.local. udp 61 false 512" NOERROR qr,aa,rd 183 0.146253949s
[INFO] 10.244.0.53:54945 - 12002 "AAAA IN example.com. udp 29 false 512" NOERROR qr,rd,ra 107 0.156911551s
[INFO] 10.244.0.53:54945 - 12002 "AAAA IN externalname.homework-s11.svc.cluster.local. udp 61 false 512" NOERROR qr,aa,rd 207 0.163896462s
```
