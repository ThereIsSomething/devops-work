# Session 13: Storage, HPA and Probes

**Nitish Kumar Bhambu — 24BCS10589**

The mini project adapts the instructor's web-app exercise: two Nginx replicas, a 500Mi PVC, a Service, startup/readiness/liveness probes and an HPA with a 50% CPU target and a maximum of five replicas. On this single-node Minikube cluster, both replicas can mount the ReadWriteOnce claim. That design is not a general solution for replicas spread across nodes; use appropriate per-replica or shared storage in a multi-node application.

The persistence check writes a marker to `/data/student.txt`, deletes one Pod, waits for its replacement, and reads the same marker. `/scratch` uses emptyDir and is local to each Pod. The run includes a busybox HTTP load generator plus bounded CPU work in the Nginx containers to make CPU scaling observable. I used both HTTP requests and CPU work for this test.

HPA needs the metrics API and CPU requests on containers. The calculation is approximately `ceil(current replicas × current utilization / target utilization)`, with stabilization and readiness checks affecting the result. The scale-down window is shortened to 30 seconds for this lab.

| Probe | Failure consequence |
|---|---|
| Startup | Restart after its threshold; readiness/liveness wait for startup success |
| Readiness | Remove unready endpoint from Service traffic; no restart by itself |
| Liveness | Restart the failed container |

See [volume notes](01-kubernetes-volumes/README.md).

```bash
kubectl -n homework-s13 get pvc
kubectl -n homework-s13 get hpa
kubectl -n homework-s13 top pods
kubectl -n homework-s13 describe hpa web-app
```

