# required import! Contains handler map
from cloudshell.shell.core.driver_builder_wrapper import DriverFunction
from cloudshell.networking.resource_driver.networking_generic_resource_driver import networking_generic_resource_driver


class cisco_generic_ios_resource_driver(networking_generic_resource_driver):
    @DriverFunction(extraMatrixRows={"resource": ["ResourceAddress", "User", "Password", "Enable Password",
                                                  "Console Server IP Address",
                                                  "Console User", "Console Password", "Console Port", "Connection Type",
                                                  "SNMP Version", "SNMP Read Community", "SNMP V3 User",
                                                  "SNMP V3 Password", "SNMP V3 Private Key"]})
    def Init(self, matrixJSON):
        self.handler_name = 'ios'
        networking_generic_resource_driver.Init(self, matrixJSON)


