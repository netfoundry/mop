# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}

{!common/nfadmin-ssh.md!}

# Azure Specifics

* Username Allowed: Any
* Root Allowed: No
* Password Authentication: Yes

Azure allows you to choose a username when launching an instance.  

Please assign an ssh key when launching the instance, if you wish to access this machine post deployment.

Read more on the Azure documentation [Here](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/create-ssh-keys-detailed)






