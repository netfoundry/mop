### Create and Deploy NF Azure Gateway
This section will guide a user through the steps on how to create a NF Manage Gateway in the NF Console UI and install it in the Azure vNet.

!!! example "Console UI"
    1. Navigate to Manage Gateways Page
    1. Click on + sign in the top right corner.
    ![Image](../images/CreateManagedGatewayAzure01.png)
    1. Click on "Create Gateway" on the Azure Cloud Gateway Card
    ![Image](../images/CreateManagedGatewayAzure02.png)
    1. Fill in the required information and click on "Create"
    ![Image](../images/CreateManagedGatewayAzure03.png)
    1. Copy the Client Registration Key
    ![Image](../images/CreateManagedGatewayAzure04.png)
    1. Click on "Deploy to Microsoft Azure". It will take you to the Azure Portal and ask you for your login credentials.
    1. You will be presented with the template that needs to be filled. The first section is the Basics regarding your Subscription and Resource Group this gateway will be deployed in.
    ![Image](../images/CreateManagedGatewayAzure05.png)
    1. The second section related to resources associated with this gateway. e.g. vm name, ip address space, security groups, etc. you will paste the registration key copied in step 5. You will also need the public ssh key to use for access to this gateway remotely.
    ![Image](../images/CreateManagedGatewayAzure06.png)
    1. You will need to agree to Azure Marketplace Terms and Conditions and click to "Purchase" to continue.
    ![Image](../images/CreateManagedGatewayAzure07.png)
    1. If the NF Gateway was deployed successfully. Here is the view of the Resource Group and NF Conole UI.
    ![Image](../images/CreateManagedGatewayAzure08.png)
    ![Image](../images/CreateManagedGatewayAzure09.png)
    1. Done
