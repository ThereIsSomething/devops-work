# Session 14: Kubernetes Troubleshooting

**Nitish Kumar Bhambu — 24BCS10589**

I start with the observed state, then check details/events, logs, selectors and connectivity before changing anything. `get` is a summary; `describe` includes conditions and events. `logs --previous` helps when a container has restarted. `exec` is useful when the container is actually running. `events`, `explain`, `top` and `get -o wide` answer different questions and are included in the transcript.

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

This implements the instructor's troubleshooting mini project with a working Nginx Deployment/Service, an invalid image, and a deliberate selector mismatch. The actual status/error and commands used appear below rather than being copied from expected output.

```bash
python3 scripts/run_kubernetes_labs.py 14
```

Reference: [Debug applications](https://kubernetes.io/docs/tasks/debug/debug-application/).

## Execution evidence

Actual local transcripts are included below after the runs finish. A missing or incomplete transcript is not a completed exercise.

<!-- EVIDENCE -->

### run.txt

[Complete transcript](outputs/run.txt)

````text
Captured 2026-10-07T12:57:01.383554+00:00
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' create namespace homework-s14
namespace/homework-s14 created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/app.yaml
deployment.apps/troubleshooting-app created
service/troubleshooting-service created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 rollout status deployment/troubleshooting-app --timeout=180s
Waiting for deployment "troubleshooting-app" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "troubleshooting-app" rollout to finish: 1 of 2 updated replicas are available...
deployment "troubleshooting-app" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 wait --for=condition=Ready pod/client --timeout=120s
pod/client condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/crash.yaml
pod/crash created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/image.yaml
pod/image created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/pending.yaml
pod/pending created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/creating.yaml
pod/creating created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/config.yaml
pod/config created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 apply -f 13-kubernetes-troubleshooting/dns.yaml
pod/dns created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 get pods -o wide
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
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 events
LAST SEEN           TYPE      REASON              OBJECT                                     MESSAGE
40s                 Normal    SuccessfulCreate    ReplicaSet/troubleshooting-app-98786d457   Created pod: troubleshooting-app-98786d457-l9d92
40s                 Normal    SuccessfulCreate    ReplicaSet/troubleshooting-app-98786d457   Created pod: troubleshooting-app-98786d457-bmkvt
40s                 Normal    ScalingReplicaSet   Deployment/troubleshooting-app             Scaled up replica set troubleshooting-app-98786d457 from 0 to 2
40s                 Normal    Scheduled           Pod/troubleshooting-app-98786d457-bmkvt    Successfully assigned homework-s14/troubleshooting-app-98786d457-bmkvt to minikube
40s                 Normal    Scheduled           Pod/troubleshooting-app-98786d457-l9d92    Successfully assigned homework-s14/troubleshooting-app-98786d457-l9d92 to minikube
39s                 Normal    Started             Pod/troubleshooting-app-98786d457-l9d92    Container started
39s                 Normal    Created             Pod/troubleshooting-app-98786d457-l9d92    Container created
39s                 Normal    Pulled              Pod/troubleshooting-app-98786d457-l9d92    Container image "nginx:1.28-alpine" already present on machine and can be accessed by the pod
39s                 Normal    Started             Pod/troubleshooting-app-98786d457-bmkvt    Container started
39s                 Normal    Created             Pod/troubleshooting-app-98786d457-bmkvt    Container created
39s                 Normal    Pulled              Pod/troubleshooting-app-98786d457-bmkvt    Container image "nginx:1.28-alpine" already present on machine and can be accessed by the pod
38s                 Normal    Started             Pod/client                                 Container started
38s                 Normal    Created             Pod/client                                 Container created
38s                 Normal    Pulled              Pod/client                                 Container image "busybox:1.37" already present on machine and can be accessed by the pod

[Excerpt: 665 intermediate lines omitted; complete transcript linked above.]

[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 run image --image=busybox:1.37 --restart=Never -- sleep 3600
pod/image created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 wait --for=condition=Ready pod/image --timeout=120s
pod/image condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 delete pod pending
pod "pending" deleted from homework-s14 namespace
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 run pending --image=busybox:1.37 --restart=Never -- sleep 3600
pod/pending created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 wait --for=condition=Ready pod/pending --timeout=120s
pod/pending condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 delete pod dns
pod "dns" deleted from homework-s14 namespace
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 run dns --image=busybox:1.37 --restart=Never -- sleep 3600
pod/dns created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 wait --for=condition=Ready pod/dns --timeout=120s
pod/dns condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 exec dns -- nslookup kubernetes.default.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10:53


Name:	kubernetes.default.svc.cluster.local
Address: 10.96.0.1
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 exec client -- wget -qO- http://troubleshooting-service
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
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s14 get pods,deploy,rs,svc -o wide
NAME                                      READY   STATUS    RESTARTS   AGE    IP            NODE       NOMINATED NODE   READINESS GATES
pod/client                                1/1     Running   0          107s   10.244.0.68   minikube   <none>           <none>
pod/config                                1/1     Running   0          105s   10.244.0.71   minikube   <none>           <none>
pod/crash                                 1/1     Running   0          38s    10.244.0.74   minikube   <none>           <none>
pod/creating                              1/1     Running   0          105s   10.244.0.73   minikube   <none>           <none>
pod/dns                                   1/1     Running   0          1s     10.244.0.77   minikube   <none>           <none>
pod/image                                 1/1     Running   0          36s    10.244.0.75   minikube   <none>           <none>
pod/pending                               1/1     Running   0          35s    10.244.0.76   minikube   <none>           <none>
pod/troubleshooting-app-98786d457-bmkvt   1/1     Running   0          109s   10.244.0.66   minikube   <none>           <none>
pod/troubleshooting-app-98786d457-l9d92   1/1     Running   0          109s   10.244.0.67   minikube   <none>           <none>

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS   IMAGES              SELECTOR
deployment.apps/troubleshooting-app   2/2     2            2           109s   web          nginx:1.28-alpine   app=troubleshooting-app

NAME                                            DESIRED   CURRENT   READY   AGE    CONTAINERS   IMAGES              SELECTOR
replicaset.apps/troubleshooting-app-98786d457   2         2         2       109s   web          nginx:1.28-alpine   app=troubleshooting-app,pod-template-hash=98786d457

NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE    SELECTOR
service/troubleshooting-service   ClusterIP   10.104.45.187   <none>        80/TCP    109s   app=troubleshooting-app
[exit 0]
LAB EXECUTION FINISHED
````
