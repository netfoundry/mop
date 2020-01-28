    To delete resources created, just follow the reverse order. Change the action to delete for AppWans first, then other resources as indicated in the code snippets.
    ``` yaml
    appwans:
    - action: delete
      endpoints:
      - BranchGatewayName
      - ClientName
      name: null
      services:
      - AZCPEGWx0xWESTUS--10.20.10.5--22
    ```
    1. Services
    ``` yaml
    services:
    - action: delete
      gateway: AZCPEGWx0xWESTUS
      ip: 10.20.10.5
      name: null
      port: 22
      type: host
    ```
    1. Endpoints - will delete all resources in Azure as well.
        1. `terraform state rm "{tf resource name for RG}" // run this before the python script if Resource Group needs to be preserved`
        1.
    ``` yaml
    gateway_list:
    - action: delete
      cloud: azure
      count: 1
      names: []
      region: westus
      regionalCidr:
      - 10.20.10.0/24
      regkeys: []
      resourceGroup:
        name: demoPythonTerraform01
        region: centralus
      tag: TerraformDemo
    ```
    1. Network
    ``` yaml
    environment:  production
    network_action: delete
    network_name: DemoNet01
    ```
    1. Done
