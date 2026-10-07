# S3: object storage

**Nitish Kumar Bhambu — 24BCS10589**

S3 stores objects in buckets. Each object has a key, content and metadata; it is not a mounted POSIX filesystem. Storage classes trade availability, retrieval characteristics and cost for different access patterns. Versioning preserves object versions, and lifecycle policies can transition or expire data and old versions.

Encryption protects stored data; bucket policies and IAM govern access. Block Public Access helps prevent unintended exposure. The Terraform exercise creates a private, versioned bucket with an explicit encryption configuration. Backups, static assets and logs are common uses. Before destroying a versioned bucket, inspect and remove all versions/delete markers only when that data is no longer needed; the code does not force-delete contents.

Reference: [S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html).
