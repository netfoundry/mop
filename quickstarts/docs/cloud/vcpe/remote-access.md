# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}

{!common/nfadmin-ssh.md!}

# VCPE Specifics

* Username Allowed: nfadmin
* Root Allowed: No
* Password Authentication: Yes
* Default Password: nfadmin

The best practice is to enable ssh key access after first boot and disable password authentication. If password option is desirable, it must be changed after the first login.  
