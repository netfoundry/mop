# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}


# OCP Specifics

* Username Allowed: "opc" only
* Root Allowed: No
* Password Authentication: No

The Oracle Cloud platform only allows the user "opc".  You can paste in ssh key while launching the instance or create key in the account.

Read more on the OCP documentation [Here](https://docs.cloud.oracle.com/en-us/iaas/Content/GSG/Tasks/testingconnection.htm)






