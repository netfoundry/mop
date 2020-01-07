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

output "rgName" {
  value = "${azurerm_resource_group.terraformgroup.name}"
}
