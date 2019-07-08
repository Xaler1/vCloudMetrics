import requests
import re
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vm import VM
from pyvcloud.vcd.vapp import VApp

class Connector():
    def connect(self, host, org, user, password):
        self.host = host
        self.org = org
        self.user = user
        self.password = password
        requests.packages.urllib3.disable_warnings()
        self.client = Client(host, verify_ssl_certs=False)
        self.client.set_highest_supported_version()
        self.client.set_credentials(BasicLoginCredentials(user, org, password))
    def getOrgs(self):
        self.orgs = self.client.get_org_list()
        org_names = []
        for org_resource in self.orgs:
            org_names.append(org_resource.get('name'))
        return org_names

    def getVDCs(self, org):
        self.orgs = self.client.get_org_list()
        VDCs = []
        found = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                found = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    VDCs.append(vdc_info['info'])
                    break
        if not found:
            print("Organisation with this name not found")



