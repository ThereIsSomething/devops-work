# DynamoDB and RDS

**Nitish Kumar Bhambu — 24BCS10589**

DynamoDB is a managed NoSQL database. Tables contain items with attributes. A partition key determines data distribution; an optional sort key orders related items within the same partition-key value. Choose keys around access patterns rather than treating a scan as the default query. It suits predictable key-based access, event data and high-scale application state.

RDS manages relational database instances for engines including PostgreSQL, MySQL, MariaDB, Oracle, SQL Server and Db2, with availability depending on engine, region and offering. Relational tables, SQL and transactions suit structured application data. Use private networking, security groups, appropriate credentials and encryption. Automated backups and snapshots support recovery. Multi-AZ provides availability/failover; read replicas usually serve read scaling and have distinct replication behavior. Neither replaces a tested recovery plan.

References: [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html), [RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html).
