variable "resourceGroupName" {
  description = "Resource Group name"
}

variable "region" {
  description = "Region for vm"
}

variable "virtualNetworkName" {
  description = "Virtual Network name"
}

variable "regionalCidr" {
  description = "CIDR for vnets"
}

variable "virtualSubnetName" {
  description = "Virtual Subnet name"
}

variable "subnetCidr" {
  description = "CIDR for vnet"
}

variable "virtualRouteTable" {
  description = "name of the virtual route table"
}

variable "tagEnvironment" {
  description = "define a tag for resources created"
}
