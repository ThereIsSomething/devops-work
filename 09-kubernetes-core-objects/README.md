# Session 10: Pods, ReplicaSets and Deployments

**Nitish Kumar Bhambu — 24BCS10589**

| Strategy | What changes | What to check |
|---|---|---|
| Rolling update | New Pods replace old ones gradually; maxSurge=1, maxUnavailable=0 | Old/new ReplicaSets during update; rollout completion |
| Blue-green | Both versions exist; change the Service selector | Response changes from blue to green |
| Canary | Four stable Pods and one canary share a Service | Both response versions and five endpoints |
| Recreate | Old ReplicaSet scales to zero before the replacement starts | Scaling events and completed rollout |

A 4:1 replica split gives an approximate 20% canary share when ready endpoints are equally selected. It does not guarantee exactly 20% of 50 requests. Persistent connections and sampling affect observed distribution. This exercise opens separate requests and records the observed counts. For strict weights, use a controller or service mesh with traffic weighting.

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
python3 scripts/run_kubernetes_labs.py 10
```

Reference: [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/).

## Execution evidence

Actual local transcripts are included below after the runs finish. A missing or incomplete transcript is not a completed exercise.

<!-- EVIDENCE -->

### run.txt

[Complete transcript](outputs/run.txt)

````text
Captured 2026-10-07T12:50:38.338658+00:00
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' create namespace homework-s10
namespace/homework-s10 created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/rolling.yaml
deployment.apps/rolling created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 rollout status deployment/rolling --timeout=180s
Waiting for deployment "rolling" rollout to finish: 0 of 3 updated replicas are available...
Waiting for deployment "rolling" rollout to finish: 1 of 3 updated replicas are available...
Waiting for deployment "rolling" rollout to finish: 2 of 3 updated replicas are available...
deployment "rolling" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/blue.yaml
deployment.apps/blue created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 rollout status deployment/blue --timeout=180s
Waiting for deployment "blue" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "blue" rollout to finish: 1 of 2 updated replicas are available...
deployment "blue" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/green.yaml
deployment.apps/green created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 rollout status deployment/green --timeout=180s
Waiting for deployment "green" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "green" rollout to finish: 1 of 2 updated replicas are available...
deployment "green" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/stable.yaml
deployment.apps/stable created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 rollout status deployment/stable --timeout=180s
Waiting for deployment "stable" rollout to finish: 0 of 4 updated replicas are available...
Waiting for deployment "stable" rollout to finish: 1 of 4 updated replicas are available...
Waiting for deployment "stable" rollout to finish: 2 of 4 updated replicas are available...
Waiting for deployment "stable" rollout to finish: 3 of 4 updated replicas are available...
deployment "stable" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/canary.yaml
deployment.apps/canary created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 rollout status deployment/canary --timeout=180s
Waiting for deployment "canary" rollout to finish: 0 of 1 updated replicas are available...
deployment "canary" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/recreate.yaml
deployment.apps/recreate created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 rollout status deployment/recreate --timeout=180s
Waiting for deployment "recreate" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "recreate" rollout to finish: 1 of 2 updated replicas are available...
deployment "recreate" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 apply -f 09-kubernetes-core-objects/services.yaml
service/colour created
service/canary created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 wait --for=condition=Ready pod/client --timeout=120s
pod/client condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 exec deployment/blue -- sh -c 'printf '"'"'blue\n'"'"' > /usr/share/nginx/html/version'

[Excerpt: 1222 intermediate lines omitted; complete transcript linked above.]

  Ready                       True 
  ContainersReady             True 
  PodScheduled                True 
Volumes:
  kube-api-access-cxcn4:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  52s   default-scheduler  Successfully assigned homework-s10/lifecycle-termination to minikube
  Normal  Pulled     52s   kubelet            spec.containers{graceful-app}: Container image "busybox:1.37" already present on machine and can be accessed by the pod
  Normal  Created    52s   kubelet            spec.containers{graceful-app}: Container created
  Normal  Started    52s   kubelet            spec.containers{graceful-app}: Container started
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 logs lifecycle-termination --all-containers=true
Application running
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 delete pod lifecycle-termination --wait=true
pod "lifecycle-termination" deleted from homework-s10 namespace
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s10 get pods,deploy,rs,svc -o wide
NAME                            READY   STATUS             RESTARTS      AGE   IP            NODE       NOMINATED NODE   READINESS GATES
pod/blue-5fcb5494ff-qcn5j       1/1     Running            0             93s   10.244.0.24   minikube   <none>           <none>
pod/blue-5fcb5494ff-xrm65       1/1     Running            0             93s   10.244.0.23   minikube   <none>           <none>
pod/canary-64767d98cf-ggpfz     1/1     Running            0             88s   10.244.0.31   minikube   <none>           <none>
pod/client                      1/1     Running            0             84s   10.244.0.34   minikube   <none>           <none>
pod/green-557cdc875b-6qbkr      1/1     Running            0             91s   10.244.0.25   minikube   <none>           <none>
pod/green-557cdc875b-wkj8b      1/1     Running            0             91s   10.244.0.26   minikube   <none>           <none>
pod/lifecycle-crashloop         0/1     Error              3 (48s ago)   70s   10.244.0.43   minikube   <none>           <none>
pod/lifecycle-failed            0/1     Error              0             70s   10.244.0.42   minikube   <none>           <none>
pod/lifecycle-image-error       0/1     ImagePullBackOff   0             69s   10.244.0.44   minikube   <none>           <none>
pod/lifecycle-init              1/1     Running            0             68s   10.244.0.48   minikube   <none>           <none>
pod/lifecycle-liveness          1/1     Running            1 (8s ago)    68s   10.244.0.46   minikube   <none>           <none>
pod/lifecycle-multi-container   2/2     Running            0             67s   10.244.0.49   minikube   <none>           <none>
pod/lifecycle-pending           0/1     Pending            0             71s   <none>        <none>     <none>           <none>
pod/lifecycle-readiness         1/1     Running            0             69s   10.244.0.45   minikube   <none>           <none>
pod/lifecycle-running           1/1     Running            0             72s   10.244.0.40   minikube   <none>           <none>
pod/lifecycle-startup           1/1     Running            0             68s   10.244.0.47   minikube   <none>           <none>
pod/lifecycle-succeeded         0/1     Completed          0             71s   10.244.0.41   minikube   <none>           <none>
pod/recreate-7889dc9c4f-7b6dz   1/1     Running            0             74s   10.244.0.38   minikube   <none>           <none>
pod/recreate-7889dc9c4f-t54tw   1/1     Running            0             74s   10.244.0.39   minikube   <none>           <none>
pod/rolling-8b6c77677-h2gbg     1/1     Running            0             79s   10.244.0.37   minikube   <none>           <none>
pod/rolling-8b6c77677-t2bsw     1/1     Running            0             80s   10.244.0.36   minikube   <none>           <none>
pod/rolling-8b6c77677-zltv5     1/1     Running            0             82s   10.244.0.35   minikube   <none>           <none>
pod/stable-6df6768768-2bzf7     1/1     Running            0             90s   10.244.0.29   minikube   <none>           <none>
pod/stable-6df6768768-h6g8n     1/1     Running            0             90s   10.244.0.30   minikube   <none>           <none>
pod/stable-6df6768768-qmwk4     1/1     Running            0             90s   10.244.0.28   minikube   <none>           <none>
pod/stable-6df6768768-tvrtq     1/1     Running            0             90s   10.244.0.27   minikube   <none>           <none>

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES              SELECTOR
deployment.apps/blue       2/2     2            2           93s   web          nginx:1.28-alpine   app=colour,version=blue
deployment.apps/canary     1/1     1            1           88s   web          nginx:1.28-alpine   app=canary,version=canary
deployment.apps/green      2/2     2            2           91s   web          nginx:1.28-alpine   app=colour,version=green
deployment.apps/recreate   2/2     2            2           87s   web          nginx:1.29-alpine   app=recreate
deployment.apps/rolling    3/3     3            3           95s   web          nginx:1.29-alpine   app=rolling
deployment.apps/stable     4/4     4            4           90s   web          nginx:1.28-alpine   app=canary,version=stable

NAME                                  DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES              SELECTOR
replicaset.apps/blue-5fcb5494ff       2         2         2       93s   web          nginx:1.28-alpine   app=colour,pod-template-hash=5fcb5494ff,version=blue
replicaset.apps/canary-64767d98cf     1         1         1       88s   web          nginx:1.28-alpine   app=canary,pod-template-hash=64767d98cf,version=canary
replicaset.apps/green-557cdc875b      2         2         2       91s   web          nginx:1.28-alpine   app=colour,pod-template-hash=557cdc875b,version=green
replicaset.apps/recreate-5b6cd97d96   0         0         0       87s   web          nginx:1.28-alpine   app=recreate,pod-template-hash=5b6cd97d96
replicaset.apps/recreate-7889dc9c4f   2         2         2       74s   web          nginx:1.29-alpine   app=recreate,pod-template-hash=7889dc9c4f
replicaset.apps/rolling-7b8664d444    0         0         0       95s   web          nginx:1.28-alpine   app=rolling,pod-template-hash=7b8664d444
replicaset.apps/rolling-8b6c77677     3         3         3       82s   web          nginx:1.29-alpine   app=rolling,pod-template-hash=8b6c77677
replicaset.apps/stable-6df6768768     4         4         4       90s   web          nginx:1.28-alpine   app=canary,pod-template-hash=6df6768768,version=stable

NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/canary   ClusterIP   10.96.225.229    <none>        80/TCP    85s   app=canary
service/colour   ClusterIP   10.111.166.139   <none>        80/TCP    85s   app=colour,version=green
[exit 0]
LAB EXECUTION FINISHED
````
