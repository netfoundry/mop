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


def create_output(instance):
    value = "${module.%s.instance_public_ips}" % instance
    tf_output = {"value": [value]}
    return tf_output
