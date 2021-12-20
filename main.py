import upnpclient
import os
import time
from luci import Luci

baseUrl = os.getenv('ROUTER_URL')
password = os.getenv('PASSWORD')
portMappings = []
for portMapping in os.getenv('PORT_MAPPINGS').split(','):
    tokens = portMapping.split(":")
    portMappings.append({
        "protocol": tokens[0].upper(),
        "port": tokens[1],
        "duration": tokens[2] if len(tokens) == 3 else '4294967295'
    })


def addPortMapping(host, mappings):
    d = upnpclient.Device(f'{baseUrl}:1900/rootDesc.xml')
    for mapping in mappings:
        try:
            d.WANIPConn1.AddPortMapping(
                NewRemoteHost='',
                NewExternalPort=mapping["port"],
                NewProtocol=mapping["protocol"],
                NewInternalPort=mapping["port"],
                NewInternalClient=host,
                NewEnabled='1',
                NewPortMappingDescription=None,
                NewLeaseDuration=mapping["duration"]
            )
            print(f'Mapping: port {mapping["port"]} protocol: {mapping["protocol"]} has been added.')
        except Exception as ex:
            print(f'Failed to add port mapping. {ex}')


luci = Luci(baseUrl, password)
while True:
    try:
        print("=================================================")
        luci.login()
        if not luci.isUpnpEnabled():
            luci.enableUpnp()
        ip = luci.getHostAddress()
        requireMapping = False
        for portMapping in portMappings:
            portLeased = luci.isPortLeased(ip,
                                           int(portMapping["port"]),
                                           tcp=portMapping["protocol"] == "TCP",
                                           udp=portMapping["protocol"] == "UDP")
            if not portLeased:
                print(f"Port: {portMapping['port']} Protocol: {portMapping['protocol']} is not mapped.")
            requireMapping = not portLeased or requireMapping
        if requireMapping:
            print('Disabling upnp...')
            luci.disableUpnp()
            print('Enabling upnp...')
            luci.enableUpnp()
            count = 0
            while count < 5:
                if luci.isUpnpEnabled():
                    break
                print(f"Upnp is not yet enabled. Waiting for enablement.")
                luci.enableUpnp()
                time.sleep(1)
            print('Upnp enabled')
            addPortMapping(ip, portMappings)
        else:
            print("All ports are mapped.")
    except Exception as ex:
        print(f'Unknown error occurred: {ex}')
    finally:
        time.sleep(30)
