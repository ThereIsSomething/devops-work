# Session 14: Kubernetes Troubleshooting

**Nitish Kumar Bhambu — 24BCS10589**

I start with the observed state, then check details/events, logs, selectors and connectivity before changing anything. `get` is a summary; `describe` includes conditions and events. `logs --previous` helps when a container has restarted. `exec` is useful when the container is actually running. `events`, `explain`, `top` and `get -o wide` answer different questions and are included in the command blocks.

| Problem | Investigation and root cause | Fix and verification |
|---|---|---|
| CrashLoopBackOff | Previous logs show deliberate-failure; command exits 1 | Replace immutable standalone Pod with long-running command; Ready |
| ErrImagePull / ImagePullBackOff | Events show nonexistent nginx tag | Replace with valid busybox image; Ready |
| Pending | FailedScheduling; CPU request is impossible | Replace with feasible request; Ready |
| ContainerCreating | FailedMount; referenced Secret does not exist | Create missing Secret; Ready |
| Configuration | CreateContainerConfigError; missing ConfigMap | Create missing ConfigMap; Ready |
| Service connectivity | Empty endpoint addresses; selector says wrong-app | Restore selector matching Pod labels; HTTP succeeds |
| DNS | Pod uses unreachable DNS server 192.0.2.1 | Replace with normal cluster DNS; nslookup succeeds |
| Pod networking | Compare direct Pod-IP HTTP with Service HTTP to isolate discovery/routing | Recorded separately with target-port failure in the final challenge |

ContainerCreating is not automatically an error; it is also normal while pulling images or setting up volumes. ErrImagePull and ImagePullBackOff may be successive observations of the same pull failure. Kubernetes DNS resolves Service names through CoreDNS. A selector mismatch causes missing endpoints even while application Pods are healthy.

The mini project uses Nginx, a deliberately invalid image and a wrong Service selector. The table above records each fix.

```bash
kubectl -n homework-s14 get pods -o wide
kubectl -n homework-s14 describe pod crash
kubectl -n homework-s14 logs crash --previous
kubectl -n homework-s14 get events
```

