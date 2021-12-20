import requests


class Luci:
    def __init__(self, baseUrl, password):
        self.baseUrl = baseUrl
        self.password = password
        self.stok = None
        self.serviceEp = None

    def login(self):
        try:
            self.getStok()
            return self.stok is not None
        except Exception as ex:
            raise Exception(f'Unknown error: {ex}')

    def getStok(self):
        payload = {"method": "do", "login": {"password": f"{self.password}"}}
        res = requests.post(self.baseUrl, json=payload).json()
        if res['error_code'] != 0:
            raise Exception(f'Failed to login. Error code: {res["error_code"]}, Raw response: {res}')
        self.stok = res["stok"]
        self.serviceEp = f'{self.baseUrl}/stok={res["stok"]}/ds'
        return res["stok"]

    def getHostAddress(self):
        try:
            payload = {"hosts_info": {"table": "host_info"}, "method": "get"}
            res = requests.post(self.serviceEp, json=payload).json()
            for host in res['hosts_info']['host_info']:
                for hostInfo in host:
                    hostInfo = host[hostInfo]
                    if hostInfo["is_cur_host"] == '1':
                        return hostInfo["ip"]
            return None
        except Exception as ex:
            raise Exception(f'Failed to get host address. {ex}')

    def isUpnpEnabled(self):
        try:
            payload = {"method": "get", "upnpd": {"name": "config"}}
            res = requests.post(self.serviceEp, json=payload).json()
            return res["upnpd"]["config"]["enable_upnp"] == "1"
        except Exception as ex:
            raise Exception(f'Failed to get upnp status. {ex}')

    def enableUpnp(self):
        try:
            payload = {"method": "set", "upnpd": {"config": {"enable_upnp": 1}}}
            res = requests.post(self.serviceEp, json=payload).json()
            if res["error_code"] != 0:
                raise Exception(f'Failed to enable upnp. {res}')
            return res["error_code"] == 0
        except Exception as ex:
            raise Exception(f'Unknown error occurred when enabling upnp. {ex}')

    def disableUpnp(self):
        try:
            payload = {"method": "set", "upnpd": {"config": {"enable_upnp": 0}}}
            res = requests.post(self.serviceEp, json=payload).json()
            if res["error_code"] != 0:
                raise Exception(f'Failed to disable upnp. {res}')
            return res["error_code"] == 0
        except Exception as ex:
            raise Exception(f'Unknown error occurred when disabling upnp. {ex}')

    def isPortLeased(self, ip, port, tcp=True, udp=True):
        try:
            payload = {"method": "get", "upnpd": {"name": "upnp_lease"}}
            res = requests.post(self.serviceEp, json=payload).json()
            if res["error_code"] != 0:
                raise Exception(f'Failed to get upnp lease. {res}')
            udpEnabled = not udp
            tcpEnabled = not tcp
            leases = res["upnpd"]["upnp_lease"]
            for lease in leases:
                for leaseInfo in lease:
                    leaseInfo = lease[leaseInfo]
                    if leaseInfo["client"] == ip and leaseInfo["inner_port"] == port and \
                            leaseInfo["ext_port"] == port and leaseInfo["enable"] == 1:
                        if leaseInfo["proto"] == 17:
                            udpEnabled = True
                        if leaseInfo["proto"] == 6:
                            tcpEnabled = True
            return udpEnabled and tcpEnabled
        except Exception as ex:
            raise Exception(f'Failed to get leasing info. {ex}')
