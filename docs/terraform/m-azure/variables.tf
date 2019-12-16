variable "resourceGroupName" {
  description = "Resource Group name"
}

variable "resourceGroupRegion" {
  description = "Region for RG"
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

variable "publicIp" {
  description = "name of public ip resource"
}

variable "nicName" {
  description = "name of nic resource"
}

variable "securityGroup" {
  description = "cloud security group"
  default     = "terraform-sg-demo"
}

variable "plan_publisher" {
  description = "azure image plan publisher"
  default = "netfoundryinc"
}

variable "plan_product" {
  description = "azure image plan product"
  default = "centos"
}

variable "plan_name" {
  description = "azure image plan name"
  default = "gateway"
}

variable "imageOffer" {
  description = "azure image"
  default = "centos"
}

variable "imagePublisher" {
  description = "azure image publisher"
  default = "netfoundryinc"
}

variable "imageSku" {
  description = "azure image sku"
   default = "gateway"
}

variable "vmName" {
  description = "name of vm to deploy"
}

variable "userName" {
  description = "vm username"
  default = "nfadmin"
}

variable "nfnKey" {
  description = "Nefroudry GW registration key"
}

variable "publicSshKeyPath" {
  description = "SSH Public Key path"
  default = "~/.ssh/id_rsa.pub"
}

variable "privateSshKeyPath" {
  description = "SSH Private Key path"
  default = "~/.ssh/id_rsa"
}

variable "tagEnvironment" {
  description = "define a tag for resources created"
}
