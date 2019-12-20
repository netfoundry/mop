# resource.yaml file options

``` yaml
appwans:
- action: { e.g. create, get, delete }
  endpoints: { list of endpoint names to be added }
  name: { name for the appwan}
  services: { list of services to be added }
environment: {NF Console Environment, e.g. Production }
gateway_list:
- action: { e.g. create, get, delete }
  cloud: { public cloud, e.g. azure }
  count: 1
  names: { empty, will be filled in by script }
  region: { cloud region that gateways will be deployed in}
  regionalCidr: { list of IP address space in Resource group}
  regkeys: { empty, will be filled in by script }
  resourceGroup:
    name: { Azure Resource Group name used/created }
    region: { Azure Resource Group region used/created }
  tag: { text }
network_action:  { e.g. create, get, delete }
network_name: { network name to use }
services:
- action: { e.g. create, get, delete}
  gateway: { name of the gateway used for this service}
  ip: (destination ip for the service)
  name: {empty, automatically generated and populated by the wrapper script}
  port: (destination port for the service)
  type: { e.g. host, network; host only enabled in this script right now}
terraform:
  bin: { path to terraform binary}
  output: { boolean e.g. no or yes}
  source: ./quickstarts/docs/terraform { where the terraform module is located e.g. azure }
  work_dir: . { directory where the terraform from main plan file to be installed }
```
