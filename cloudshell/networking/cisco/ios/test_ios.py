import threading

from cloudshell.networking.cisco.ios.cisco_ios_resource_driver import CiscoIOSResourceDriver
from cloudshell.shell.core.context.context import ResourceCommandContext, ResourceContextDetails, \
    ReservationContextDetails

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
context.resource.name = 'dsada'
context.reservation = ReservationContextDetails()
context.reservation.reservation_id = 'test_id'
context.resource.attributes = {}
context.resource.attributes['user'] = 'root'
context.resource.attributes['SNMP Version'] = '2'
context.resource.attributes['SNMP Read Community'] = 'Cisco'
context.resource.attributes['password'] = 'Password1'
context.resource.attributes['ResourceAddress'] = '192.168.42.235'

class MyThread(threading.Thread):

    def __del__(self):
        print('Delete Thread: '+self.getName())

MyThread(target=tt.get_inventory, args=[context]).start()
#MyThread(target=tt.simple_command, args=[context, '10']).start()
#MyThread(target=tt.simple_command, args=[context, '10']).start()