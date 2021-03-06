# Configure the Microsoft Azure Provider with environment variables set
provider "azurerm" {
    version = "=1.38.0"
}

# Create a resource group if it doesn’t exist
resource "azurerm_resource_group" "terraformgroup" {
    name     = "${var.resourceGroupName}"
    location = "${var.resourceGroupRegion}"

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Create virtual network
resource "azurerm_virtual_network" "terraformnetwork" {
    name                = "${var.virtualNetworkName}"
    address_space       = "${var.regionalCidr}"
    location            = "${var.region}"
    resource_group_name = "${azurerm_resource_group.terraformgroup.name}"

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Create virtual subnet
resource "azurerm_subnet" "terraformsubnet" {
    name                 = "${var.virtualSubnetName}"
    resource_group_name  = "${azurerm_resource_group.terraformgroup.name}"
    virtual_network_name = "${azurerm_virtual_network.terraformnetwork.name}"
    address_prefix       = "${var.subnetCidr}"
}

# Create public ip resource
resource "azurerm_route_table" "terraformroutetable" {
  name                          = "${var.virtualRouteTable}"
  location                      = "${azurerm_virtual_network.terraformnetwork.location}"
  resource_group_name           = "${azurerm_resource_group.terraformgroup.name}"
  disable_bgp_route_propagation = false

  tags = {
    environment = "${var.tagEnvironment}"
  }
}

# Create public IPs
resource "azurerm_public_ip" "terraformpublicip" {
    name                  = "${var.publicIp}"
    location              = "${var.region}"
    resource_group_name   = "${azurerm_resource_group.terraformgroup.name}"
    allocation_method     = "Static"

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "terraformnsg" {
    name                = "${var.securityGroup}"
    location            = "${var.region}"
    resource_group_name = "${azurerm_resource_group.terraformgroup.name}"

    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Create network interface
resource "azurerm_network_interface" "terraformnic" {
    name                      = "${var.nicName}"
    location                  = "${var.region}"
    resource_group_name       = "${azurerm_resource_group.terraformgroup.name}"
    network_security_group_id = "${azurerm_network_security_group.terraformnsg.id}"
    enable_ip_forwarding      = true

    ip_configuration {
        name                          = "${var.nicName}"
        subnet_id                     = "${azurerm_subnet.terraformsubnet.id}"
        private_ip_address_allocation = "dynamic"
        public_ip_address_id          = "${azurerm_public_ip.terraformpublicip.id}"
    }

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Generate random text for a unique storage account name
resource "random_id" "randomId" {
    keepers = {
        # Generate a new ID only when a new resource group is defined
        resource_group = "${azurerm_resource_group.terraformgroup.name}"
    }

    byte_length = 8
}

# Create storage account for boot diagnostics
resource "azurerm_storage_account" "storageaccount" {
    name                        = "storage${random_id.randomId.hex}"
    resource_group_name         = "${azurerm_resource_group.terraformgroup.name}"
    location                    = "${var.region}"
    account_tier                = "Standard"
    account_replication_type    = "LRS"

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Create virtual machine
resource "azurerm_virtual_machine" "terraformvm" {
    name                  = "${var.vmName}"
    location              = "${var.region}"
    resource_group_name   = "${azurerm_resource_group.terraformgroup.name}"
    network_interface_ids = ["${azurerm_network_interface.terraformnic.id}"]
    vm_size               = "Standard_B1ms"

    storage_os_disk {
        name              = "${var.vmName}OsDisk"
        caching           = "ReadWrite"
        create_option     = "FromImage"
        managed_disk_type = "Premium_LRS"
    }

    plan {
        publisher        = "${var.plan_publisher}"
        product          = "${var.plan_product}"
        name             = "${var.plan_name}"
    }

    storage_image_reference {
        offer            = "${var.imageOffer}"
        publisher        = "${var.imagePublisher}"
        sku              = "${var.imageSku}"
        version          = "latest"
    }

    os_profile {
        computer_name  = "${var.vmName}"
        admin_username = "${var.userName}"
    }

    os_profile_linux_config {
        disable_password_authentication = true
        ssh_keys {
            path     = "/home/${var.userName}/.ssh/authorized_keys"
            key_data = "${file("${var.publicSshKeyPath}")}"
        }
    }

    boot_diagnostics {
        enabled = "true"
        storage_uri = "${azurerm_storage_account.storageaccount.primary_blob_endpoint}"
    }

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

resource "azurerm_subnet_route_table_association" "terraformsubnetroutetable" {
  subnet_id      = "${azurerm_subnet.terraformsubnet.id}"
  route_table_id = "${azurerm_route_table.terraformroutetable.id}"
}

resource "null_resource" "gateway_registration" {

  connection {
    host = "${element(azurerm_public_ip.terraformpublicip.*.ip_address, 0)}"
    type     = "ssh"
    user     = "nfadmin"
    private_key = "${file("~/.ssh/id_rsa")}"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo /opt/netfoundry/vtc/nfnreg ${var.nfnKey}",
    ]
  }
}

output "instance_public_ips" {
  value = "${azurerm_public_ip.terraformpublicip.*.ip_address}"
}
