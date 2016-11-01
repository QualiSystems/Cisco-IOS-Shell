from threading import Thread

from cloudshell.networking.apply_connectivity.apply_connectivity_operation import apply_connectivity_changes
from cloudshell.networking.cisco.ios.autoload.cisco_autoload_operations import CiscoAutoloadOperations
from cloudshell.networking.cisco.cisco_firmware_operations import CiscoFirmwareOperations
from cloudshell.shell.core.context_utils import get_attribute_by_name
from cloudshell.networking.driver_helper import get_logger_with_thread_id, get_api, get_cli
from cloudshell.shell.core.context import ResourceContextDetails, ResourceCommandContext, ReservationContextDetails
from cloudshell.networking.cisco.cisco_configuration_operations import CiscoConfigurationOperations
from cloudshell.networking.cisco.cisco_connectivity_operations import CiscoConnectivityOperations
from cloudshell.networking.cisco.cisco_run_command_operations import CiscoRunCommandOperations
from cloudshell.networking.cisco.cisco_state_operations import CiscoStateOperations
from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_utils import GlobalLock


class CiscoIOSResourceDriver(ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock):
    SUPPORTED_OS = ["CAT[ -]?OS", "IOS[ -]?X?[ER]?"]

    def __init__(self):
        super(CiscoIOSResourceDriver, self).__init__()
        self._cli = None

    def initialize(self, context):
        """Initialize method
        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """

        session_pool_size = int(get_attribute_by_name(context=context, attribute_name='Sessions Concurrency Limit'))
        self._cli = get_cli(session_pool_size)
        return 'Finished initializing'

    def cleanup(self):
        pass

    def ApplyConnectivityChanges(self, context, request):

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        connectivity_operations = CiscoConnectivityOperations(cli=self._cli, context=context, api=api, logger=logger,
                                                              supported_os=self.SUPPORTED_OS)
        connectivity_operations.logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
        response = apply_connectivity_changes(request=request, logger=logger,
                                              add_vlan_action=connectivity_operations.add_vlan_action,
                                              remove_vlan_action=connectivity_operations.remove_vlan_action)
        connectivity_operations.logger.info('Finished applying connectivity changes, responce is: {0}'.format(str(
            response)))
        connectivity_operations.logger.info('Apply Connectivity changes completed')
        return response

    @GlobalLock.lock
    def restore(self, context, path, configuration_type, restore_method, vrf_management_name=None):
        """Restore selected file to the provided destination

        :param path: source config file
        :param configuration_type: running or startup configs
        :param restore_method: append or override methods
        :param vrf_management_name: VRF management Name
        """

        if not configuration_type:
            configuration_type = 'running'

        if not restore_method:
            restore_method = 'override'

        if not vrf_management_name:
            vrf_management_name = get_attribute_by_name(context=context, attribute_name='VRF Management Name')

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        configuration_operations = CiscoConfigurationOperations(logger=logger, api=api, cli=self._cli, context=context)
        logger.info('Restore started')
        response = configuration_operations.restore(path=path, restore_method=restore_method,
                                                    configuration_type=configuration_type,
                                                    vrf_management_name=vrf_management_name)
        logger.info('Restore completed')
        logger.info(response)

    def save(self, context, folder_path, configuration_type, vrf_management_name=None):
        """Save selected file to the provided destination

        :param configuration_type: source file, which will be saved
        :param folder_path: destination path where file will be saved
        :param vrf_management_name: VRF management Name
        """

        if not configuration_type:
            configuration_type = 'running'

        if not vrf_management_name:
            vrf_management_name = get_attribute_by_name(context=context, attribute_name='VRF Management Name')

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        configuration_operations = CiscoConfigurationOperations(logger=logger, api=api, cli=self._cli, context=context)
        logger.info('Save started')
        response = configuration_operations.save(folder_path, configuration_type, vrf_management_name)
        logger.info('Save completed')
        return response

    def orchestration_save(self, context, mode="shallow", custom_params=None):

        if not mode:
            mode = 'shallow'

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        configuration_operations = CiscoConfigurationOperations(logger=logger, api=api, cli=self._cli, context=context)
        logger.info('Orchestration save started')
        response = configuration_operations.orchestration_save(mode=mode, custom_params=custom_params)
        logger.info('Orchestration save completed')
        return response

    def orchestration_restore(self, context, saved_artifact_info, custom_params=None):
        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        configuration_operations = CiscoConfigurationOperations(logger=logger, api=api, cli=self._cli, context=context)
        logger.info('Orchestration restore started')
        configuration_operations.orchestration_restore(saved_artifact_info=saved_artifact_info,
                                                       custom_params=custom_params)
        logger.info('Orchestration restore completed')

    @GlobalLock.lock
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :return: response
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        autoload_operations = CiscoAutoloadOperations(cli=self._cli, logger=logger, context=context,
                                                      supported_os=self.SUPPORTED_OS)
        autoload_operations.logger.info('Autoload started')
        response = autoload_operations.discover()
        autoload_operations.logger.info('Autoload completed')
        return response

    @GlobalLock.lock
    def load_firmware(self, context, path, vrf_management_name=None):
        """Upload and updates firmware on the resource

        :param path: full path to firmware file, i.e. tftp://10.10.10.1/firmware.tar
        :param vrf_management_name: VRF management Name
        :return: result
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        if not vrf_management_name:
            vrf_management_name = get_attribute_by_name(context=context, attribute_name='VRF Management Name')

        logger.info('Start Load Firmware')
        firmware_operations = CiscoFirmwareOperations(cli=self._cli, logger=logger, context=context, api=api)
        response = firmware_operations.load_firmware(path=path, vrf_management_name=vrf_management_name)
        logger.info('Finish Load Firmware: {}'.format(response))

    def run_custom_command(self, context, custom_command):
        """Send custom command

        :return: result
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        response = send_command_operations.run_custom_command(custom_command=custom_command)
        return response

    def health_check(self, context):
        """Performs device health check

        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        state_operations = CiscoStateOperations(cli=self._cli, logger=logger, api=api, context=context)
        return state_operations.health_check()

    def run_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        result_str = send_command_operations.run_custom_config_command(custom_command=custom_command)
        return result_str

    @GlobalLock.lock
    def update_firmware(self, context, remote_host, file_path):
        """Upload and updates firmware on the resource

        :param remote_host: path to firmware file location on ftp or tftp server
        :param file_path: firmware file name
        :return: result
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        vrf_management_name = get_attribute_by_name(context=context, attribute_name='VRF Management Name')

        logger.info('Start Update Firmware')
        firmware_operations = CiscoFirmwareOperations(cli=self._cli, logger=logger, context=context, api=api)
        response = firmware_operations.load_firmware(path=remote_host, vrf_management_name=vrf_management_name)
        logger.info('Finish Update Firmware: {}'.format(response))

    def send_custom_command(self, context, custom_command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        response = send_command_operations.run_custom_command(custom_command=custom_command)
        return response

    def send_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        result_str = send_command_operations.run_custom_config_command(custom_command=custom_command)
        return result_str

    def shutdown(self, context):
        pass

if __name__ == '__main__':
    context = type('context', (object,), {'resource': type('resource', (object,), {'name': 'test name'})})
    tt = CiscoIOSResourceDriver()

    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'dsada'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = 'c3b410cb-70bd-4437-ae32-15ea17c33a74'
    context.resource.attributes = dict()
    context.resource.attributes['User'] = 'root'
    context.resource.attributes['SNMP Version'] = '2'
    context.resource.attributes['SNMP Read Community'] = 'quali'
    context.resource.attributes['Password'] = 'P0G8gOpDHL0c52ROLdsaVQ==' # 'NuCpFxP8cJMCic8ePJokug=='
    context.resource.attributes['Enable Password'] = 'NuCpFxP8cJMCic8ePJokug=='
    context.resource.attributes['Enable SNMP'] = 'True'
    context.resource.attributes['Disable SNMP'] = 'True'
    context.resource.attributes['CLI Connection Type'] = 'Telnet'
    context.resource.attributes['Sessions Concurrency Limit'] = '1'
    context.resource.attributes['CLI TCP Port'] = '23'
    context.resource.address = '192.168.42.235'
    context.resource.name = '2950'

    request = """{
    "driverRequest" : {
        "actions" : [{
                "connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
                "connectionParams" : {
                    "vlanId" : "450",
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
                            "attributeValue" : "45",
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

    tt.initialize(context)
    Thread(target=tt.health_check, args=(context, )).start()
    Thread(target=tt.ApplyConnectivityChanges, args=(context, request)).start()
    Thread(target=tt.get_inventory, args=(context, )).start()
    Thread(target=tt.save, args=(context, 'ftp://ftpuser:ftppass@192.168.65.39', '', '')).start()
    Thread(target=tt.send_custom_command, args=(context, 'show run')).start()
