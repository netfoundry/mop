# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}


# GCP Specifics

* Username Allowed: Any
* Root Allowed: No

The Google Cloud platform allows you to specify any user name and ssh key combination. Those user names and ssh key can be stored at the "project" level or at an instance level.  GCP also support injecting user names and ssh key on demand for those whom have access using a simple SSH button.

Read more on the GCP documentation [Here](https://cloud.google.com/compute/docs/instances/connecting-to-instance)






