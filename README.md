# Auto Upnp Mapping

This project implements a small upnp port mapping program.
It automatically adds port mapping based on configuration.

It is particularly useful if you are in a nested LAN, 
where you can access IGP router but your program does not know how to talk to it.
You still need to configure your local router for port forwarding though

It is designed to run in docker.

So far it only works with certain TP-Link router.

## Environment variables
**ROUTER_URL**: Url of router. eg. http://192.168.1.1

**PASSWORD**: The password for router. 
Note, use encrypted password here, capture it from the network tab, don't put plain text here.

**PORT_MAPPINGS**: A list of port mappings to be added. Format: {PORT}:{PROTOCOL}. 
Can take multiple values, comma separated. eg. 1234:TCP,5678:UDP