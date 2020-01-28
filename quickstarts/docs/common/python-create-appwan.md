    Update the Resoure.yaml file to include the AppWan option to create the NF AppWan tying the gateway, client and service created in the previous steps. Don't forget to change the action on the service option to "get".
    ``` yaml
    environment: production
    gateway_list:
    - action: get
      cloud: azure
      count: 1
      names:
      - AZCPEGWx0xWESTUS
      region: westus
      regionalCidr:
      - 10.20.10.0/24
      regkeys:
      - 21DB86724EC3F31C11C1C9D68CE5ECD6A06F057E
      resourceGroup:
        name: demoPythonTerraform01
        region: centralus
      tag: TerraformDemo
    network_action: get
    network_name: DemoNet01
    services:
    - action: get
      gateway: AZCPEGWx0xWESTUS
      ip: 10.20.10.5
      name: AZCPEGWx0xWESTUS--10.20.10.5--22
      port: 22
      type: host
    terraform:
      bin: terraform
      output: 'no'
      source: ./quickstarts/docs/terraform
      work_dir: .
    appwans:
    - action: create
      endpoints:
      - BranchGatewayName
      - ClientName
      name: appwan-ssh-22
      services:
      - AZCPEGWx0xWESTUS--10.20.10.5--22
    ```
    1. After the script ran again successfully, the connectivity should have been up.
    ![Image](../images/CreateAppWan06.png)
