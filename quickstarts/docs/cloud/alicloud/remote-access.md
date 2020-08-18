# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}

{!common/nfadmin-ssh.md!}

# AliCloud Specifics

* Username Allowed: nfadmin
* Root Allowed: No
* Password Authentication: No

The AliCloud image username is "nfadmin". Please assign an ssh key when launching the instance, if you wish to access this machine post deployment.

!!! Note
    **Password Reset**: In order for the password reset function to work, you must reboot the machine afterward the procedure is complete for the password to take effect. Reset password only reset the root password. Using Ali Console, you can VNC into the VM with the "root" as user and password. Once you login, the nfadmin password can be resetted via the shell command (passwd nfadmin).  This will enable ssh login with user "nfadmin" using password.


Read more on the AliCloud documentation [Here](https://www.alibabacloud.com/help/doc-detail/71529.htm)



