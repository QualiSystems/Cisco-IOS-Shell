__author__ = 'CoYe'
# required import! Contains handler map
import cloudshell.networking.cisco.ios.resource_drivers
from cloudshell.shell.core.driver_builder_wrapper import DriverFunction
from cloudshell.networking.resource_driver.networking_generic_resource_dirver import networking_generic_resource_driver


class cisco_generic_ios_resource_driver(networking_generic_resource_driver):
    @DriverFunction(extraMatrixRows={"resource": ["ResourceAddress", "User", "Password", "Enable Password",
                                                  "Console Server IP Address",
                                                  "Console User", "Console Password", "Console Port", "Connection Type",
                                                  "SNMP Version", "SNMP Read Community", "SNMP V3 User",
                                                  "SNMP V3 Password", "SNMP V3 Private Key"]})
    def Init(self, matrixJSON):
        self.handler_name = 'ios'
        networking_generic_resource_driver.Init(self, matrixJSON)

if __name__ == '__main__':

    data_json = str("""{
            "resource" : {

                    "ResourceAddress": "192.168.42.235",
                    "User": "root",
                    "Password": "Password1",
                    "CLI Connection Type": "telnet",
                    "Console User": "",
                    "Console Password": "",
                    "Console Server IP Address": "",
                    "ResourceName" : "2950",
                    "ResourceFullName" : "2950",
                    "Enable Password": "",
                    "Console Port": "",
                    "SNMP Read Community": "Cisco",
                    "SNMP Version": "2",
                    "SNMP V3 Password": "",
                    "SNMP V3 User": "",
                    "SNMP V3 Private Key": ""
                },
            "reservation" : {
                    "Username" : "admin",
                    "Password" : "admin",
                    "Domain" : "Global",
                    "AdminUsername" : "admin",
                    "AdminPassword" : "admin"}
            }""")

    resource_driver = cisco_generic_ios_resource_driver('77', data_json)
    print resource_driver.GetInventory(data_json)
    #print resource_driver.Add_VLAN(data_json, '192.168.42.235/0/22', '55', 'trunk', '')
    #import sys; sys.exit()
    print resource_driver.SendCommand(data_json, 'sh ver')
    #print resource_driver.Save(data_json, 'tftp://192.168.65.85', 'startup-config')
    data_json = str("""{
            "resource" : {

                    "ResourceAddress": "192.168.42.235",
                    "User": "root",
                    "Password": "Password1",
                    "CLI Connection Type": "telnet",
                    "Console User": "",
                    "Console Password": "",
                    "Console Server IP Address": "",
                    "ResourceName" : "Cisco-2950-Router",
                    "ResourceFullName" : "Cisco-2950-Router",
                    "Enable Password": "",
                    "Console Port": "",
                    "SNMP Read Community": "Cisco",
                    "SNMP Version": "3",
                    "SNMP V3 Password": "Password1",
                    "SNMP V3 User": "QUALI",
                    "SNMP V3 Private Key": "Live4lol"
                }
            }""")

    #print resource_driver.Save(data_json, 'tftp://192.168.65.85', 'startup-config')
    print resource_driver.GetInventory(data_json)
    print resource_driver.SendCommand(data_json, 'sh ver')
    #print resource_driver.GetInventory(data_json)



