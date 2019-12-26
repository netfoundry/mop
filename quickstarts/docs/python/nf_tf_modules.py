#!/usr/bin/python3


def create_vpc(region, pbsubnet, pvsubnet, source):
    tf_module_vpc = {
        "source" : "%s/m-aws-vpc" % source,
        "awsRegion" : region,
        "public_subnet_cidr" : pbsubnet,
        "private_subnet_cidr" : pvsubnet,
    }
    return tf_module_vpc


def create_vm_aws(vpc, region, ami, vm_name, nfkey, source):
    tf_module_vm = {
        "source" : "%s/m-aws-instance" % source,
        "awsRegion" : region,
        "vm_name": vm_name,
        "nfnKey" : nfkey,
        "ami" : ami,
        "eth1_scriptPath": source,
        "sgId" : "${module.%s.sgId}" % vpc,
        "keyPairId" : "${module.%s.keyPairId}" % vpc,
        "publicSubnetId" : "${module.%s.publicSubnetId}" % vpc,
        "privateSubnetId" : "${module.%s.privateSubnetId}" % vpc
    }
    return tf_module_vm

def create_rg_azure(resourceGroup, tag, source):
    tf_module_rg = {
        "source" : "%s/m-azure-rg" % source,
        "resourceGroupName": resourceGroup['name'],
        "resourceGroupRegion": resourceGroup['region'],
        "tagEnvironment": tag
    }
    return tf_module_rg

def create_vnet_azure(rg, region, regionalCidr, tag, source):
    tf_module_vnet = {
        "source" : "%s/m-azure-vnet" % source,
        "resourceGroupName": "${module.%s.rgName}" % rg,
        "region" : region,
        "virtualNetworkName": region + '-vNet',
        "regionalCidr": regionalCidr,
        "virtualSubnetName": region + '-subnet',
        "subnetCidr": regionalCidr[0],
        "virtualRouteTable": region + '-routeTable',
        "tagEnvironment": tag
    }
    return tf_module_vnet

def create_vm_azure(rg, region, vmName, nfkey, subnet, tag, source):
    tf_module_vm = {
        "source" : "%s/m-azure-vm" % source,
        "resourceGroupName": "${module.%s.rgName}" % rg,
        "region" : region,
        "vmName": vmName,
        "nfnKey" : nfkey,
        "nicName": vmName + '-nic',
        "publicIp": vmName + '-publicIp',
        "securityGroup": vmName + '-securityGroup',
        "publicSubnetId": "${module.%s.publicSubnetId}" % subnet,
        "tagEnvironment": tag
    }
    return tf_module_vm

def create_output(instance, item):
    value = "${module.%s.%s}" % (instance, item)
    tf_output = {"value": [value]}
    return tf_output
