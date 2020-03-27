# Global Parameters

#auth paramters
$environment = "sandbox"
$client_id = "*********"
$client_secret = "*******************"
$audience = "https://gateway." + $environment + ".netfoundry.io/"
$api_endpoint = "https://gateway." + $environment + ".netfoundry.io/rest/v1"

#network parameters
$network_name = "EDWARD-PS"

#datacenter paramters
$region_name = "us-east-1"
$provider = "AWS"

#Set Endpoint name to second half of computer name:
$endpoint_name = $ENV:COMPUTERNAME.Split("-")[-1]



# Get a auth token from Auth0

$auth_payload = @{
    client_id=$client_id
    client_secret=$client_secret
    audience=$audience
    grant_type='client_credentials'
}

$auth_json = $auth_payload | ConvertTo-Json

$post_uri =  "https://netfoundry-" + $environment + ".auth0.com/oauth/token"

$auth0_response = Invoke-RestMethod -Method Post -Uri $post_uri -ContentType 'application/json' -Body $auth_json

$token = $auth0_response.access_token

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.add("Authorization", ("Bearer " + $token))


# Get a dataCenter ID:


$datacenter_uri = $api_endpoint + "/dataCenters"

$dataCenter_response = Invoke-RestMethod -Method Get -Uri $datacenter_uri -ContentType 'application/json' -Headers $headers


$dataCenter = $dataCenter_response._embedded.dataCenters | where { $_.locationCode -like $region_name -and $_.provider -like $provider }  | select _links

$dataCenterId = ($dataCenter._links.self.href).Split("/")[-1]


# Get a Netowrk ID:


$network_uri = $api_endpoint + "/networks"

$network_response = Invoke-RestMethod -Method Get -Uri $network_uri -ContentType 'application/json' -Headers $headers


$network = $network_response._embedded.networks | where { $_.name -like $network_name }  | select _links

$networkrId = ($network._links.self.href).Split("/")[-1]


# Create an Endpoint & get reg key

$endpoint_uri = $api_endpoint + "/networks/" + $networkrId + "/endpoints"

$endpoint_payload  = @{
    name = $endpoint_name
    endpointType = "CL"
    dataCenterId = $dataCenterId
}

$endpoint_json = $endpoint_payload | ConvertTo-Json

$endpoint_response  = Invoke-RestMethod -Method Post -Uri $endpoint_uri -ContentType 'application/json' -Body $endpoint_json -Headers $headers

$endpoint_registration_key = $endpoint_response.registrationKey

# Run registration script

Start-Process -FilePath C:\Program Files\DVN\vtc_app\nfnreg $endpoint_registration_key