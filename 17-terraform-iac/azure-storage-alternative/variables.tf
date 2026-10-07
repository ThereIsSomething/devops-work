variable "subscription_id" { type = string }
variable "storage_account_name" { type = string }
variable "resource_group_name" { type = string }
variable "stage" {
  type    = string
  default = "initial"
}
