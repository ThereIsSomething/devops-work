# IAM: governance

**Nitish Kumar Bhambu — 24BCS10589**

IAM controls who can perform which actions on which AWS resources. Users are identities; groups collect users; roles are assumed and issue temporary credentials; policies express permissions and conditions. Effective access depends on all applicable policies, including explicit denies and organization boundaries.

I would use a role for an application or CI job and temporary/SSO access for a person. Least privilege means granting only the needed actions at the needed scope. Enable MFA, avoid root-account daily use, review unused permissions and do not commit access keys. A group can share a policy among students, while an EC2 role can let a VM read a specific S3 bucket without embedding keys.

Reference: [IAM introduction](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html).
