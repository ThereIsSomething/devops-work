# Session 11: Kubernetes Networking and Services

**Nitish Kumar Bhambu — 24BCS10589**

| Service | What I use it for | Verification |
|---|---|---|
| ClusterIP | Stable internal address for Pods | HTTP request from client Pod |
| NodePort | Node IP plus an allocated port | HTTP request from this laptop to Minikube IP |
| LoadBalancer | Request an external load balancer from an implementation | Service inspected; internal HTTP tested |
| ExternalName | Return a DNS alias for an external name | nslookup shows the alias; it does not proxy traffic |
| Headless | Discover individual endpoint IPs without a virtual ClusterIP | DNS returns Pod IPs; HTTP tested |

Headless is a configuration (`clusterIP: None`), not an additional value of `spec.type`. On Minikube without a tunnel or load-balancer implementation, EXTERNAL-IP remains `<pending>`. The transcript records that limitation honestly. Internal success does not prove external LoadBalancer access. To complete the external portion, run `minikube tunnel` in a separate local terminal, inspect `kubectl get svc`, and test the assigned address.

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
python3 scripts/run_kubernetes_labs.py 11
```

Reference: [Service](https://kubernetes.io/docs/concepts/services-networking/service/).

## Execution evidence

Actual local transcripts are included below after the runs finish. A missing or incomplete transcript is not a completed exercise.


## Real cloud LoadBalancer verification

The Minikube LoadBalancer Service initially remained Pending because it had no cloud load-balancer controller or active tunnel. The real AKS deployment supplies that controller. Its temporary frontend LoadBalancer, assigned public IP and HTTP response are recorded in the [Azure functional test](../final-devops-project/outputs/azure-functional.txt). The service is restored to ClusterIP before cloud cleanup.

<!-- EVIDENCE -->

### run.txt

[Complete transcript](outputs/run.txt)

````text
Captured 2026-10-07T12:53:16.964682+00:00
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' create namespace homework-s11
namespace/homework-s11 created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 apply -f 10-kubernetes-services/app.yaml
deployment.apps/web created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 rollout status deployment/web --timeout=180s
Waiting for deployment "web" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web" rollout to finish: 1 of 2 updated replicas are available...
deployment "web" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 apply -f 10-kubernetes-services/clusterip.yaml
service/clusterip created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 apply -f 10-kubernetes-services/nodeport.yaml
service/nodeport created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 apply -f 10-kubernetes-services/loadbalancer.yaml
service/loadbalancer created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 apply -f 10-kubernetes-services/externalname.yaml
service/externalname created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 apply -f 10-kubernetes-services/headless.yaml
service/headless created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 wait --for=condition=Ready pod/client --timeout=120s
pod/client condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 get svc -o wide
NAME           TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE   SELECTOR
clusterip      ClusterIP      10.111.252.56    <none>        80/TCP         4s    app=web
externalname   ExternalName   <none>           example.com   <none>         2s    <none>
headless       ClusterIP      None             <none>        80/TCP         2s    app=web
loadbalancer   LoadBalancer   10.98.166.22     <pending>     80:31600/TCP   3s    app=web
nodeport       NodePort       10.108.135.157   <none>        80:30183/TCP   4s    app=web
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 exec client -- wget -qO- http://clusterip
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

[Excerpt: 150 intermediate lines omitted; complete transcript linked above.]

Labels:                   <none>
Annotations:              <none>
Selector:                 app=web
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.98.166.22
IPs:                      10.98.166.22
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31600/TCP
Endpoints:                10.244.0.52:80,10.244.0.51:80
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 get configmap coredns -n kube-system -o yaml
apiVersion: v1
data:
  Corefile: |
    .:53 {
        log
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        hosts {
           192.168.49.1 host.minikube.internal
           fallthrough
        }
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30 {
           disable success cluster.local
           disable denial cluster.local
        }
        loop
        reload
        loadbalance
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2026-09-08T11:34:57Z"
  name: coredns
  namespace: kube-system
  resourceVersion: "324"
  uid: fc9370fa-d33b-4958-ba9f-33855261a450
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s11 logs -n kube-system -l k8s-app=kube-dns --tail=20
[INFO] 10.244.0.34:46446 - 51521 "AAAA IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 148 0.000423986s
[INFO] 10.244.0.34:46446 - 60760 "A IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 108 0.000612513s
[INFO] 10.244.0.34:44347 - 62414 "AAAA IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 148 0.000471602s
[INFO] 10.244.0.34:44347 - 27845 "A IN canary.homework-s10.svc.cluster.local. udp 55 false 512" NOERROR qr,aa,rd 108 0.001237907s
[INFO] 10.244.0.53:55519 - 47533 "A IN clusterip.homework-s11.svc.cluster.local. udp 58 false 512" NOERROR qr,aa,rd 114 0.00092573s
[INFO] 10.244.0.53:55519 - 29119 "AAAA IN clusterip.homework-s11.svc.cluster.local. udp 58 false 512" NOERROR qr,aa,rd 151 0.001117543s
[INFO] 10.244.0.53:37065 - 61062 "AAAA IN nodeport.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 150 0.000703172s
[INFO] 10.244.0.53:37065 - 62081 "A IN nodeport.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 112 0.000925065s
[INFO] 10.244.0.53:54620 - 8467 "A IN loadbalancer.homework-s11.svc.cluster.local. udp 61 false 512" NOERROR qr,aa,rd 120 0.00035621s
[INFO] 10.244.0.53:54620 - 12296 "AAAA IN loadbalancer.homework-s11.svc.cluster.local. udp 61 false 512" NOERROR qr,aa,rd 154 0.000535757s
[INFO] 10.244.0.53:40069 - 54166 "AAAA IN headless.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 150 0.000355091s
[INFO] 10.244.0.53:40069 - 58013 "A IN headless.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 167 0.000408945s
[INFO] 10.244.0.53:36319 - 23899 "A IN clusterip.homework-s11.svc.cluster.local. udp 58 false 512" NOERROR qr,aa,rd 114 0.000463592s
[INFO] 10.244.0.53:36319 - 23900 "AAAA IN clusterip.homework-s11.svc.cluster.local. udp 58 false 512" NOERROR qr,aa,rd 151 0.000414202s
[INFO] 10.244.0.53:54156 - 52535 "AAAA IN headless.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 150 0.000582124s
[INFO] 10.244.0.53:54156 - 52534 "A IN headless.homework-s11.svc.cluster.local. udp 57 false 512" NOERROR qr,aa,rd 167 0.000762242s
[INFO] 10.244.0.53:54945 - 12001 "A IN example.com. udp 29 false 512" NOERROR qr,rd,ra 83 0.116803615s
[INFO] 10.244.0.53:54945 - 12001 "A IN externalname.homework-s11.svc.cluster.local. udp 61 false 512" NOERROR qr,aa,rd 183 0.146253949s
[INFO] 10.244.0.53:54945 - 12002 "AAAA IN example.com. udp 29 false 512" NOERROR qr,rd,ra 107 0.156911551s
[INFO] 10.244.0.53:54945 - 12002 "AAAA IN externalname.homework-s11.svc.cluster.local. udp 61 false 512" NOERROR qr,aa,rd 207 0.163896462s
[exit 0]
LAB EXECUTION FINISHED
````
