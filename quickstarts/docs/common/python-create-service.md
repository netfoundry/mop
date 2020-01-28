    Update the Resoure.yaml file to include the Service option to create the NF service on the gateway create in the previous step. Don't forget to change the action on the gateway to "get".
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
    terraform:
      bin: terraform
      output: 'no'
      source: ./quickstarts/docs/terraform
      work_dir: .
    services:
    - action: create
      gateway: AZCPEGWx0xWESTUS
      ip: 10.20.10.5
      port: 22
      name:
      type: host
    ```
    1. After the script run again successfully, the service section should have been populated with the service name as so.
    ``` yaml
    services:
    - action: create
      gateway: AZCPEGWx0xWESTUS
      ip: 10.20.10.5
      name: AZCPEGWx0xWESTUS--10.20.10.5--22
      port: 22
      type: host
    ```
    ![Image](../images/CreateService07.png)
