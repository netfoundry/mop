# Secure Connectivity to Cloud Applications
### Overview
We will provide series of quickstart guides on how to quickly deploy and configure Secure Overlay Network via NetFoundry to connect Enterprise Remote Users or Branch Applications/Users to Applications located in various public or private clouds.

### Supported Cloud Providers
1. AliCloud
    1. [Getting Started Guide](cloud/alicloud/getting-started.md)
1. AWS Cloud Connectivity
    1. [Bastion Host](cloud/aws/aws-bastion.md)    
1. Azure Cloud Connectivity
    1. [Use Case Overview](cloud/azure/intro.md)
    1. [Mobile User to Cloud Application Connectivity](cloud/azure/connectUser2App.md)
    1. [Branch Application to Cloud Application Connectivity](cloud/azure/connectApp2App.md)
    1. [Bastion Host](cloud/azure/azure-bastion.md)
    1. [Accessing Azure Stack](cloud/azure/accessing-azure-stack.md)
1. Google Cloud Connectivity
    1. [Getting Started Guide](cloud/gcp/getting-started.md)
1. Oracle Cloud
    1. [Getting Started Guide](cloud/ocp/getting-started.md)
    1. [Import Oracle Cloud Public Image](cloud/ocp/image-import.md)
1. VCPE
    1. [CPE Automation (Ubuntu)](cloud/vcpe/cpe-automation-ub.md)
    1. [CPE Automation](cloud/vcpe/cpe-automation.md)
    1. [CPE Automation Supplement](cloud/vcpe/cpe-automation-supplement.md)
    1. [Super Micro](cloud/vcpe/cpe-supermicro.md)

### Supported HyperVisor Providers
1. Hyper-V
    1. [Getting Started Guide](hypervisor/hyper-v/getting-started.md) 
1. KVM
    1. [Getting Started Guide](hypervisor/kvm/getting-started.md) 
1. VMware
    1. [Getting Started Guide](hypervisor/vmware/getting-started.md)
1. VirtualBox
    1. [Getting Started Guide](hypervisor/virtualbox/getting-started.md) 


!!! note
    Regardless of where Applications Users are trying to reach reside, NetFoundry (NF) Network Fabric needs to be provisioned and deployed first.
    Navigate to [NetFoundry/NF Fabric](netfoundry/intro.md) to find more information on how to stand up the NF Network Fabric.
