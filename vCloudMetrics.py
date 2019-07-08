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
        else:
            return(VDCs)

    def getVMs(self, org, orgVDC):
        self.orgs = self.client.get_org_list()
        VMs = []
        orgfound = False
        vdcfound = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                orgfound = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    if vdc_info['name'] == orgVDC:
                        vdcfound = True
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        for resource in vdc.list_resources(EntityType.VAPP):
                            vapp = VApp(self.client, resource=vdc.get_vapp(resource['name']))
                            for vm_info in vapp.get_all_vms():
                                name_vm = vm_info.get('name')
        if not orgfound:
            print("Organisation with this name not found")
        elif not vdcfound:
            print("VDC not found")
        else:
            return VMs

    def getCPUUsedByOrg(self, org):
        self.orgs = self.client.get_org_list()
        CPUUsed = 0
        found = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                found = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                    vdc_xml = vdc.get_resource()
                    CPUUsed += vdc_xml.ComputeCapacity.Cpu.Used
                    break
        if not found:
            print("Organisation with this name not found")
            return 0
        else:
            return CPUUsed

    def getCPUMHzByOrg(self, org):
            self.orgs = self.client.get_org_list()
            CPUMHz= 0
            found = False
            for org_resource in self.orgs:
                name = org_resource.get('name')
                if name == org:
                    found = True
                    org = Org(self.client, resource=org_resource)
                    for vdc_info in org:
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        vdc_xml = vdc.get_resource()
                        CPUMHz += vdc_xml.VCpuInMhz2
                        break
            if not found:
                print("Organisation with this name not found")
                return 0
            else:
                return CPUMHz

    def getCPULimitByOrg(self, org):
        self.orgs = self.client.get_org_list()
        CPULimit = 0
        found = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                found = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                    vdc_xml = vdc.get_resource()
                    CPULimit += vdc_xml.ComputeCapacity.Cpu.Limit
                    break
        if not found:
            print("Organisation with this name not found")
            return 0
        else:
            return CPULimit

    def getMemoryUsedByOrg(self, org):
        self.orgs = self.client.get_org_list()
        MemoryUsed = 0
        found = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                found = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                    vdc_xml = vdc.get_resource()
                    MemoryUsed += vdc_xml.ComputeCapacity.Memory.Used
                    break
        if not found:
            print("Organisation with this name not found")
            return 0
        else:
            return MemoryUsed

    def getMemoryLimitByOrg(self, org):
        self.orgs = self.client.get_org_list()
        MemoryLimit = 0
        found = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                found = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                    vdc_xml = vdc.get_resource()
                    MemoryLimit += vdc_xml.ComputeCapacity.Memory.Limit
                    break
        if not found:
            print("Organisation with this name not found")
            return 0
        else:
            return MemoryLimit


###########################################################################################################################################

    def getCPUUsedByVDC(self, org, orgVDC):
        self.orgs = self.client.get_org_list()
        orgfound = False
        vdcfound = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                orgfound = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    if vdc_info['name'] == orgVDC:
                        vdcfound = True
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        vdc_xml = vdc.get_resource()
                        CPUUsed = vdc_xml.ComputeCapacity.Cpu.Used
                    break
        if not orgfound:
            print("Organisation with this name not found")
            return 0
        elif not vdcfound:
            print("VDC with this name not found")
            return 0
        else:
            return CPUUsed

    def getCPUMHzByVDC(self, org, orgVDC):
        self.orgs = self.client.get_org_list()
        orgfound = False
        vdcfound = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                orgfound = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    if vdc_info['name'] == orgVDC:
                        vdcfound = True
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        vdc_xml = vdc.get_resource()
                        CPUMHz = vdc_xml.VCpuInMhz2
                    break
        if not orgfound:
            print("Organisation with this name not found")
            return 0
        elif not vdcfound:
            print("VDC with this name not found")
            return 0
        else:
            return CPUMHz

    def getCPULimitByVDC(self, org, orgVDC):
        self.orgs = self.client.get_org_list()
        orgfound = False
        vdcfound = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                orgfound = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    if vdc_info['name'] == orgVDC:
                        vdcfound = True
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        vdc_xml = vdc.get_resource()
                        CPULimit = vdc_xml.ComputeCapacity.Cpu.Limit
                    break
        if not orgfound:
            print("Organisation with this name not found")
            return 0
        elif not vdcfound:
            print("VDC with this name not found")
            return 0
        else:
            return CPULimit

    def getMemoryUsedByVDC(self, org, orgVDC):
        self.orgs = self.client.get_org_list()
        orgfound = False
        vdcfound = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                orgfound = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    if vdc_info['name'] == orgVDC:
                        vdcfound = True
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        vdc_xml = vdc.get_resource()
                        MemoryUsed = vdc_xml.ComputeCapacity.Memory.Used
                    break
        if not orgfound:
            print("Organisation with this name not found")
            return 0
        elif not vdcfound:
            print("VDC with this name not found")
            return 0
        else:
            return MemoryUsed

    def getMemoryLimitByVDC(self, org, orgVDC):
        self.orgs = self.client.get_org_list()
        orgfound = False
        vdcfound = False
        for org_resource in self.orgs:
            name = org_resource.get('name')
            if name == org:
                orgfound = True
                org = Org(self.client, resource=org_resource)
                for vdc_info in org:
                    if vdc_info['name'] == orgVDC:
                        vdcfound = True
                        vdc = VDC(self.client, resource=org.get_vdc(vdc_info['name']))
                        vdc_xml = vdc.get_resource()
                        MemoryLimit = vdc_xml.ComputeCapacity.Memory.Limit
                    break
        if not orgfound:
            print("Organisation with this name not found")
            return 0
        elif not vdcfound:
            print("VDC with this name not found")
            return 0
        else:
            return MemoryLimit