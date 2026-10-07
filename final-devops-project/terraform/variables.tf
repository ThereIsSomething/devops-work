variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "cluster_name" {
  type    = string
  default = "nitish-homework"
}
variable "administrator_principal_arn" {
  type        = string
  description = "IAM role or user ARN granted EKS cluster admin; not an STS session ARN."
}
variable "api_allowed_cidrs" {
  type        = list(string)
  description = "Trusted public source IPs in CIDR notation, e.g. your current IP/32."
}
variable "kubernetes_version" {
  type        = string
  default     = null
  description = "Omit to use the EKS default; select a supported standard-support version before apply."
}
