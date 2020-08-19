# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}


# AWS Specifics

* Username Allowed: nfadmin
* Root Allowed: No
* Password Authentication: No

The AWS image username is "nfadmin". Please assign an ssh key when launching the instance, if you wish to access this machine post deployment.

Read more on the AWS documentation [Here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)






