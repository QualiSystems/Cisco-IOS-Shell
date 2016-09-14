import threading
from cloudshell.networking.cisco.ios.cisco_ios_resource_driver import CiscoIOSResourceDriver
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, \
    ReservationContextDetails
from cloudshell.shell.core.driver_context import ConnectivityContext


class DriverCommandExecution(threading.Thread):
    def __init__(self, driver_instance, command_name, parameters_name_value_map):
        threading.Thread.__init__(self)

        self._parameters_name_value_map = parameters_name_value_map
        self._driver_instance = driver_instance
        self._command_name = command_name
        # self._cancellation_context = CancellationContext()

    def run(self):
        self._result = self._driver_instance.invoke_func(self._command_name,
                                                         self._parameters_name_value_map)

    def set_cancellation_context(self):
        # self._cancellation_context.is_cancelled = True
        pass

    def get_result(self):
        return self._result


class DriverWrapper:
    def __init__(self, obj):
        self.instance = obj

    def invoke_func(self, command_name, params):
        func = getattr(self.instance, command_name)

        return func(**params)


tt = CiscoIOSResourceDriver()

context = ResourceCommandContext()
context.resource = ResourceContextDetails()
context.resource.name = 'ASR9k'
context.reservation = ReservationContextDetails()
context.reservation.reservation_id = 'c3b410cb-70bd-4437-ae32-15ea17c33a74'
context.reservation.domain = 'Global'
context.connectivity = ConnectivityContext
context.connectivity.server_address = 'localhost'
context.connectivity.cloudshell_api_port = 8029
context.resource.attributes = dict()
context.resource.attributes['User'] = 'root'
context.resource.attributes['SNMP Version'] = '2'
context.resource.attributes['SNMP Read Community'] = 'Cisco'
context.resource.attributes['Password'] = 'P0G8gOpDHL0c52ROLdsaVQ=='  # 'NuCpFxP8cJMCic8ePJokug=='  #
context.resource.attributes['Enable Password'] = 'NuCpFxP8cJMCic8ePJokug=='
context.resource.attributes['CLI Connection Type'] = 'ssh'
context.resource.attributes['CLI TCP Port'] = '0'
context.resource.address = '192.168.42.235'
request1 = """{
	"driverRequest" : {
		"actions" : [{
				"connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
				"connectionParams" : {
					"vlanId" : "406",
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
							"attributeValue" : "46",
							"type" : "vlanServiceAttribute"
						}, {
							"attributeName" : "Virtual Network",
							"attributeValue" : "45",
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

request2 = """{
	"driverRequest" : {
		"actions" : [{
				"connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
				"connectionParams" : {
					"vlanId" : "46",
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
							"attributeValue" : "46",
							"type" : "vlanServiceAttribute"
						}, {
							"attributeName" : "Virtual Network",
							"attributeValue" : "45",
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


class MyThread(threading.Thread):
    def __del__(self):
        print('Delete Thread: ' + self.getName())

# , 'tftp://192.168.65.47', 'running'
# apply_connectivity_changes
# MyThread(target=tt.health_check, args=[context]).start()
# MyThread(target=tt.ApplyConnectivityChanges, args=[context, request1]).start()
MyThread(target=tt.run_custom_command, args=[context, 'sh run']).start()
MyThread(target=tt.run_custom_config_command, args=[context, 'do sh ver']).start()

MyThread(target=tt.save, args=[context, 'ftp://ftpuser:ftppass@192.168.65.74', 'running']).start()
MyThread(target=tt.get_inventory, args=[context]).start()
# MyThread(target=tt.ApplyConnectivityChanges, args=[context, request2]).start()
# MyThread(target=tt.restore, args=[context, 'ftp://ftpuser:ftppass@192.168.65.74/2950-running-160816-144710', 'running', 'append']).start()
