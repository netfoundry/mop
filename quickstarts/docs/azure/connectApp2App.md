# Overview
This quickstart guide will provide all the steps to create a secure service between a branch application and/or user and an application hosted in Azure Cloud using NetFoundry Overlay Fabric (NFOF).

!!! info "PAGE UNDER CONSTRUCTION"

{!common/fabric-only-important.md!}

## Through NF Web Console UI

{!common/create-private-gateway.md!}

{!common/create-azure-gateway.md!}

{!common/create-ip-host-service.md!}

{!common/create-appwan-gateway.md!}

### Test Connectivity to Application Server

!!! note "Route to vNet"
    The private IP of NF Gateway (e.g. YourBranchGatewayName) needs to be the next hop to reach the vNet in Azure (e.g. 10.0.8.0/24).
    Thus, a static route will need to be configured in one of the branch routers. NF Gateway can support dynamic routing if needed (e.g.bgp, ospf)

!!! example "Steps"
    1. Log in to a Client App Host in Branch DataCenter
    1. Run ssh username@privateIpOfServerAppHostInAzure
    ![Image](../images/CreateService06.png)

## Programmatically

### via Python and Terraform

{!common/python-module-note.md!}

{!common/azure-environment-setup-note.md!}
