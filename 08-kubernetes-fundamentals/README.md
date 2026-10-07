# Session 9: Kubernetes Fundamentals

**Nitish Kumar Bhambu — 24BCS10589**

A Kubernetes cluster has a control plane and worker nodes. The API server accepts requests, etcd stores cluster state, the scheduler selects a node, and controllers keep actual state close to the declared state. On each node, kubelet manages Pods, the container runtime runs containers, and networking components provide connectivity. Minikube combines these roles on one local node here.

A Pod is the smallest scheduling unit. A Deployment manages ReplicaSets, which maintain a desired number of Pods. A Service gives changing Pods a stable access point. Labels connect these objects.

The exercise follows the basic tutorial flow: deploy, inspect, expose, reach the application, scale, update and roll back. `kubectl get` is a summary; `describe` explains details and events; `logs` reads the application output. On my laptop, `kubectl` is an alias for the Minikube client.

```bash
minikube status
kubectl get nodes
kubectl get pods -n kube-system
```

Reference: [Kubernetes basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s09
namespace/homework-s09 created

zephoryx@fedora$ minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

zephoryx@fedora$ kubectl -n homework-s09 cluster-info
Kubernetes control plane is running at https://192.168.49.2:8443

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

zephoryx@fedora$ kubectl -n homework-s09 get nodes -o wide
NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION                  CONTAINER-RUNTIME
minikube   Ready    control-plane   29d   v1.37.0   192.168.49.2   <none>        Debian GNU/Linux 12 (bookworm)   7.2.8-200.fc44.x86_64 (amd64)   containerd://2.3.4

zephoryx@fedora$ kubectl -n homework-s09 get pods -n kube-system
NAME                               READY   STATUS    RESTARTS       AGE
coredns-559f6c778d-46j8r           1/1     Running   8 (16m ago)    29d
etcd-minikube                      1/1     Running   7 (16m ago)    29d
kindnet-k448g                      1/1     Running   8 (16m ago)    29d
kube-apiserver-minikube            1/1     Running   8 (16m ago)    29d
kube-controller-manager-minikube   1/1     Running   7 (16m ago)    29d
kube-proxy-dn285                   1/1     Running   7 (16m ago)    29d
kube-scheduler-minikube            1/1     Running   7 (16m ago)    29d
metrics-server-768f9f6999-blwjv    1/1     Running   6 (15m ago)    18d
storage-provisioner                1/1     Running   21 (15m ago)   29d

zephoryx@fedora$ kubectl -n homework-s09 apply -f 08-kubernetes-fundamentals/app.yaml
deployment.apps/web created
service/web created

zephoryx@fedora$ kubectl -n homework-s09 rollout status deployment/web
Waiting for deployment "web" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web" rollout to finish: 1 of 2 updated replicas are available...
deployment "web" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s09 get pods,deploy,rs,svc -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
pod/web-7b8558696c-58hs5   1/1     Running   0          21s   10.244.0.11   minikube   <none>           <none>
pod/web-7b8558696c-h74bn   1/1     Running   0          21s   10.244.0.10   minikube   <none>           <none>

NAME                  READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES              SELECTOR
deployment.apps/web   2/2     2            2           21s   web          nginx:1.28-alpine   app=web

NAME                             DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES              SELECTOR
replicaset.apps/web-7b8558696c   2         2         2       21s   web          nginx:1.28-alpine   app=web,pod-template-hash=7b8558696c

NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/web   ClusterIP   10.98.226.112   <none>        80/TCP    21s   app=web

zephoryx@fedora$ kubectl -n homework-s09 explain deployment.spec.replicas
GROUP:      apps
KIND:       Deployment
VERSION:    v1

FIELD: replicas <integer>

DESCRIPTION:
    Number of desired pods. This is a pointer to distinguish between explicit
    zero and not specified. Defaults to 1.

zephoryx@fedora$ kubectl -n homework-s09 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s09 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ kubectl -n homework-s09 exec client -- wget -qO- http://web
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s09 scale deployment/web --replicas=3
deployment.apps/web scaled

zephoryx@fedora$ kubectl -n homework-s09 rollout status deployment/web
Waiting for deployment "web" rollout to finish: 2 of 3 updated replicas are available...
deployment "web" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s09 set image deployment/web web=nginx:1.29-alpine
deployment.apps/web image updated

zephoryx@fedora$ kubectl -n homework-s09 rollout status deployment/web
Waiting for deployment "web" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
deployment "web" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s09 rollout history deployment/web
deployment.apps/web
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

zephoryx@fedora$ kubectl -n homework-s09 rollout undo deployment/web
Warning: resource deployments/web was previously managed with 'kubectl apply'. Rolling back will not update the kubectl.kubernetes.io/last-applied-configuration annotation, which may cause unexpected behavior on future 'kubectl apply' operations. Consider using 'kubectl apply' with your previous configuration file instead.
deployment.apps/web rolled back

zephoryx@fedora$ kubectl -n homework-s09 rollout status deployment/web
Waiting for deployment "web" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
deployment "web" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s09 get pods,deploy,rs,svc -o wide
NAME                       READY   STATUS        RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
pod/client                 1/1     Running       0          31s   10.244.0.12   minikube   <none>           <none>
pod/web-755df94d58-4cbb8   1/1     Terminating   0          24s   10.244.0.14   minikube   <none>           <none>
pod/web-7b8558696c-bgv5z   1/1     Running       0          3s    10.244.0.18   minikube   <none>           <none>
pod/web-7b8558696c-mrdzj   1/1     Running       0          4s    10.244.0.17   minikube   <none>           <none>
pod/web-7b8558696c-vkgcm   1/1     Running       0          1s    10.244.0.19   minikube   <none>           <none>

NAME                  READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES              SELECTOR
deployment.apps/web   3/3     3            3           53s   web          nginx:1.28-alpine   app=web

NAME                             DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES              SELECTOR
replicaset.apps/web-755df94d58   0         0         0       24s   web          nginx:1.29-alpine   app=web,pod-template-hash=755df94d58
replicaset.apps/web-7b8558696c   3         3         3       53s   web          nginx:1.28-alpine   app=web,pod-template-hash=7b8558696c

NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/web   ClusterIP   10.98.226.112   <none>        80/TCP    53s   app=web
```
