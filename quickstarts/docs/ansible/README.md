# Ansible Roles for Jenkins Pipelines

Created for Regression Testing of NetFoundry Features, e.g. AVW VPN Sit Creation, Ziti Edge Developer Edition Image.
1. AVW VPN Site Testing Specific Roles:
    1. customer-router: simulating a customer router that would peer with NF gateway acting as a AVW VPN Site in a Customer Branch DC
    1. frr - a role that configures BGP Routing Agent on the simulated customer router.
    1. test-case-01 - test cases that verify that AVW VPN Site Creation through NF MOP Console works as expected.
1. ZEDE Specific Roles
    1. zede-client: simulating a client endpoint where a Ziti Tunneler is run
    1. zede: VM created from ZEDE image
    1. zede-tc-01: test cases to verify that the ZEDE image was build successfully.
1. Shared Roles
    1. app-server: simulating a server where the app is run, e.g. webserver, iperf3 performance tool
