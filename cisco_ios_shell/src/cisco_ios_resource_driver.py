from cloudshell.networking.apply_connectivity.apply_connectivity_operation import apply_connectivity_changes
from cloudshell.networking.cisco.ios.autoload.cisco_autoload_operations import CiscoAutoloadOperations
from cloudshell.networking.cisco.cisco_firmware_operations import CiscoFirmwareOperations
from cloudshell.networking.operations.connectivity_operations import serialize_connectivity_result
from cloudshell.shell.core.context_utils import get_attribute_by_name
from cloudshell.networking.driver_helper import get_logger_with_thread_id, get_api, get_cli
from cloudshell.shell.core.context import ResourceCommandContext
from cloudshell.networking.cisco.cisco_configuration_operations import CiscoConfigurationOperations
from cloudshell.networking.cisco.cisco_connectivity_operations import CiscoConnectivityOperations
from cloudshell.networking.cisco.cisco_run_command_operations import CiscoRunCommandOperations
from cloudshell.networking.cisco.cisco_state_operations import CiscoStateOperations
from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_utils import GlobalLock


class CiscoIOSResourceDriver(ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock):
    SUPPORTED_OS = ["CAT[ -]?OS", "IOS[ -]?X?[E]?"]

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
        """
        Create vlan and add or remove it to/from network interface

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param str request: request json
        :return:
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        connectivity_operations = CiscoConnectivityOperations(cli=self._cli, context=context, api=api, logger=logger,
                                                              supported_os=self.SUPPORTED_OS)
        logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
        result = apply_connectivity_changes(request=request, logger=logger,
                                            add_vlan_action=connectivity_operations.add_vlan_action,
                                            remove_vlan_action=connectivity_operations.remove_vlan_action)
        response = serialize_connectivity_result(result)
        logger.info('Finished applying connectivity changes, response is: {0}'.format(str(
            response)))
        logger.info('Apply Connectivity changes completed')

        return response

    @GlobalLock.lock
    def restore(self, context, path, configuration_type, restore_method, vrf_management_name=None):
        """Restore selected file to the provided destination

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
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

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param configuration_type: source file, which will be saved
        :param folder_path: destination path where file will be saved
        :param vrf_management_name: VRF management Name
        :return str saved configuration file name:
        """

        if not configuration_type:
            configuration_type = 'running'

        if not vrf_management_name:
            vrf_management_name = get_attribute_by_name(context=context, attribute_name='VRF Management Name')

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        configuration_operations = CiscoConfigurationOperations(logger=logger, api=api, cli=self._cli, context=context)
        logger.info('Save started')
        response = configuration_operations.save_configuration(folder_path, configuration_type, vrf_management_name)
        logger.info('Save completed')
        return response

    def orchestration_save(self, context, mode="shallow", custom_params=None):
        """

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param mode: mode
        :param custom_params: json with custom save parameters
        :return str response: response json
        """

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
        """

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param saved_artifact_info: OrchestrationSavedArtifactInfo json
        :param custom_params: json with custom restore parameters
        """

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

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: response
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        autoload_operations = CiscoAutoloadOperations(cli=self._cli, logger=logger, context=context,
                                                      supported_os=self.SUPPORTED_OS)
        logger.info('Autoload started')
        response = autoload_operations.discover()
        logger.info('Autoload completed')
        return response

    @GlobalLock.lock
    def load_firmware(self, context, path, vrf_management_name=None):
        """Upload and updates firmware on the resource

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param path: full path to firmware file, i.e. tftp://10.10.10.1/firmware.tar
        :param vrf_management_name: VRF management Name
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

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: result
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        response = send_command_operations.run_custom_command(custom_command=custom_command)
        return response

    def health_check(self, context):
        """Performs device health check

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: Success or Error message
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        state_operations = CiscoStateOperations(cli=self._cli, logger=logger, api=api, context=context)
        return state_operations.health_check()

    def run_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: result
        :rtype: str
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
        :rtype: str
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

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: result
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        response = send_command_operations.run_custom_command(custom_command=custom_command)
        return response

    def send_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: result
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        send_command_operations = CiscoRunCommandOperations(cli=self._cli, logger=logger, context=context, api=api)
        result_str = send_command_operations.run_custom_config_command(custom_command=custom_command)
        return result_str

    def shutdown(self, context):
        pass
