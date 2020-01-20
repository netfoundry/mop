# Configure the Microsoft Azure Provider with environment variables set
provider "azurerm" {
    version = "=1.38.0"
}

# Create virtual network
resource "azurerm_virtual_network" "terraformnetwork" {
    name                = "${var.virtualNetworkName}"
    address_space       = "${var.regionalCidr}"
    location            = "${var.region}"
    resource_group_name = "${var.resourceGroupName}"

    tags = {
        environment = "${var.tagEnvironment}"
    }
}

# Create virtual subnet
resource "azurerm_subnet" "terraformsubnet" {
    depends_on = [azurerm_virtual_network.terraformnetwork]
    name                 = "${var.virtualSubnetName}"
    resource_group_name  = "${var.resourceGroupName}"
    virtual_network_name = "${azurerm_virtual_network.terraformnetwork.name}"
    address_prefix       = "${var.subnetCidr}"
}

# Create route table
resource "azurerm_route_table" "terraformroutetable" {
  depends_on = [azurerm_virtual_network.terraformnetwork]
  name                          = "${var.virtualRouteTable}"
  location                      = "${azurerm_virtual_network.terraformnetwork.location}"
  resource_group_name           = "${var.resourceGroupName}"
  disable_bgp_route_propagation = false

  tags = {
    environment = "${var.tagEnvironment}"
  }
}

resource "azurerm_subnet_route_table_association" "terraformsubnetroutetable" {
  depends_on = [azurerm_route_table.terraformroutetable, azurerm_subnet.terraformsubnet]
  subnet_id      = "${azurerm_subnet.terraformsubnet.id}"
  route_table_id = "${azurerm_route_table.terraformroutetable.id}"
}

output "publicSubnetId" {
  value = "${azurerm_subnet.terraformsubnet.id}"
}
