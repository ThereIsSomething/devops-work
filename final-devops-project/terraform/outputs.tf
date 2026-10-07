output "cluster_name" { value = aws_eks_cluster.lab.name }
output "cluster_endpoint" { value = aws_eks_cluster.lab.endpoint }
output "vpc_id" { value = aws_vpc.lab.id }
output "subnet_ids" { value = aws_subnet.public[*].id }
