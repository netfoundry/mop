### Create and Deploy NF Gateway in Branch Datacenter
This section will guide a user through the steps on how to create a NF Manage Gateway in the NF Console UI and install it in the Branch Datacenter.

!!! example "Console UI"
    1. Navigate to Manage Gateways Page
    1. Click on + sign in the top right corner.
    ![Image](../images/CreateManagedGatewayAzure01.png)
    1. Click on "Create Gateway" on the VCPE Gateway Card
    ![Image](../images/GatewayTiles.png)
    1. Fill in the required information and click on "Create"
    ![Image](../images/CreateBranchGatewayDetails.png)
    1. Copy the Client Registration Key
    ![Image](../images/RegKeyBranchGatewayDetails.png)
    1. Click on "Download" button on the Installation Package Card
    ![Image](../images/DownloadBranchGatewayDetails.png)
    1. Download the correct image for the desired Hypervisor.
    1. Follow the installation procedure linked in the description of each image type (i.e. "Click Here").
    1. Once installed, login into it locally with ssh and register it using the key copied in the previous step. Run the following command `sudo nfnreg "reg key"`
    ![Image](../images/RegistrationBranchGatewayDetails.png)
    1. Once registered, one should see the gateway status turn to green in NF Console UI
    ![Image](../images/GreenStatusBranchGatewayDetails.png)
    1. Done
