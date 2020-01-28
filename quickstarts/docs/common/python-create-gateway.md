    Clone this repo (git clone https://github.com/netfoundry/mop.git)
    1. Update [Resource yaml](../python/nf_resources.yml) file with the desired options to feed into the wrapper script as described
    in the following code snippet.
    [All Resource.yml Options](README.md)
    1. Run this from the root folder to create GW in NF Console UI and Azure.
    ``` python
    python3 quickstarts/docs/python/nf_resources.py --file quickstarts/docs/python/nf_resources.yml
    ```
    Required Configuration Parameters for Gateway Creation
    ``` yaml
    environment: production
    network_action: get
    network_name: DemoNet01
    gateway_list:
    - action: create
      cloud: azure
      count: 1
      names: []
      region: westus
      regionalCidr: [10.20.10.0/24]
      regkeys: []
      resourceGroup:
        name: demoPythonTerraform01
        region: centralus
      tag: TerraformDemo
    terraform:
      bin: terraform
      output: 'no'
      source: ./quickstarts/docs/terraform
      work_dir: .
    ```
    1. After the script is run successfully, one can see that the gateway name and registration key were saved in Resource.yml file. The name is created automatically based on region and gateway type joined with x and gateway count (AZCPEGW means an azure type gateway in NF console). One can create more than one gateway in the same region by increasing the count to more than 1.
    ``` yaml
    environment: production
    gateway_list:
    - action: create
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
    ```
    ![Image](../images/CreateManagedGatewayAzure11.png)
    ![Image](../images/CreateManagedGatewayAzure12.png)
