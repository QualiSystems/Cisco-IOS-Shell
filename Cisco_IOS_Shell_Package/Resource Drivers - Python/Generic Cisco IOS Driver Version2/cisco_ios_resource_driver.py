from cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload
from cloudshell.networking.cisco.cisco_configuration_operations import CiscoConfigurationOperations
from cloudshell.networking.cisco.cisco_connectivity_operations import CiscoConnectivityOperations
from cloudshell.networking.cisco.cisco_send_command_operations import CiscoSendCommandOperations
from cloudshell.networking.cisco.cisco_state_operations import CiscoStateOperations

from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.context_utils import context_from_args
from cloudshell.shell.core.driver_bootstrap import DriverBootstrap
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_utils import GlobalLock

import cloudshell.networking.cisco.ios.cisco_ios_configuration as driver_config


class CiscoIOSResourceDriver(ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock):
    def __init__(self):
        super(CiscoIOSResourceDriver, self).__init__()
        bootstrap = DriverBootstrap()
        bootstrap.add_config(driver_config)
        bootstrap.initialize()

    @context_from_args
    def initialize(self, context):
        """Initialize method
        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """

        return 'Finished initializing'

    def cleanup(self):
        pass

    @context_from_args
    def ApplyConnectivityChanges(self, context, request):
        connectivity_operations = CiscoConnectivityOperations()
        connectivity_operations.logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
        response = connectivity_operations.apply_connectivity_changes(request)
        connectivity_operations.logger.info('Finished applying connectivity changes, responce is: {0}'.format(str(
            response)))
        connectivity_operations.logger.info('Apply Connectivity changes completed')
        return response

    @GlobalLock.lock
    @context_from_args
    def restore(self, context, path, configuration_type='running', restore_method='override', vrf_management_name=None):
        """Restore selected file to the provided destination

        :param path: source config file
        :param configuration_type: running or startup configs
        :param restore_method: append or override methods
        :param vrf_management_name: VRF management Name
        """

        configuration_operations = CiscoConfigurationOperations()
        response = configuration_operations.restore(path=path, restore_method=restore_method,
                                                    configuration_type=configuration_type,
                                                    vrf_management_name=vrf_management_name)
        configuration_operations.logger.info('Restore completed')
        configuration_operations.logger.info(response)

    @context_from_args
    def save(self, context, folder_path, configuration_type, vrf_management_name=None):
        """Save selected file to the provided destination

        :param configuration_type: source file, which will be saved
        :param folder_path: destination path where file will be saved
        :param vrf_management_name: VRF management Name
        """

        configuration_operations = CiscoConfigurationOperations()
        response = configuration_operations.save(folder_path, configuration_type, vrf_management_name)
        configuration_operations.logger.info('Save completed')
        return response

    @context_from_args
    def orchestration_save(self, context, mode="shallow", custom_params=None):
        configuration_operations = CiscoConfigurationOperations()
        configuration_operations.logger.info('Orchestration save started')
        response = configuration_operations.orchestration_save(mode=mode, custom_params=custom_params)
        configuration_operations.logger.info('Orchestration save completed')
        return response

    @context_from_args
    def orchestration_restore(self, context, saved_artifact_info, custom_params=None):
        configuration_operations = CiscoConfigurationOperations()
        configuration_operations.logger.info('Orchestration restore started')
        configuration_operations.orchestration_restore(saved_artifact_info=saved_artifact_info,
                                                       custom_params=custom_params)
        configuration_operations.logger.info('Orchestration restore completed')

    @context_from_args
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :return: response
        :rtype: string
        """

        autoload_operations = CiscoGenericSNMPAutoload()
        autoload_operations.logger.info('Autoload started')
        response = autoload_operations.discover()
        autoload_operations.logger.info('Autoload completed')
        return response

    @GlobalLock.lock
    @context_from_args
    def load_firmware(self, context, path, vrf_management_name=None):
        """Upload and updates firmware on the resource

        :param path: full path to firmware file, i.e. tftp://10.10.10.1/firmware.tar
        :param vrf_management_name: VRF management Name
        :return: result
        :rtype: string
        """

        firmware_operations = CiscoConfigurationOperations()
        response = firmware_operations.load_firmware(path=path, vrf_management_name=vrf_management_name)
        firmware_operations.logger.info(response)

    @context_from_args
    def run_custom_command(self, context, custom_command):
        """Send custom command

        :return: result
        :rtype: string
        """

        send_command_operations = CiscoSendCommandOperations()
        response = send_command_operations.send_command(command=custom_command)
        return response

    @context_from_args
    def health_check(self, context):
        """Performs device health check

        """

        state_operations = CiscoStateOperations()
        return state_operations.health_check()

    @context_from_args
    def run_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """
        send_command_operations = CiscoSendCommandOperations()
        result_str = send_command_operations.send_config_command(command=custom_command)
        return result_str

    @GlobalLock.lock
    @context_from_args
    def update_firmware(self, context, remote_host, file_path):
        """Upload and updates firmware on the resource

        :param remote_host: path to firmware file location on ftp or tftp server
        :param file_path: firmware file name
        :return: result
        :rtype: string
        """

        firmware_operations = CiscoConfigurationOperations()
        response = firmware_operations.load_firmware(path=remote_host)
        firmware_operations.logger.info(response)

    @context_from_args
    def shutdown(self, context):
        pass
