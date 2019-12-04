
## Create a new network fabric
This section will show how to do that through [NF Console](https://nfconsole.io), and programatically  using NF Orchestration's APIs

# via Console UI
1. Click on Network Menu
1. Click on "+" button in the top right corner to create a network
1. Give it a name, e.g. "DemoNet01"
![Image](../images/NetworkMopMenu.png)
1. Wait until the icon network turns green.
![Image](../images/NetworkMopMenuGreen.png)

# via REST API (Python)

!!! note
    For the code clarity, we have broken down the code into multiple Python modules  

    1. [NF REST CRUD (Create,Read, Update and Delete) operations](../../python/nf_requests.py)
    1. [Get MOP Session Token](../../python/nf_token.py)
    1. [Create NF Network](../../python/nf_network.py)
    1. [Wrapper Script to Create NF Resources based on Resource yml file](../../python/nf_resources.py)

Updated the Resource yaml file with the options need to run the wrapper script.
``` yaml

environment: production
gateway_list:
- action: [create, get, delete]
  ami: {{ NF Azure Gateway AMI }}
  cloud: azure
  count: 1
  names: []
  private_subnet: 10.0.11.0/24
  public_subnet: 10.0.10.0/24
  region: ca-central-1
  regkeys: []
  tag: null
network_action: [create, get, delete]
network_name: { e.g. DemoNet01 }
```
