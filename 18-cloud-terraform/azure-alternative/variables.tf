variable "subscription_id" { type = string }
variable "location" {
  type    = string
  default = "centralindia"
}
variable "storage_account_name" {
  type        = string
  description = "Globally unique name of 3-24 lowercase letters and digits."
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Use 3-24 lowercase letters and digits."
  }
}

variable "resource_group_name" {
  type    = string
  default = "rg-devops-homework"
}
variable "enable_vm" {
  type    = bool
  default = false
}
variable "ssh_public_key" {
  type        = string
  default     = null
  description = "SSH public key, required only when enable_vm=true. Never supply the private key."
}
variable "vm_size" {
  type    = string
  default = "Standard_B1s"
}
