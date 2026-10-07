# Session 13: Storage, HPA and Probes

**Nitish Kumar Bhambu — 24BCS10589**

The mini project adapts the instructor's web-app exercise: two Nginx replicas, a 500Mi PVC, a Service, startup/readiness/liveness probes and an HPA with a 50% CPU target and a maximum of five replicas. On this single-node Minikube cluster, both replicas can mount the ReadWriteOnce claim. That design is not a general solution for replicas spread across nodes; use appropriate per-replica or shared storage in a multi-node application.

The persistence check writes a marker to `/data/student.txt`, deletes one Pod, waits for its replacement, and reads the same marker. `/scratch` uses emptyDir and is local to each Pod. The run includes a busybox HTTP load generator plus bounded CPU work in the Nginx containers to make CPU scaling observable. The extra CPU load is an explicit lab instrument, not a claim that HTTP traffic alone caused the recorded CPU level.

HPA needs the metrics API and CPU requests on containers. The calculation is approximately `ceil(current replicas × current utilization / target utilization)`, with readiness checks, tolerance, missing metrics and stabilization affecting the result. The scale-down window is shortened to 30 seconds for this lab.

| Probe | Failure consequence |
|---|---|
| Startup | Restart after its threshold; readiness/liveness wait for startup success |
| Readiness | Remove unready endpoint from Service traffic; no restart by itself |
| Liveness | Restart the failed container |

See [volume notes](01-kubernetes-volumes/README.md).

```bash
python3 scripts/run_kubernetes_labs.py 13
```

Reference: [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

## Execution evidence

Actual local transcripts are included below after the runs finish. A missing or incomplete transcript is not a completed exercise.

<!-- EVIDENCE -->

### run.txt

[Complete transcript](outputs/run.txt)

````text
Captured 2026-10-07T12:53:39.023997+00:00
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' create namespace homework-s13
namespace/homework-s13 created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 apply -f 12-storage-hpa-probes/app.yaml
persistentvolumeclaim/web-data created
deployment.apps/web-app created
service/web created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 rollout status deployment/web-app --timeout=180s
Waiting for deployment "web-app" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web-app" rollout to finish: 1 of 2 updated replicas are available...
deployment "web-app" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 apply -f 12-storage-hpa-probes/hpa.yml
horizontalpodautoscaler.autoscaling/web-app created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get pvc,pv,sc
NAME                             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/web-data   Bound    pvc-63a5ae6b-2242-473e-aa5b-8a9a06c72912   500Mi      RWO            standard       <unset>                 7s

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/pvc-5f552fd6-f87a-49c5-9436-694ca80bd20c   500Mi      RWO            Delete           Bound       default/student-pvc     standard       <unset>                          18d
persistentvolume/pvc-63a5ae6b-2242-473e-aa5b-8a9a06c72912   500Mi      RWO            Delete           Bound       homework-s13/web-data   standard       <unset>                          7s
persistentvolume/student-pv                                 1Gi        RWO            Retain           Available                                          <unset>                          18d

NAME                                             PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
storageclass.storage.k8s.io/standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  29d
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 wait --for=condition=Ready pod/client --timeout=120s
pod/client condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 exec client -- wget -qO- http://web
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
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get pods -l app=web-app -o json
{
    "apiVersion": "v1",
    "items": [
        {

[Excerpt: 1342 intermediate lines omitted; complete transcript linked above.]

$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get deployment web-app -o 'jsonpath={.spec.replicas}'
2
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get hpa
NAME      REFERENCE            TARGETS          MINPODS   MAXPODS   REPLICAS   AGE
web-app   Deployment/web-app   cpu: 1000%/50%   2         5         2          96s
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 top pods
NAME                       CPU(cores)   MEMORY(bytes)
client                     0m           0Mi
load-generator             339m         3Mi
web-app-85c8fd8f57-rx84t   250m         11Mi
web-app-85c8fd8f57-wbk47   250m         10Mi
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get pods
NAME                       READY   STATUS    RESTARTS   AGE
client                     1/1     Running   0          95s
load-generator             1/1     Running   0          85s
web-app-85c8fd8f57-757kh   0/1     Running   0          5s
web-app-85c8fd8f57-dfrcd   0/1     Running   0          5s
web-app-85c8fd8f57-rr27z   0/1     Running   0          5s
web-app-85c8fd8f57-rx84t   1/1     Running   0          92s
web-app-85c8fd8f57-wbk47   1/1     Running   0          102s
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get deployment web-app -o 'jsonpath={.spec.replicas}'
5
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 delete pod load-generator
pod "load-generator" deleted from homework-s13 namespace
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 describe hpa
Name:                                                  web-app
Namespace:                                             homework-s13
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Wed, 07 Oct 2026 18:23:46 +0530
Reference:                                             Deployment/web-app
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  1002% (250m) / 50%
Min replicas:                                          2
Max replicas:                                          5
Behavior:
  Scale Up:
    Stabilization Window: 0 seconds
    Select Policy: Max
    Policies:
      - Type: Pods     Value: 4    Period: 15 seconds
      - Type: Percent  Value: 100  Period: 15 seconds
  Scale Down:
    Stabilization Window: 30 seconds
    Select Policy: Max
    Policies:
      - Type: Percent  Value: 100  Period: 15 seconds
Deployment pods:       5 current / 5 desired
Conditions:
  Type            Status  Reason            Message
  ----            ------  ------            -------
  AbleToScale     True    ReadyForNewScale  recommended size matches current size
  ScalingActive   True    ValidMetricFound  the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooManyReplicas   the desired replica count is more than the maximum replica count
  ScaledToZero    False   NotScaledToZero   the HPA controller did not scale the workload to zero
Events:
  Type     Reason                        Age                    From                       Message
  ----     ------                        ----                   ----                       -------
  Warning  FailedGetResourceMetric       2m59s (x2 over 3m14s)  horizontal-pod-autoscaler  failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedComputeMetricsReplicas  2m59s (x2 over 3m14s)  horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedGetResourceMetric       118s (x4 over 2m44s)   horizontal-pod-autoscaler  failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Warning  FailedComputeMetricsReplicas  118s (x4 over 2m43s)   horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Normal   SuccessfulRescale             103s                   horizontal-pod-autoscaler  New size: 5; reason: cpu resource utilization (percentage of request) above target
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s13 get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
client                     1/1     Running   0          3m14s   10.244.0.59   minikube   <none>           <none>
web-app-85c8fd8f57-757kh   1/1     Running   0          104s    10.244.0.63   minikube   <none>           <none>
web-app-85c8fd8f57-dfrcd   1/1     Running   0          104s    10.244.0.65   minikube   <none>           <none>
web-app-85c8fd8f57-rr27z   1/1     Running   0          104s    10.244.0.64   minikube   <none>           <none>
web-app-85c8fd8f57-rx84t   1/1     Running   0          3m11s   10.244.0.60   minikube   <none>           <none>
web-app-85c8fd8f57-wbk47   1/1     Running   0          3m21s   10.244.0.57   minikube   <none>           <none>
[exit 0]
LAB EXECUTION FINISHED
````
