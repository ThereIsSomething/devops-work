variable "subscription_id" { type = string }
variable "resource_group_name" {
  type    = string
  default = "rg-devops-homework"
}
variable "node_vm_size" {
  type    = string
  default = "Standard_D2s_v3"
}
variable "api_allowed_cidrs" {
  type        = list(string)
  description = "Your trusted public source IPs in CIDR notation."
}
