!!! note "Environment Setup Requirements"

    1. [~/.env](../../api/python/etc/env) to store NF Credentials in (e.g. `clientId, clientSecret`) to obtain a session token for NF API

    1. Export Azure Credentials (e.g, `export ARM_TENANT_ID, ARM_CLIENT_ID, ARM_CLIENT_SECRET, ARM_SUBSCRIPTION_ID`) to enable resource gateway creation in Azure Resource Group via Terraform.
    1. Terraform and Python3 installed in path.

    Additional Information:

    1. The new Resource Group in Azure is created based on then name provided in [Resource yaml](../api/python/etc/nf_resources.yml), if one does not exists already in the same region (e.g. centralus). The action delete gateway will delete the RG as well even if it was an existing RG. If one does not want to delete the RG, the command `terraform state rm "{tf resource name for RG}"` needs to be run before running the gateway delete step. This will ensure that the RG is not deleted.
    1. A new vNet will be created and NF Gateway will be placed in it.
    1. Environment means the NF Console Environment used (e.g. production), not Azure.
