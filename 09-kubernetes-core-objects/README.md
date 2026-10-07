# Session 10: Pods, ReplicaSets and Deployments

**Nitish Kumar Bhambu — 24BCS10589**

| Strategy | What changes | What to check |
|---|---|---|
| Rolling update | New Pods replace old ones gradually; maxSurge=1, maxUnavailable=0 | Old/new ReplicaSets during update; rollout completion |
| Blue-green | Both versions exist; change the Service selector | Response changes from blue to green |
| Canary | Four stable Pods and one canary share a Service | Both response versions and five endpoints |
| Recreate | Old ReplicaSet scales to zero before the replacement starts | Scaling events and completed rollout |

Four stable replicas and one canary give an approximate 80:20 split. I checked both response versions; the small sample need not split exactly 80:20.

The `lifecycle/` YAML files adapt all 12 examples from the instructor's `session10-k8s-core-objects/pod-lifecycle`. Changes: current image tags and an intentionally impossible CPU request so Pending is repeatable on this laptop.

| Example | Meaning |
|---|---|
| Running | Container is running; readiness is a separate condition |
| Pending | The scheduler cannot satisfy the CPU request |
| Succeeded | One-off task exits 0 with restartPolicy Never |
| Failed | One-off task exits nonzero with restartPolicy Never |
| CrashLoopBackOff | Container repeatedly exits and restart backoff increases |
| ImagePullBackOff | Image cannot be pulled; inspect events for the actual error |
| Readiness | Determines whether Service traffic should reach the Pod |
| Liveness | Removing the health file eventually triggers a restart |
| Startup | Gives slow initialization time before other probes apply |
| Init container | Setup completes before the application starts |
| Multiple containers | App and sidecar share one Pod and network namespace |
| Termination | SIGTERM allows cleanup before the grace period expires |

`CrashLoopBackOff` and `ImagePullBackOff` are container waiting reasons shown by kubectl, not extra Pod phases. Pod phases include Pending, Running, Succeeded, Failed and Unknown. Failed exercises are deliberate; the captured `describe` output is the evidence of their causes.

```bash
kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/rolling.yaml
kubectl -n homework-s10 get pods,rs,deploy
kubectl -n homework-s10 rollout history deployment/rolling
```

