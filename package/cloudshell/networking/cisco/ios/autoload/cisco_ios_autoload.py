from cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload
from cloudshell.networking.cisco.ios.autoload.autoload_structure import GenericPort, GenericPortChannel, \
    CiscoIOSDevice, GenericChassis, GenericModule, GenericPowerPort


class CiscoIOSAutoload(CiscoGenericSNMPAutoload):
    def __init__(self, snmp_handler, logger, supported_os, resource_name):
        super(CiscoIOSAutoload, self).__init__(snmp_handler, logger, supported_os, resource_name)
        self.port = GenericPort
        self.power_port = GenericPowerPort
        self.port_channel = GenericPortChannel
        self.root_model = CiscoIOSDevice
        self.chassis = GenericChassis
        self.module = GenericModule
