from unittest import TestCase

from cloudshell.networking.cisco.ios.autoload.autoload_structure import CiscoIOSDevice, GenericChassis, GenericModule, \
    GenericPort, GenericPortChannel, GenericPowerPort, GenericSubModule
from cloudshell.shell.core.driver_context import AutoLoadResource, AutoLoadAttribute


class CiscoAutoloadStructure(TestCase):

    def test_get_correct_attributes_names_of_root_element(self):
        root = CiscoIOSDevice()
        for attr in root.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)

    def test_get_correct_attributes_names_of_chassis_element(self):
        chassis = GenericChassis(name="Chassis 0", relative_address="0")
        self.assertIsInstance(chassis.get_resource(), AutoLoadResource)
        for attr in chassis.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)

    def test_get_correct_attributes_names_of_module_element(self):
        module = GenericModule(name="Module 0", relative_address="0/0")
        self.assertIsInstance(module.get_resource(), AutoLoadResource)
        for attr in module.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)

    def test_get_correct_attributes_names_of_Sub_module_element(self):
        module = GenericSubModule(name="Module 0", relative_address="0/0")
        self.assertIsInstance(module.get_resource(), AutoLoadResource)
        for attr in module.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)

    def test_get_correct_attributes_names_of_port_element(self):
        port = GenericPort(name="Ethernet 0/1", relative_address="0/0/1")
        self.assertIsInstance(port.get_resource(), AutoLoadResource)
        for attr in port.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)

    def test_get_correct_attributes_names_of_port_channel_element(self):
        port_channel = GenericPortChannel(name="PC 0", relative_address="PC1")
        self.assertIsInstance(port_channel.get_resource(), AutoLoadResource)
        for attr in port_channel.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)

    def test_get_correct_attributes_names_of_power_port_element(self):
        power_port = GenericPowerPort(name="PP 0", relative_address="0/PP1")
        self.assertIsInstance(power_port.get_resource(), AutoLoadResource)
        for attr in power_port.get_attributes():
            self.assertIsInstance(attr, AutoLoadAttribute)
