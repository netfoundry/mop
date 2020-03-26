This section provides the powershell code to spin up a NF client with the name as computer name fetched by PS script. 

Here is a sample powershell script with example Clientid, Secret, Region name,Network name which needs to be changed as suits the need. 

``` yaml 
environment: {NF Console Environment, e.g. Production}
network_name: { e.g. DemoNet01 } 
region_name: nearest D{nearest dc in AWS, us-east-1}
```
Clientid and Secret needs to be fetched from the NFconsole

```powershell
#Set Endpoint name to second half of computer name:
$endpoint_name = $ENV:COMPUTERNAME.Split("-")[-1]
```

Here is [PS script](file:///C:\Users\Sathish\Desktop\NF-pwrshell)