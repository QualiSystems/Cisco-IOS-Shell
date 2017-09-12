from mock import patch
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails
from src.cisco_ios_resource_driver import CiscoIOSResourceDriver as ShellDriver

set_vlan = "setVlan"

request1 = """{
  "driverRequest" : {
    "actions" : [{
      "connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
      "connectionParams" : {
        "vlanId" : "45",
        "mode" : "Access",
        "vlanServiceAttributes" : [{
          "attributeName" : "QnQ",
          "attributeValue" : "True",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "CTag",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Isolation Level",
          "attributeValue" : "Shared",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Access Mode",
          "attributeValue" : "Access",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "VLAN ID",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Virtual Network",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Pool Name",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }
        ],
        "type" : "setVlanParameter"
      },
      "connectorAttributes" : [],
      "actionId" : "457238ad-4023-49cf-8943-219cb038c0dc_4244579e-bf6f-4d14-84f9-32d9cacaf9d9",
      "actionTarget" : {
        "fullName" : "2950/Chassis 0/FastEthernet0-23",
        "fullAddress" : "192.168.42.235/0/23",
        "type" : "actionTarget"
      },
      "customActionAttributes" : [],
      "type" : "removeVlan"
    }
    ]
  }
}"""

request2 = """{
  "driverRequest" : {
    "actions" : [{
      "connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
      "connectionParams" : {
        "vlanId" : "45",
        "mode" : "Access",
        "vlanServiceAttributes" : [{
          "attributeName" : "QnQ",
          "attributeValue" : "False",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "CTag",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Isolation Level",
          "attributeValue" : "Shared",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Access Mode",
          "attributeValue" : "Access",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "VLAN ID",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Virtual Network",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Pool Name",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }
        ],
        "type" : "setVlanParameter"
      },
      "connectorAttributes" : [],
      "actionId" : "457238ad-4023-49cf-8943-219cb038c0dc_4244579e-bf6f-4d14-84f9-32d9cacaf9d9",
      "actionTarget" : {
        "fullName" : "2950/Chassis 0/FastEthernet0-23",
        "fullAddress" : "192.168.42.235/0/23",
        "type" : "actionTarget"
      },
      "customActionAttributes" : [],
      "type" : "setVlan"
    }
    ]
  }
}"""

SHELL_NAME = ""
# SHELL_NAME = ""

address = '192.168.42.235'
user = 'root'
password = 'Password1'
enable_password = 'Password2'
auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
api_port = 8029

context = ResourceCommandContext()
context.resource = ResourceContextDetails()
context.resource.name = 'Test ios'
context.resource.fullname = 'Test ios'
context.resource.family = 'Switch'
context.reservation = ReservationContextDetails()
context.reservation.reservation_id = 'test_id'
context.resource.attributes = {}
context.resource.attributes['{}User'.format(SHELL_NAME)] = user
context.resource.attributes['{}Password'.format(SHELL_NAME)] = password
context.resource.attributes['{}host'.format(SHELL_NAME)] = "localhost"
context.resource.attributes['{}Enable Password'.format(SHELL_NAME)] = enable_password
# context.resource.attributes['Port'] = port
# context.resource.attributes['Backup Location'] = 'tftp://172.25.10.96/AireOS_test'
# context.resource.attributes['{}Backup Location'.format(SHELL_NAME)] = 'ftp://junos:junos@192.168.85.47'
# context.resource.attributes['{}Backup Location'.format(SHELL_NAME)] = 'ftp://user:pass@172.29.128.11'
context.resource.attributes['{}Backup Location'.format(SHELL_NAME)] = 'tftp://172.29.128.16'
context.resource.address = address
# context.connectivity = ConnectivityContext()
# context.connectivity.admin_auth_token = auth_key
# context.connectivity.server_address = '10.5.1.2'
# context.connectivity.cloudshell_api_port = api_port
context.resource.attributes['{}SNMP Version'.format(SHELL_NAME)] = '2'
context.resource.attributes['{}SNMP Read Community'.format(SHELL_NAME)] = 'Cisco'
context.resource.attributes['{}CLI Connection Type'.format(SHELL_NAME)] = 'auto'
# context.resource.attributes['{}CLI TCP Port'.format(SHELL_NAME)] = 17000
context.resource.attributes['{}Enable SNMP'.format(SHELL_NAME)] = 'True'
context.resource.attributes['{}Disable SNMP'.format(SHELL_NAME)] = 'False'
context.resource.attributes['{}Sessions Concurrency Limit'.format(SHELL_NAME)] = '1'


context.resource.attributes['{}Console Server IP Address'.format(SHELL_NAME)] = '192.168.42.166'
context.resource.attributes['{}Console User'.format(SHELL_NAME)] = ''
context.resource.attributes['{}Console Password'.format(SHELL_NAME)] = ''
context.resource.attributes['{}Console Port'.format(SHELL_NAME)] = 17000


if __name__ == '__main__':

    res = dict(context.resource.attributes)

    driver = ShellDriver()
    driver.initialize(context)

    with patch('src.cisco_ios_resource_driver.get_api') as get_api:
        api = type('api', (object,),
                   {'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()
        get_api.return_value = api
        # response = driver.get_inventory(context)
        # response = driver.health_check(context=context)
        response = driver.ApplyConnectivityChanges(context=context, request=request1)
        response = driver.ApplyConnectivityChanges(context=context, request=request2)
        # response = driver.run_custom_command(context=context, custom_command="show ver")
        # response = driver.save(context=context, folder_path="", configuration_type="running")
        # response = driver.save(context=context, folder_path="", configuration_type="startup")
        # response = driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-startup-300317-182734",
        #                           configuration_type="startup",
        #                           restore_method="override")
        # response = driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-startup-300317-182734",
        #                           configuration_type="startup",
        #                           restore_method="append")
        # response = driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-running-300317-182729",
        #                           configuration_type="running",
        #                           restore_method="override")
        # response = driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-running-300317-182729",
        #                           configuration_type="running",
        #                           restore_method="append")

        print response
        print "*"*20, "FINISH", "*"*20