Reference: [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s10
namespace/homework-s10 created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/rolling.yaml
deployment.apps/rolling created

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/rolling
Waiting for deployment "rolling" rollout to finish: 0 of 3 updated replicas are available...
Waiting for deployment "rolling" rollout to finish: 1 of 3 updated replicas are available...
Waiting for deployment "rolling" rollout to finish: 2 of 3 updated replicas are available...
deployment "rolling" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/blue.yaml
deployment.apps/blue created

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/blue
Waiting for deployment "blue" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "blue" rollout to finish: 1 of 2 updated replicas are available...
deployment "blue" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/green.yaml
deployment.apps/green created

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/green
Waiting for deployment "green" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "green" rollout to finish: 1 of 2 updated replicas are available...
deployment "green" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/stable.yaml
deployment.apps/stable created

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/stable
Waiting for deployment "stable" rollout to finish: 0 of 4 updated replicas are available...
Waiting for deployment "stable" rollout to finish: 1 of 4 updated replicas are available...
Waiting for deployment "stable" rollout to finish: 2 of 4 updated replicas are available...
Waiting for deployment "stable" rollout to finish: 3 of 4 updated replicas are available...
deployment "stable" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/canary.yaml
deployment.apps/canary created

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/canary
Waiting for deployment "canary" rollout to finish: 0 of 1 updated replicas are available...
deployment "canary" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/recreate.yaml
deployment.apps/recreate created

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/recreate
Waiting for deployment "recreate" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "recreate" rollout to finish: 1 of 2 updated replicas are available...
deployment "recreate" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/services.yaml
service/colour created
service/canary created

zephoryx@fedora$ kubectl -n homework-s10 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s10 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ kubectl -n homework-s10 exec deployment/blue -- sh -c 'printf '"'"'blue\n'"'"' > /usr/share/nginx/html/version'

zephoryx@fedora$ kubectl -n homework-s10 exec deployment/green -- sh -c 'printf '"'"'green\n'"'"' > /usr/share/nginx/html/version'

zephoryx@fedora$ kubectl -n homework-s10 exec deployment/stable -- sh -c 'printf '"'"'stable\n'"'"' > /usr/share/nginx/html/version'

zephoryx@fedora$ kubectl -n homework-s10 exec deployment/canary -- sh -c 'printf '"'"'canary\n'"'"' > /usr/share/nginx/html/version'

zephoryx@fedora$ kubectl -n homework-s10 get rs
NAME                  DESIRED   CURRENT   READY   AGE
blue-5fcb5494ff       2         2         2       11s
canary-64767d98cf     1         1         1       6s
green-557cdc875b      2         2         2       9s
recreate-5b6cd97d96   2         2         2       5s
rolling-7b8664d444    3         3         3       13s
stable-6df6768768     4         4         4       8s

zephoryx@fedora$ kubectl -n homework-s10 set image deployment/rolling web=nginx:1.29-alpine
deployment.apps/rolling image updated

zephoryx@fedora$ kubectl -n homework-s10 get pods,rs
NAME                            READY   STATUS              RESTARTS   AGE
pod/blue-5fcb5494ff-qcn5j       1/1     Running             0          12s
pod/blue-5fcb5494ff-xrm65       1/1     Running             0          12s
pod/canary-64767d98cf-ggpfz     1/1     Running             0          7s
pod/client                      1/1     Running             0          3s
pod/green-557cdc875b-6qbkr      1/1     Running             0          10s
# ... intermediate output omitted ...
replicaset.apps/blue-5fcb5494ff       2         2         2       12s
replicaset.apps/canary-64767d98cf     1         1         1       7s
replicaset.apps/green-557cdc875b      2         2         2       10s
replicaset.apps/recreate-5b6cd97d96   2         2         2       6s
replicaset.apps/rolling-7b8664d444    3         3         3       14s
replicaset.apps/rolling-8b6c77677     1         1         0       1s
replicaset.apps/stable-6df6768768     4         4         4       9s

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/rolling
Waiting for deployment "rolling" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "rolling" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "rolling" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "rolling" rollout to finish: 1 old replicas are pending termination...
deployment "rolling" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 get rs
NAME                  DESIRED   CURRENT   READY   AGE
blue-5fcb5494ff       2         2         2       15s
canary-64767d98cf     1         1         1       10s
green-557cdc875b      2         2         2       13s
recreate-5b6cd97d96   2         2         2       9s
rolling-7b8664d444    0         0         0       17s
rolling-8b6c77677     3         3         3       4s
stable-6df6768768     4         4         4       12s

zephoryx@fedora$ kubectl -n homework-s10 exec client -- wget -qO- http://colour/version
blue

zephoryx@fedora$ kubectl -n homework-s10 patch svc colour --type=merge -p '{"spec":{"selector":{"app":"colour","version":"green"}}}'
service/colour patched

zephoryx@fedora$ kubectl -n homework-s10 exec client -- wget -qO- http://colour/version
green

zephoryx@fedora$ kubectl -n homework-s10 get endpointslices -l kubernetes.io/service-name=canary -o wide
NAME           ADDRESSTYPE   PORTS   ENDPOINTS                                         AGE
canary-gdx82   IPv4          80      10.244.0.27,10.244.0.28,10.244.0.30 + 2 more...   9s

zephoryx@fedora$ kubectl -n homework-s10 exec client -- sh -c 'for i in $(seq 1 50); do wget -qO- http://canary/version; done | sort | uniq -c'
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
# ... intermediate output omitted ...
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
wget: server returned error: HTTP/1.1 404 Not Found
     11 canary
     12 stable

zephoryx@fedora$ kubectl -n homework-s10 set image deployment/recreate web=nginx:1.29-alpine
deployment.apps/recreate image updated

zephoryx@fedora$ kubectl -n homework-s10 get pods,rs
NAME                            READY   STATUS        RESTARTS   AGE
pod/blue-5fcb5494ff-qcn5j       1/1     Running       0          19s
pod/blue-5fcb5494ff-xrm65       1/1     Running       0          19s
pod/canary-64767d98cf-ggpfz     1/1     Running       0          14s
pod/client                      1/1     Running       0          10s
pod/green-557cdc875b-6qbkr      1/1     Running       0          17s
# ... intermediate output omitted ...
replicaset.apps/blue-5fcb5494ff       2         2         2       19s
replicaset.apps/canary-64767d98cf     1         1         1       14s
replicaset.apps/green-557cdc875b      2         2         2       17s
replicaset.apps/recreate-5b6cd97d96   0         0         0       13s
replicaset.apps/rolling-7b8664d444    0         0         0       21s
replicaset.apps/rolling-8b6c77677     3         3         3       8s
replicaset.apps/stable-6df6768768     4         4         4       16s

zephoryx@fedora$ kubectl -n homework-s10 rollout status deployment/recreate
Waiting for deployment "recreate" rollout to finish: 0 out of 2 new replicas have been updated...
Waiting for deployment "recreate" rollout to finish: 0 out of 2 new replicas have been updated...
Waiting for deployment "recreate" rollout to finish: 0 out of 2 new replicas have been updated...
Waiting for deployment "recreate" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "recreate" rollout to finish: 1 of 2 updated replicas are available...
deployment "recreate" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s10 get events --sort-by=.metadata.creationTimestamp
LAST SEEN   TYPE     REASON              OBJECT                           MESSAGE
23s         Normal   ScalingReplicaSet   deployment/rolling               Scaled up replica set rolling-7b8664d444 from 0 to 3
22s         Normal   Scheduled           pod/rolling-7b8664d444-79mf6     Successfully assigned homework-s10/rolling-7b8664d444-79mf6 to minikube
23s         Normal   SuccessfulCreate    replicaset/rolling-7b8664d444    Created pod: rolling-7b8664d444-79mf6
23s         Normal   SuccessfulCreate    replicaset/rolling-7b8664d444    Created pod: rolling-7b8664d444-nl7ns
22s         Normal   Scheduled           pod/rolling-7b8664d444-nl7ns     Successfully assigned homework-s10/rolling-7b8664d444-nl7ns to minikube
# ... intermediate output omitted ...
2s          Normal   SuccessfulCreate    replicaset/recreate-7889dc9c4f   Created pod: recreate-7889dc9c4f-t54tw
1s          Normal   Pulled              pod/recreate-7889dc9c4f-t54tw    Container image "nginx:1.29-alpine" already present on machine and can be accessed by the pod
1s          Normal   Started             pod/recreate-7889dc9c4f-7b6dz    Container started
1s          Normal   Created             pod/recreate-7889dc9c4f-7b6dz    Container created
1s          Normal   Pulled              pod/recreate-7889dc9c4f-7b6dz    Container image "nginx:1.29-alpine" already present on machine and can be accessed by the pod
1s          Normal   Created             pod/recreate-7889dc9c4f-t54tw    Container created
1s          Normal   Started             pod/recreate-7889dc9c4f-t54tw    Container started

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/01-running.yaml
pod/lifecycle-running created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/02-pending.yaml
pod/lifecycle-pending created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/03-succeeded.yaml
pod/lifecycle-succeeded created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/04-failed.yaml
pod/lifecycle-failed created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/05-crashloopbackoff.yaml
pod/lifecycle-crashloop created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/06-imagepullbackoff.yaml
pod/lifecycle-image-error created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/07-readiness.yaml
pod/lifecycle-readiness created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/08-liveness.yaml
pod/lifecycle-liveness created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/09-startup.yaml
pod/lifecycle-startup created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/10-init-container.yaml
pod/lifecycle-init created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/11-multi-container.yaml
pod/lifecycle-multi-container created

zephoryx@fedora$ kubectl -n homework-s10 apply -f 09-kubernetes-core-objects/lifecycle/12-termination.yaml
pod/lifecycle-termination created

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-running -o wide
NAME                READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-running   1/1     Running   0          46s   10.244.0.40   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-running
Name:             lifecycle-running
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:21:01 +0530
# ... intermediate output omitted ...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  46s   default-scheduler  Successfully assigned homework-s10/lifecycle-running to minikube
  Normal  Pulled     45s   kubelet            spec.containers{nginx}: Container image "nginx:1.28-alpine" already present on machine and can be accessed by the pod
  Normal  Created    45s   kubelet            spec.containers{nginx}: Container created
  Normal  Started    45s   kubelet            spec.containers{nginx}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-running --all-containers=true
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# ... intermediate output omitted ...
2026/10/07 12:51:02 [notice] 1#1: start worker process 35
2026/10/07 12:51:02 [notice] 1#1: start worker process 36
2026/10/07 12:51:02 [notice] 1#1: start worker process 37
2026/10/07 12:51:02 [notice] 1#1: start worker process 38
2026/10/07 12:51:02 [notice] 1#1: start worker process 39
2026/10/07 12:51:02 [notice] 1#1: start worker process 40
2026/10/07 12:51:02 [notice] 1#1: start worker process 41

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-pending -o wide
NAME                READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
lifecycle-pending   0/1     Pending   0          47s   <none>   <none>   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-pending
Name:             lifecycle-pending
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             <none>
Labels:           <none>
# ... intermediate output omitted ...
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  47s                default-scheduler  0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
  Warning  FailedScheduling  38s (x2 over 38s)  default-scheduler  0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-pending --all-containers=true

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-succeeded -o wide
NAME                  READY   STATUS      RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-succeeded   0/1     Completed   0          48s   10.244.0.41   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-succeeded
Name:             lifecycle-succeeded
Namespace:        homework-s10
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       Completed
# ... output shortened ...
  Normal  Scheduled  48s   default-scheduler  Successfully assigned homework-s10/lifecycle-succeeded to minikube
  Normal  Pulled     47s   kubelet            spec.containers{task}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal  Created    47s   kubelet            spec.containers{task}: Container created
  Normal  Started    47s   kubelet            spec.containers{task}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-succeeded --all-containers=true
Task started
Task completed successfully

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-failed -o wide
NAME               READY   STATUS   RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-failed   0/1     Error    0          48s   10.244.0.42   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-failed
Name:             lifecycle-failed
Namespace:        homework-s10
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       Error
# ... output shortened ...
  Normal  Scheduled  48s   default-scheduler  Successfully assigned homework-s10/lifecycle-failed to minikube
  Normal  Pulled     48s   kubelet            spec.containers{task}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal  Created    48s   kubelet            spec.containers{task}: Container created
  Normal  Started    47s   kubelet            spec.containers{task}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-failed --all-containers=true
Task started
Task failed

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-crashloop -o wide
NAME                  READY   STATUS   RESTARTS      AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-crashloop   0/1     Error    2 (41s ago)   49s   10.244.0.43   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-crashloop
Name:             lifecycle-crashloop
Namespace:        homework-s10
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       Error
# ... output shortened ...
      Reason:       Error
# ... output shortened ...
  Normal   Pulled     30s (x3 over 48s)  kubelet            spec.containers{crashing-app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal   Created    30s (x3 over 48s)  kubelet            spec.containers{crashing-app}: Container created
  Normal   Started    30s (x3 over 48s)  kubelet            spec.containers{crashing-app}: Container started
  Warning  BackOff    26s (x2 over 40s)  kubelet            spec.containers{crashing-app}: Back-off restarting failed container crashing-app in pod lifecycle-crashloop_homework-s10(b9d5233b-5ed6-4f78-a853-05e322a3d2fe)

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-crashloop --all-containers=true
Application started
Application crashed

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-image-error -o wide
NAME                    READY   STATUS             RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-image-error   0/1     ImagePullBackOff   0          49s   10.244.0.44   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-image-error
Name:             lifecycle-image-error
Namespace:        homework-s10
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       ImagePullBackOff
# ... output shortened ...
  Warning  Failed     20s (x2 over 47s)  kubelet            spec.containers{broken-image}: Error: ImagePullBackOff
  Normal   Pulling    5s (x3 over 49s)   kubelet            spec.containers{broken-image}: Pulling image "jakwehrgkaejw:kahsdfgkhj"
  Warning  Failed     4s (x3 over 47s)   kubelet            spec.containers{broken-image}: Failed to pull image "jakwehrgkaejw:kahsdfgkhj": failed to pull and unpack image "docker.io/library/jakwehrgkaejw:kahsdfgkhj": failed to resolve reference "docker.io/library/jakwehrgkaejw:kahsdfgkhj": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
  Warning  Failed     4s (x3 over 47s)   kubelet            spec.containers{broken-image}: Error: ErrImagePull

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-image-error --all-containers=true
Error from server (BadRequest): container "broken-image" in pod "lifecycle-image-error" is waiting to start: trying and failing to pull image
# Exit status: 1

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-readiness -o wide
NAME                  READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-readiness   1/1     Running   0          50s   10.244.0.45   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-readiness
Name:             lifecycle-readiness
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:21:04 +0530
# ... intermediate output omitted ...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  50s   default-scheduler  Successfully assigned homework-s10/lifecycle-readiness to minikube
  Normal  Pulled     49s   kubelet            spec.containers{nginx}: Container image "nginx:1.28-alpine" already present on machine and can be accessed by the pod
  Normal  Created    49s   kubelet            spec.containers{nginx}: Container created
  Normal  Started    49s   kubelet            spec.containers{nginx}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-readiness --all-containers=true
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# ... intermediate output omitted ...
10.244.0.1 - - [07/Oct/2026:12:51:21 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"
10.244.0.1 - - [07/Oct/2026:12:51:26 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"
10.244.0.1 - - [07/Oct/2026:12:51:31 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"
10.244.0.1 - - [07/Oct/2026:12:51:36 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"
10.244.0.1 - - [07/Oct/2026:12:51:41 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"
10.244.0.1 - - [07/Oct/2026:12:51:46 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"
10.244.0.1 - - [07/Oct/2026:12:51:51 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.37" "-"

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-liveness -o wide
NAME                 READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-liveness   1/1     Running   0          50s   10.244.0.46   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-liveness
Name:             lifecycle-liveness
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:21:05 +0530
# ... intermediate output omitted ...
  ----     ------     ----               ----               -------
  Normal   Scheduled  50s                default-scheduler  Successfully assigned homework-s10/lifecycle-liveness to minikube
  Normal   Pulled     50s                kubelet            spec.containers{app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal   Created    50s                kubelet            spec.containers{app}: Container created
  Normal   Started    50s                kubelet            spec.containers{app}: Container started
  Warning  Unhealthy  20s (x2 over 25s)  kubelet            spec.containers{app}: Liveness probe failed:
  Normal   Killing    20s                kubelet            spec.containers{app}: Container app failed liveness probe, will be restarted

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-liveness --all-containers=true
App started
Health file removed

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-startup -o wide
NAME                READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-startup   1/1     Running   0          51s   10.244.0.47   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-startup
Name:             lifecycle-startup
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:21:05 +0530
# ... intermediate output omitted ...
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  51s                default-scheduler  Successfully assigned homework-s10/lifecycle-startup to minikube
  Normal   Pulled     50s                kubelet            spec.containers{slow-app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal   Created    50s                kubelet            spec.containers{slow-app}: Container created
  Normal   Started    50s                kubelet            spec.containers{slow-app}: Container started
  Warning  Unhealthy  21s (x6 over 46s)  kubelet            spec.containers{slow-app}: Startup probe failed:

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-startup --all-containers=true
Application starting...
Application started

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-init -o wide
NAME             READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-init   1/1     Running   0          52s   10.244.0.48   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-init
Name:             lifecycle-init
Namespace:        homework-s10
Priority:         0
Service Account:  default
# ... output shortened ...
      Reason:       Completed
# ... output shortened ...
  Normal  Started    51s   kubelet            spec.initContainers{setup}: Container started
  Normal  Pulled     40s   kubelet            spec.containers{app}: Container image "nginx:1.28-alpine" already present on machine and can be accessed by the pod
  Normal  Created    40s   kubelet            spec.containers{app}: Container created
  Normal  Started    40s   kubelet            spec.containers{app}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-init --all-containers=true
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# ... intermediate output omitted ...
2026/10/07 12:51:17 [notice] 1#1: start worker process 38
2026/10/07 12:51:17 [notice] 1#1: start worker process 39
2026/10/07 12:51:17 [notice] 1#1: start worker process 40
2026/10/07 12:51:17 [notice] 1#1: start worker process 41
2026/10/07 12:51:17 [notice] 1#1: start worker process 42
Init container running
Init complete

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-multi-container -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-multi-container   2/2     Running   0          52s   10.244.0.49   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-multi-container
Name:             lifecycle-multi-container
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:21:06 +0530
# ... intermediate output omitted ...
  Normal  Scheduled  52s   default-scheduler  Successfully assigned homework-s10/lifecycle-multi-container to minikube
  Normal  Pulled     51s   kubelet            spec.containers{app}: Container image "nginx:1.28-alpine" already present on machine and can be accessed by the pod
  Normal  Created    51s   kubelet            spec.containers{app}: Container created
  Normal  Started    51s   kubelet            spec.containers{app}: Container started
  Normal  Pulled     51s   kubelet            spec.containers{sidecar}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal  Created    51s   kubelet            spec.containers{sidecar}: Container created
  Normal  Started    51s   kubelet            spec.containers{sidecar}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-multi-container --all-containers=true
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# ... intermediate output omitted ...
2026/10/07 12:51:07 [notice] 1#1: start worker process 41
Sidecar is running
Sidecar is running
Sidecar is running
Sidecar is running
Sidecar is running
Sidecar is running

zephoryx@fedora$ kubectl -n homework-s10 get pod lifecycle-termination -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
lifecycle-termination   1/1     Running   0          53s   10.244.0.50   minikube   <none>           <none>

zephoryx@fedora$ kubectl -n homework-s10 describe pod lifecycle-termination
Name:             lifecycle-termination
Namespace:        homework-s10
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 07 Oct 2026 18:21:06 +0530
# ... intermediate output omitted ...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  52s   default-scheduler  Successfully assigned homework-s10/lifecycle-termination to minikube
  Normal  Pulled     52s   kubelet            spec.containers{graceful-app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal  Created    52s   kubelet            spec.containers{graceful-app}: Container created
  Normal  Started    52s   kubelet            spec.containers{graceful-app}: Container started

zephoryx@fedora$ kubectl -n homework-s10 logs lifecycle-termination --all-containers=true
Application running

zephoryx@fedora$ kubectl -n homework-s10 delete pod lifecycle-termination --wait=true
pod "lifecycle-termination" deleted from homework-s10 namespace

zephoryx@fedora$ kubectl -n homework-s10 get pods,deploy,rs,svc -o wide
NAME                            READY   STATUS             RESTARTS      AGE   IP            NODE       NOMINATED NODE   READINESS GATES
pod/blue-5fcb5494ff-qcn5j       1/1     Running            0             93s   10.244.0.24   minikube   <none>           <none>
pod/blue-5fcb5494ff-xrm65       1/1     Running            0             93s   10.244.0.23   minikube   <none>           <none>
pod/canary-64767d98cf-ggpfz     1/1     Running            0             88s   10.244.0.31   minikube   <none>           <none>
pod/client                      1/1     Running            0             84s   10.244.0.34   minikube   <none>           <none>
pod/green-557cdc875b-6qbkr      1/1     Running            0             91s   10.244.0.25   minikube   <none>           <none>
# ... intermediate output omitted ...
replicaset.apps/rolling-7b8664d444    0         0         0       95s   web          nginx:1.28-alpine   app=rolling,pod-template-hash=7b8664d444
replicaset.apps/rolling-8b6c77677     3         3         3       82s   web          nginx:1.29-alpine   app=rolling,pod-template-hash=8b6c77677
replicaset.apps/stable-6df6768768     4         4         4       90s   web          nginx:1.28-alpine   app=canary,pod-template-hash=6df6768768,version=stable

NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/canary   ClusterIP   10.96.225.229    <none>        80/TCP    85s   app=canary
service/colour   ClusterIP   10.111.166.139   <none>        80/TCP    85s   app=colour,version=green
```
