# VPC: networking

**Nitish Kumar Bhambu — 24BCS10589**

A VPC is a logically isolated AWS network. CIDR defines its address range; subnets divide that range and belong to availability zones. Route tables select next hops. A subnet is public when its route table has a route to an Internet Gateway; an instance also needs an appropriate address and security rules to be reachable.

A private subnet does not have that direct Internet Gateway route. A public NAT Gateway can provide outbound IPv4 access from private subnets through a public subnet, without accepting unsolicited inbound connections. Security Groups are stateful rules at network interfaces. Network ACLs are stateless subnet rules, so return traffic must be allowed explicitly. NAT, public IPs and data transfer can add cost.

Reference: [VPC user guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html).
