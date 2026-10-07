resource "azurerm_public_ip" "web" {
  count               = var.enable_vm ? 1 : 0
  name                = "pip-devops-homework"
  resource_group_name = data.azurerm_resource_group.lab.name
  location            = data.azurerm_resource_group.lab.location
  allocation_method   = "Static"
  sku                 = "Standard"
}
resource "azurerm_network_security_rule" "http" {
  count                       = var.enable_vm ? 1 : 0
  name                        = "http"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = data.azurerm_resource_group.lab.name
  network_security_group_name = azurerm_network_security_group.app.name
}
resource "azurerm_network_interface" "web" {
  count               = var.enable_vm ? 1 : 0
  name                = "nic-devops-homework"
  resource_group_name = data.azurerm_resource_group.lab.name
  location            = data.azurerm_resource_group.lab.location
  ip_configuration {
    name                          = "web"
    subnet_id                     = azurerm_subnet.app.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.web[0].id
  }
}
resource "azurerm_linux_virtual_machine" "web" {
  count                           = var.enable_vm ? 1 : 0
  name                            = "vm-devops-homework"
  resource_group_name             = data.azurerm_resource_group.lab.name
  location                        = data.azurerm_resource_group.lab.location
  size                            = var.vm_size
  admin_username                  = "labstudent"
  disable_password_authentication = true
  network_interface_ids           = [azurerm_network_interface.web[0].id]
  admin_ssh_key {
    username   = "labstudent"
    public_key = var.ssh_public_key
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }
  custom_data = base64encode(<<-CLOUDINIT
    #cloud-config
    package_update: true
    packages: [nginx]
    runcmd:
      - [sh, -c, "echo 'Hello World from Terraform on Azure' > /var/www/html/index.html"]
      - [systemctl, enable, --now, nginx]
  CLOUDINIT
  )
  depends_on = [azurerm_subnet_network_security_group_association.app]
}
output "web_url" {
  value = var.enable_vm ? "http://${azurerm_public_ip.web[0].ip_address}" : null
}
