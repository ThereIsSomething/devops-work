# FQDN and Kubernetes Service DNS

A fully qualified domain name specifies the complete DNS name, such as `clusterip.homework-s11.svc.cluster.local`. A final dot explicitly marks the DNS root, though tools commonly accept the name without it.

The Service pattern is `<service>.<namespace>.svc.<cluster-domain>`. This cluster uses `cluster.local`; it is configurable. Within homework-s11 a Pod can use `clusterip`; from another namespace use `clusterip.homework-s11` or the full name. `/etc/resolv.conf` search domains expand short names.

A normal ClusterIP Service resolves to its stable virtual IP. A headless Service resolves to endpoint IPs. StatefulSets can use names such as `postgres-0.postgres.homework-final.svc.cluster.local` when their headless Service and Pod identity are configured appropriately. An ExternalName Service returns a CNAME; DNS aliasing does not rewrite an HTTP Host header or a TLS certificate.

The parent session transcript runs nslookup from a client Pod and tests Pod-to-Service HTTP.

Reference: [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