Reference: [Debug applications](https://kubernetes.io/docs/tasks/debug/debug-application/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s14
namespace/homework-s14 created

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/app.yaml
deployment.apps/troubleshooting-app created
service/troubleshooting-service created

zephoryx@fedora$ kubectl -n homework-s14 rollout status deployment/troubleshooting-app
Waiting for deployment "troubleshooting-app" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "troubleshooting-app" rollout to finish: 1 of 2 updated replicas are available...
deployment "troubleshooting-app" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s14 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s14 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/crash.yaml
pod/crash created

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/image.yaml
pod/image created

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/pending.yaml
pod/pending created

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/creating.yaml
pod/creating created

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/config.yaml
pod/config created

zephoryx@fedora$ kubectl -n homework-s14 apply -f 13-kubernetes-troubleshooting/dns.yaml
pod/dns created

zephoryx@fedora$ kubectl -n homework-s14 get pods -o wide
NAME                                  READY   STATUS                       RESTARTS      AGE   IP            NODE       NOMINATED NODE   READINESS GATES
client                                1/1     Running                      0             38s   10.244.0.68   minikube   <none>           <none>
config                                0/1     CreateContainerConfigError   0             36s   10.244.0.71   minikube   <none>           <none>
crash                                 1/1     Running                      3 (22s ago)   37s   10.244.0.69   minikube   <none>           <none>
creating                              0/1     ContainerCreating            0             36s   <none>        minikube   <none>           <none>
dns                                   1/1     Running                      0             35s   10.244.0.72   minikube   <none>           <none>
image                                 0/1     ErrImagePull                 0             37s   10.244.0.70   minikube   <none>           <none>
pending                               0/1     Pending                      0             36s   <none>        <none>     <none>           <none>
troubleshooting-app-98786d457-bmkvt   1/1     Running                      0             40s   10.244.0.66   minikube   <none>           <none>
troubleshooting-app-98786d457-l9d92   1/1     Running                      0             40s   10.244.0.67   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s14 events
LAST SEEN           TYPE      REASON              OBJECT                                     MESSAGE
40s                 Normal    SuccessfulCreate    ReplicaSet/troubleshooting-app-98786d457   Created pod: troubleshooting-app-98786d457-l9d92
40s                 Normal    SuccessfulCreate    ReplicaSet/troubleshooting-app-98786d457   Created pod: troubleshooting-app-98786d457-bmkvt
40s                 Normal    ScalingReplicaSet   Deployment/troubleshooting-app             Scaled up replica set troubleshooting-app-98786d457 from 0 to 2
# ... output shortened ...
36s                 Warning   FailedScheduling    Pod/pending                                0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
# ... output shortened ...
19s (x2 over 35s)   Warning   Failed              Pod/image                                  Error: ErrImagePull
# ... output shortened ...
7s (x4 over 35s)    Warning   Failed              Pod/config                                 Error: configmap "missing-config" not found
# ... output shortened ...
4s (x7 over 36s)    Warning   FailedMount         Pod/creating                               MountVolume.SetUp failed for volume "missing" : secret "missing-volume" not found
3s (x2 over 34s)    Warning   Failed              Pod/image                                  Error: ImagePullBackOff
3s (x2 over 34s)    Normal    BackOff             Pod/image                                  Back-off pulling image "nginx:homework-does-not-exist"
0s (x4 over 36s)    Normal    Started             Pod/crash                                  Container started
0s (x4 over 37s)    Normal    Created             Pod/crash                                  Container created
0s (x4 over 37s)    Normal    Pulled              Pod/crash                                  Container image "busybox:1.37" already present on machine and can be accessed by the pod

zephoryx@fedora$ kubectl -n homework-s14 explain pod.spec.containers
KIND:       Pod
VERSION:    v1

FIELD: containers <[]Container>

DESCRIPTION:
# ... intermediate output omitted ...
  volumeMounts	<[]VolumeMount>
    Pod volumes to mount into the container's filesystem. Cannot be updated.

  workingDir	<string>
    Container's working directory. If not specified, the container runtime's
    default will be used, which might be configured in the container image.
    Cannot be updated.

zephoryx@fedora$ kubectl -n homework-s14 top pods
error: metrics not available yet
# Exit status: 1

zephoryx@fedora$ kubectl -n homework-s14 describe pod crash
Name:             crash
Namespace:        homework-s14
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       Error
# ... output shortened ...
      Reason:       Error
# ... output shortened ...
  Normal   Pulled     1s (x4 over 38s)  kubelet            spec.containers{app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal   Created    1s (x4 over 38s)  kubelet            spec.containers{app}: Container created
  Normal   Started    1s (x4 over 37s)  kubelet            spec.containers{app}: Container started
  Warning  BackOff    0s (x3 over 36s)  kubelet            spec.containers{app}: Back-off restarting failed container app in pod crash_homework-s14(a3382af5-cd81-49d6-a8c5-a15fe1f6c533)

zephoryx@fedora$ kubectl -n homework-s14 describe pod image
Name:             image
Namespace:        homework-s14
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       ErrImagePull
# ... output shortened ...
  Warning  Failed     20s (x2 over 36s)  kubelet            spec.containers{app}: Failed to pull image "nginx:homework-does-not-exist": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/library/nginx:homework-does-not-exist": failed to resolve reference "docker.io/library/nginx:homework-does-not-exist": docker.io/library/nginx:homework-does-not-exist: not found
  Warning  Failed     20s (x2 over 36s)  kubelet            spec.containers{app}: Error: ErrImagePull
  Normal   BackOff    4s (x2 over 35s)   kubelet            spec.containers{app}: Back-off pulling image "nginx:homework-does-not-exist"
  Warning  Failed     4s (x2 over 35s)   kubelet            spec.containers{app}: Error: ImagePullBackOff

zephoryx@fedora$ kubectl -n homework-s14 describe pod pending
Name:             pending
Namespace:        homework-s14
Priority:         0
Service Account:  default
Node:             <none>
Labels:           <none>
# ... intermediate output omitted ...
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  38s   default-scheduler  0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.

zephoryx@fedora$ kubectl -n homework-s14 describe pod creating
Name:             creating
Namespace:        homework-s14
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       ContainerCreating
# ... output shortened ...
  Type     Reason       Age               From               Message
  ----     ------       ----              ----               -------
  Normal   Scheduled    38s               default-scheduler  Successfully assigned homework-s14/creating to minikube
  Warning  FailedMount  6s (x7 over 38s)  kubelet            MountVolume.SetUp failed for volume "missing" : secret "missing-volume" not found

zephoryx@fedora$ kubectl -n homework-s14 describe pod config
Name:             config
Namespace:        homework-s14
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       CreateContainerConfigError
# ... output shortened ...
  ----     ------     ----              ----               -------
  Normal   Scheduled  37s               default-scheduler  Successfully assigned homework-s14/config to minikube
  Normal   Pulled     9s (x4 over 37s)  kubelet            spec.containers{app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Warning  Failed     9s (x4 over 37s)  kubelet            spec.containers{app}: Error: configmap "missing-config" not found

zephoryx@fedora$ kubectl -n homework-s14 describe pod dns
Name:             dns
Namespace:        homework-s14
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:27:07 +0530
# ... intermediate output omitted ...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  37s   default-scheduler  Successfully assigned homework-s14/dns to minikube
  Normal  Pulled     37s   kubelet            spec.containers{app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal  Created    37s   kubelet            spec.containers{app}: Container created
  Normal  Started    37s   kubelet            spec.containers{app}: Container started

zephoryx@fedora$ kubectl -n homework-s14 logs crash --previous
unable to retrieve container logs for containerd://4a34ac61628d35caa091d6ab41fad7419c51e19fa921d7f9a07de5d000a3a8fc

zephoryx@fedora$ kubectl -n homework-s14 exec dns -- nslookup kubernetes.default.svc.cluster.local
;; connection timed out; no servers could be reached

command terminated with exit code 1
# Exit status: 1

zephoryx@fedora$ kubectl -n homework-s14 patch svc troubleshooting-service --type=merge -p '{"spec":{"selector":{"app":"wrong-app"}}}'
service/troubleshooting-service patched

zephoryx@fedora$ kubectl -n homework-s14 get endpointslices -l kubernetes.io/service-name=troubleshooting-service -o yaml
apiVersion: v1
items:
- addressType: IPv4
  apiVersion: discovery.k8s.io/v1
  endpoints: null
  kind: EndpointSlice
# ... intermediate output omitted ...
      uid: 78446f9a-ca66-401e-b385-e16ba941463f
    resourceVersion: "346355"
    uid: cf5df864-8c6e-4972-bf38-3a03fcb0b22e
  ports: null
kind: List
metadata:
  resourceVersion: ""

zephoryx@fedora$ kubectl -n homework-s14 get pods --show-labels
NAME                                  READY   STATUS                       RESTARTS      AGE   LABELS
client                                1/1     Running                      0             47s   run=client
config                                0/1     CreateContainerConfigError   0             45s   <none>
crash                                 0/1     Error                        3 (31s ago)   46s   <none>
creating                              0/1     ContainerCreating            0             45s   <none>
dns                                   1/1     Running                      0             44s   <none>
image                                 0/1     ImagePullBackOff             0             46s   <none>
pending                               0/1     Pending                      0             45s   <none>
troubleshooting-app-98786d457-bmkvt   1/1     Running                      0             49s   app=troubleshooting-app,pod-template-hash=98786d457
troubleshooting-app-98786d457-l9d92   1/1     Running                      0             49s   app=troubleshooting-app,pod-template-hash=98786d457

zephoryx@fedora$ kubectl -n homework-s14 patch svc troubleshooting-service --type=merge -p '{"spec":{"selector":{"app":"troubleshooting-app"}}}'
service/troubleshooting-service patched

zephoryx@fedora$ kubectl -n homework-s14 exec client -- wget -qO- http://troubleshooting-service
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s14 create secret generic missing-volume --from-literal=demo=public-dummy
secret/missing-volume created

zephoryx@fedora$ kubectl -n homework-s14 create configmap missing-config --from-literal=MODE=fixed
configmap/missing-config created

zephoryx@fedora$ kubectl -n homework-s14 wait --for=condition=Ready pod/creating pod/config
pod/creating condition met
pod/config condition met

zephoryx@fedora$ kubectl -n homework-s14 delete pod crash
pod "crash" deleted from homework-s14 namespace

zephoryx@fedora$ kubectl -n homework-s14 run crash --image=busybox:1.37 --restart=Never -- sleep 3600
pod/crash created

zephoryx@fedora$ kubectl -n homework-s14 wait --for=condition=Ready pod/crash
pod/crash condition met

zephoryx@fedora$ kubectl -n homework-s14 delete pod image
pod "image" deleted from homework-s14 namespace

zephoryx@fedora$ kubectl -n homework-s14 run image --image=busybox:1.37 --restart=Never -- sleep 3600
pod/image created

zephoryx@fedora$ kubectl -n homework-s14 wait --for=condition=Ready pod/image
pod/image condition met

zephoryx@fedora$ kubectl -n homework-s14 delete pod pending
pod "pending" deleted from homework-s14 namespace

zephoryx@fedora$ kubectl -n homework-s14 run pending --image=busybox:1.37 --restart=Never -- sleep 3600
pod/pending created

zephoryx@fedora$ kubectl -n homework-s14 wait --for=condition=Ready pod/pending
pod/pending condition met

zephoryx@fedora$ kubectl -n homework-s14 delete pod dns
pod "dns" deleted from homework-s14 namespace

zephoryx@fedora$ kubectl -n homework-s14 run dns --image=busybox:1.37 --restart=Never -- sleep 3600
pod/dns created

zephoryx@fedora$ kubectl -n homework-s14 wait --for=condition=Ready pod/dns
pod/dns condition met

zephoryx@fedora$ kubectl -n homework-s14 exec dns -- nslookup kubernetes.default.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10:53

Name:	kubernetes.default.svc.cluster.local
Address: 10.96.0.1

zephoryx@fedora$ kubectl -n homework-s14 exec client -- wget -qO- http://troubleshooting-service
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s14 get pods,deploy,rs,svc -o wide
NAME                                      READY   STATUS    RESTARTS   AGE    IP            NODE       NOMINATED NODE   READINESS GATES
pod/client                                1/1     Running   0          107s   10.244.0.68   minikube   <none>           <none>
pod/config                                1/1     Running   0          105s   10.244.0.71   minikube   <none>           <none>
pod/crash                                 1/1     Running   0          38s    10.244.0.74   minikube   <none>           <none>
# ... output shortened ...
NAME                                            DESIRED   CURRENT   READY   AGE    CONTAINERS   IMAGES              SELECTOR
replicaset.apps/troubleshooting-app-98786d457   2         2         2       109s   web          nginx:1.28-alpine   app=troubleshooting-app,pod-template-hash=98786d457

NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE    SELECTOR
service/troubleshooting-service   ClusterIP   10.104.45.187   <none>        80/TCP    109s   app=troubleshooting-app
```
