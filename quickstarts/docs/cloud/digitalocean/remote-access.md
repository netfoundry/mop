# Overview

  This guide will help you understand the cloud vendor specific rules and guideline for remotely accessing
  the "NetFoundry Zero Trust Network" image once it's instantiated.

{!common/ssh-authentication-important.md!}

{!common/root-ssh-disabled-important.md!}

# Digital Ocean Specifics

* Username Allowed: root
* Root Allowed: Yes - only user allowed.

The only way to access the digital ocean droplet is to ssh with the root user.  In order to access this remotely
you **must use ssh keys**.  If you choose to use a password instead of ssh keys, you will only be able to access this via the Digital Ocean console connection.

Read more on the Digital Ocean documentation:

[SSH Access](https://www.digitalocean.com/docs/droplets/how-to/connect-with-ssh/)

[Console Access](https://www.digitalocean.com/docs/droplets/resources/console/)