# resource.yaml file opions

``` yaml
appwans:
- action: { e.g. create, get, delete}
  endpoints: { list of endpoint names to be added}
  name: { name for the appwan}
  services: { list of services to be added}
environment: {NF Console Environment, e.g. Production}
gateway_list:
- action: { e.g. create, get, delete}
  cloud: azure
  count: 1
  names: []
  region:
  regionalCidr: []
  regkeys: []
  resourceGroup:
    name:
    region:
  tag: TerraformDemo
network_action:
network_name: Demo01
services:
- action: { e.g. create, get, delete}
  gateway: { name of the gateway used for this service}
  ip: (destination ip for the service)
  name: {empty, automatically generated and populated by the wrapper scipt}
  port: (destination port for the service)
  type: { e.g. host, network}
terraform:
  bin: { path to terraform binary}
  output: { boolean e.g. no or yes}
  source: ./quickstarts/docs/terraform
  work_dir: .
```
