# CoreDNS

CoreDNS provides cluster DNS in this Minikube installation. A Pod's resolver sends queries to the kube-dns Service. The CoreDNS kubernetes plugin watches API objects and answers cluster Service/endpoint queries. Names outside the cluster domain are typically sent to upstream resolvers by the forward plugin. A cache reduces repeated upstream work.

The Corefile lives in the `coredns` ConfigMap in kube-system. The captured session output includes the actual configuration and recent logs. Common plugins include kubernetes, forward, cache, loop, health and ready; their presence and settings should be checked in the actual Corefile.

Troubleshoot in order: read the client Pod's `/etc/resolv.conf`; try a full Service name; check that the Service and EndpointSlices exist; check CoreDNS Pods and the kube-dns Service; inspect logs/config; then check reachability and NetworkPolicies on UDP/TCP port 53. A failed HTTP request with successful DNS resolution is not necessarily a DNS problem.

```bash
scripts/kubectl -n homework-s11 exec client -- cat /etc/resolv.conf
scripts/kubectl -n kube-system get pods -l k8s-app=kube-dns
scripts/kubectl -n kube-system get configmap coredns -o yaml
scripts/kubectl -n kube-system logs -l k8s-app=kube-dns --tail=30
```

Reference: [Debug DNS resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/).
