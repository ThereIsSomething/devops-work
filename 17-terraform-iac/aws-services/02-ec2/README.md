# EC2: compute

**Nitish Kumar Bhambu — 24BCS10589**

EC2 provides virtual machines. An AMI is the starting operating-system image; an instance type selects CPU, memory and other hardware characteristics. Key pairs can support SSH access, although role-based Systems Manager access can avoid opening SSH. A Security Group is a stateful network filter attached to network interfaces. EBS is block storage and can persist independently depending on volume settings.

Private IPs serve VPC communication; a public IPv4 address enables public reachability only with suitable routing and rules. Instance lifecycle includes pending, running, stopping, stopped, shutting-down and terminated. Stopping a VM does not mean all associated storage or IP charges disappear. Typical uses include web servers, workers and development environments.

Reference: [EC2 concepts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html).
