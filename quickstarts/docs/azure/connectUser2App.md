# Overview
This quickstart guide will provide all the steps to create a secure service between a remote user and an application hosted in Azure Cloud using NetFoundry Overlay Fabric (NFOF).

{!common/fabric-client-important.md!}

## Through NF Web Console UI

{!common/install-nf-client.md!}

{!common/create-azure-gateway.md!}

{!common/create-ip-host-service.md!}

{!common/create-appwan-client.md!}

### Test Connectivity to Application Server

!!! example "To test connectivity, log in to the DemoClinet01 and run ssh username@privateIp"
    ![Image](../images/CreateService06.png)

## Programmatically

### via Python and Terraform

{!common/python-module-note.md!}

{!common/azure-environment-setup-note.md!}

!!! example "Steps"
    1. {!common/python-create-gateway.md!}
    1. Create a test server vm on the same vNet if not already present.
    ![Image](../images/CreateManagedGatewayAzure13.png)
    1. {!common/python-create-service.md!}
    1. Create a client endpoint if not already done so.
    ![Image](../images/DemoClient01.png)
    1. {!common/python-create-appwan.md!}
    1. To test connectivity, log in to the DemoClinet01 and run ssh "username"@"privateIp"
    ![Image](../images/DemoClientTestSsh01.png)
    1. {!common/python-delete-all.md!}

### via Jenkins

In this section, we will use [Resource yaml](../api/python/etc/nf_resources.yml) along with Jenkinsfile to show how to automate the steps further by creating the Jenkins Job

{!common/install-jenkins.md!}
