#!/bin/bash

if [ $# -lt 1 ]; then

   echo -e "\nUsage:"
   echo "     $0 <interface name> "
   echo "i.e.  $0 enp2s0 "
   exit
fi


### check to make sure interface exists
interfacename=$1
checklink=$(ip link show |grep $1 |grep mtu)

if [ -z "$checklink" ]; then
   echo $1 is not a valid interface
   exit
fi


### get the next bridge number automatically
listbridge=$(ls /etc/sysconfig/network-scripts/ifcfg-br* |tail -1)
bridgenumber="${listbridge: -1}"
nextbridgenumber=$(($bridgenumber+1))


### now configure the bridge and interface

echo "DEVICE=br$nextbridgenumber" >bridge_tttt
echo "TYPE=Bridge" >>bridge_tttt
echo "BOOTPROTO=none" >>bridge_tttt
echo "ONBOOT=yes" >>bridge_tttt
echo "STP=off" >>bridge_tttt
echo "NM_CONTROLLED=no" >>bridge_tttt
echo "DELAY=0" >>bridge_tttt

echo "DEVICE=$interfacename" >intf_tttt
echo "ONBOOT=yes" >>intf_tttt
echo "TYPE=Ethernet" >>intf_tttt
echo "NM_CONTROLLED=no" >>intf_tttt
echo "BRIDGE=br$nextbridgenumber" >>intf_tttt


sudo mv bridge_tttt /etc/sysconfig/network-scripts/ifcfg-br$nextbridgenumber
sudo rm -f /etc/sysconfig/network-scripts/ifcfg-$interfacename
sudo mv intf_tttt /etc/sysconfig/network-scripts/ifcfg-$interfacename
echo Restarting Network, this may take few seconds...
sudo systemctl restart network

#### attach the interface to your vm
sudo virsh attach-interface --domain nfgateway --type bridge --source br$nextbridgenumber --model virtio --config --live

echo "--done--"