Reference: [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s13
namespace/homework-s13 created

zephoryx@fedora$ kubectl -n homework-s13 apply -f 12-storage-hpa-probes/app.yaml
persistentvolumeclaim/web-data created
deployment.apps/web-app created
service/web created

zephoryx@fedora$ kubectl -n homework-s13 rollout status deployment/web-app
Waiting for deployment "web-app" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web-app" rollout to finish: 1 of 2 updated replicas are available...
deployment "web-app" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s13 apply -f 12-storage-hpa-probes/hpa.yml
horizontalpodautoscaler.autoscaling/web-app created

zephoryx@fedora$ kubectl -n homework-s13 get pvc,pv,sc
NAME                             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/web-data   Bound    pvc-63a5ae6b-2242-473e-aa5b-8a9a06c72912   500Mi      RWO            standard       <unset>                 7s

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/pvc-5f552fd6-f87a-49c5-9436-694ca80bd20c   500Mi      RWO            Delete           Bound       default/student-pvc     standard       <unset>                          18d
persistentvolume/pvc-63a5ae6b-2242-473e-aa5b-8a9a06c72912   500Mi      RWO            Delete           Bound       homework-s13/web-data   standard       <unset>                          7s
persistentvolume/student-pv                                 1Gi        RWO            Retain           Available                                          <unset>                          18d

NAME                                             PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
storageclass.storage.k8s.io/standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  29d

zephoryx@fedora$ kubectl -n homework-s13 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s13 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ kubectl -n homework-s13 exec client -- wget -qO- http://web
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ kubectl -n homework-s13 get pods -l app=web-app -o json
{
    "apiVersion": "v1",
    "items": [
        {
            "apiVersion": "v1",
            "kind": "Pod",
# ... intermediate output omitted ...
        }
    ],
    "kind": "List",
    "metadata": {
        "resourceVersion": ""
    }
}

zephoryx@fedora$ kubectl -n homework-s13 exec web-app-85c8fd8f57-kmq72 -- sh -c 'echo persistent-homework-data > /data/student.txt; echo ephemeral-data > /scratch/transient.txt; cat /data/student.txt'
persistent-homework-data

zephoryx@fedora$ kubectl -n homework-s13 delete pod web-app-85c8fd8f57-kmq72
pod "web-app-85c8fd8f57-kmq72" deleted from homework-s13 namespace

zephoryx@fedora$ kubectl -n homework-s13 rollout status deployment/web-app
Waiting for deployment "web-app" rollout to finish: 1 of 2 updated replicas are available...
deployment "web-app" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s13 get pods -l app=web-app -o json
{
    "apiVersion": "v1",
    "items": [
        {
            "apiVersion": "v1",
            "kind": "Pod",
# ... intermediate output omitted ...
        }
    ],
    "kind": "List",
    "metadata": {
        "resourceVersion": ""
    }
}

zephoryx@fedora$ kubectl -n homework-s13 exec web-app-85c8fd8f57-rx84t -- cat /data/student.txt
persistent-homework-data

zephoryx@fedora$ kubectl -n homework-s13 get hpa
NAME      REFERENCE            TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
web-app   Deployment/web-app   cpu: <unknown>/50%   2         5         2          11s

zephoryx@fedora$ kubectl -n homework-s13 top pods
error: metrics not available yet
# Exit status: 1

zephoryx@fedora$ kubectl -n homework-s13 apply -f 12-storage-hpa-probes/load-generator.yaml
pod/load-generator created
CPU workload: bounded 150-second busy loop in each application Pod; HTTP load-generator also running.

zephoryx@fedora$ kubectl -n homework-s13 get hpa
NAME      REFERENCE            TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
web-app   Deployment/web-app   cpu: <unknown>/50%   2         5         2          32s

zephoryx@fedora$ kubectl -n homework-s13 top pods
NAME                       CPU(cores)   MEMORY(bytes)
client                     9m           0Mi
web-app-85c8fd8f57-rx84t   121m         10Mi
web-app-85c8fd8f57-wbk47   58m          11Mi

zephoryx@fedora$ kubectl -n homework-s13 get pods
NAME                       READY   STATUS    RESTARTS   AGE
client                     1/1     Running   0          31s
load-generator             1/1     Running   0          21s
web-app-85c8fd8f57-rx84t   1/1     Running   0          28s
web-app-85c8fd8f57-wbk47   1/1     Running   0          38s

zephoryx@fedora$ kubectl -n homework-s13 get deployment web-app -o 'jsonpath={.spec.replicas}'
2

zephoryx@fedora$ kubectl -n homework-s13 get hpa
NAME      REFERENCE            TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
web-app   Deployment/web-app   cpu: <unknown>/50%   2         5         2          53s

zephoryx@fedora$ kubectl -n homework-s13 top pods
NAME                       CPU(cores)   MEMORY(bytes)
client                     9m           0Mi
web-app-85c8fd8f57-rx84t   121m         10Mi
web-app-85c8fd8f57-wbk47   58m          11Mi

zephoryx@fedora$ kubectl -n homework-s13 get pods
NAME                       READY   STATUS    RESTARTS   AGE
client                     1/1     Running   0          53s
load-generator             1/1     Running   0          43s
web-app-85c8fd8f57-rx84t   1/1     Running   0          50s
web-app-85c8fd8f57-wbk47   1/1     Running   0          60s

zephoryx@fedora$ kubectl -n homework-s13 get deployment web-app -o 'jsonpath={.spec.replicas}'
2

zephoryx@fedora$ kubectl -n homework-s13 get hpa
NAME      REFERENCE            TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
web-app   Deployment/web-app   cpu: <unknown>/50%   2         5         2          75s

zephoryx@fedora$ kubectl -n homework-s13 top pods
NAME                       CPU(cores)   MEMORY(bytes)
client                     9m           0Mi
web-app-85c8fd8f57-rx84t   121m         10Mi
web-app-85c8fd8f57-wbk47   58m          11Mi

zephoryx@fedora$ kubectl -n homework-s13 get pods
NAME                       READY   STATUS    RESTARTS   AGE
client                     1/1     Running   0          74s
load-generator             1/1     Running   0          64s
web-app-85c8fd8f57-rx84t   1/1     Running   0          71s
web-app-85c8fd8f57-wbk47   1/1     Running   0          81s

zephoryx@fedora$ kubectl -n homework-s13 get deployment web-app -o 'jsonpath={.spec.replicas}'
2

zephoryx@fedora$ kubectl -n homework-s13 get hpa
NAME      REFERENCE            TARGETS          MINPODS   MAXPODS   REPLICAS   AGE
web-app   Deployment/web-app   cpu: 1000%/50%   2         5         2          96s

zephoryx@fedora$ kubectl -n homework-s13 top pods
NAME                       CPU(cores)   MEMORY(bytes)
client                     0m           0Mi
load-generator             339m         3Mi
web-app-85c8fd8f57-rx84t   250m         11Mi
web-app-85c8fd8f57-wbk47   250m         10Mi

zephoryx@fedora$ kubectl -n homework-s13 get pods
NAME                       READY   STATUS    RESTARTS   AGE
client                     1/1     Running   0          95s
load-generator             1/1     Running   0          85s
web-app-85c8fd8f57-757kh   0/1     Running   0          5s
web-app-85c8fd8f57-dfrcd   0/1     Running   0          5s
web-app-85c8fd8f57-rr27z   0/1     Running   0          5s
web-app-85c8fd8f57-rx84t   1/1     Running   0          92s
web-app-85c8fd8f57-wbk47   1/1     Running   0          102s

zephoryx@fedora$ kubectl -n homework-s13 get deployment web-app -o 'jsonpath={.spec.replicas}'
5

zephoryx@fedora$ kubectl -n homework-s13 delete pod load-generator
pod "load-generator" deleted from homework-s13 namespace

zephoryx@fedora$ kubectl -n homework-s13 describe hpa
Name:                                                  web-app
Namespace:                                             homework-s13
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Wed, 07 Oct 2026 18:23:46 +0530
Reference:                                             Deployment/web-app
# ... intermediate output omitted ...
  Type     Reason                        Age                    From                       Message
  ----     ------                        ----                   ----                       -------
  Warning  FailedGetResourceMetric       2m59s (x2 over 3m14s)  horizontal-pod-autoscaler  failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedComputeMetricsReplicas  2m59s (x2 over 3m14s)  horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedGetResourceMetric       118s (x4 over 2m44s)   horizontal-pod-autoscaler  failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Warning  FailedComputeMetricsReplicas  118s (x4 over 2m43s)   horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Normal   SuccessfulRescale             103s                   horizontal-pod-autoscaler  New size: 5; reason: cpu resource utilization (percentage of request) above target

zephoryx@fedora$ kubectl -n homework-s13 get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
client                     1/1     Running   0          3m14s   10.244.0.59   minikube   <none>           <none>
web-app-85c8fd8f57-757kh   1/1     Running   0          104s    10.244.0.63   minikube   <none>           <none>
web-app-85c8fd8f57-dfrcd   1/1     Running   0          104s    10.244.0.65   minikube   <none>           <none>
web-app-85c8fd8f57-rr27z   1/1     Running   0          104s    10.244.0.64   minikube   <none>           <none>
web-app-85c8fd8f57-rx84t   1/1     Running   0          3m11s   10.244.0.60   minikube   <none>           <none>
web-app-85c8fd8f57-wbk47   1/1     Running   0          3m21s   10.244.0.57   minikube   <none>           <none>
```
