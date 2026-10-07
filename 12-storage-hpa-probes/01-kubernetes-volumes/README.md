# Kubernetes volumes

| Mechanism | Lifetime and use | Limitation |
|---|---|---|
| emptyDir | Created for one Pod; shared by its containers; survives container restarts | Deleted when the Pod is removed |
| hostPath | Mounts a path from one node | Tied to that node; exposes host data and needs careful permissions |
| PersistentVolume | Cluster storage resource, provisioned manually or dynamically | Access modes and reclaim policy matter |
| PersistentVolumeClaim | Application request for storage | Must bind to a compatible PV |
| StorageClass | Defines provisioner and parameters | Depends on an installed driver/provisioner |
| Dynamic provisioning | Creates a PV when a claim requests a class | Needs a functioning provisioner and available capacity |

In this exercise `/scratch` is emptyDir and `/data` uses a PVC. Minikube's standard class provisions node-local storage. A PVC lets data survive Pod replacement; it is not automatically a backup. The PV reclaim policy controls what happens after the claim is deleted, while actual backend behavior also depends on the provisioner. ReadWriteOnce means read/write on one node, not necessarily one Pod. ReadWriteOncePod is the stricter single-Pod mode where supported.

A static hostPath example for a disposable single-node lab would create a PV with `hostPath.path: /data/homework`, a capacity, access mode and storageClassName, then a matching PVC. The running project uses dynamic provisioning instead of assuming that a manually created node path exists.

Reference: [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/), [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).
