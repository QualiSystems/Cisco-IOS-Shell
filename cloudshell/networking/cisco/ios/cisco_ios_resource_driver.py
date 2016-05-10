import inject

from cloudshell.shell.core.context.context_utils import context_from_args
from cloudshell.networking.cisco.ios.cisco_ios_bootstrap import CiscoIOSBootstrap
import cloudshell.networking.cisco.ios.cisco_ios_configuration as config


class CiscoIOSResourceDriver:
    def __init__(self):
        bootstrap = CiscoIOSBootstrap()
        bootstrap.add_config(config)
        bootstrap.initialize()

    @context_from_args
    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """
        return 'Finished initializing'

    def cleanup(self):
        pass

    @context_from_args
    def apply_connectivity_changes(self, context, request):
        handler = inject.instance('handler')
        responce = handler.apply_connectivity_changes(request)
        handler.logger.info('finished applying connectivity changes responce is:\n{0}'.format(str(responce)))
        return responce

    @context_from_args
    def restore(self, context, source_file, clear_config='override'):
        handler = inject.instance('handler')
        responce = handler.restore_configuration(source_file=source_file, clear_config=clear_config)
        handler.logger.info('Command completed')
        return responce

    @context_from_args
    def save(self, context, destination_host, source_filename):
        handler = inject.instance('handler')
        responce = handler.backup_configuration(destination_host, source_filename)
        return responce

    @context_from_args
    def get_inventory(self, context):
        """
        Return device structure with all standard attributes
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result = handler.discover_snmp()
        return result

    @context_from_args
    def load_firmware(self, context, remote_host, file_path):
        """
        Upload and updates firmware on the resource
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.update_firmware(remote_host=remote_host, file_path=file_path)
        handler.disconnect()
        handler.logger.info(result_str)

    @context_from_args
    def send_custom_command(self, context, command):
        """
        Send custom command
        :return: result
        :rtype: string
        """
        cli = inject.instance("cli_service")
        result_str = cli.send_command(command)
        return result_str

    @context_from_args
    def add_vlan(self, context, ports, vlan_range, port_mode, additional_info):
        """
        Assign vlan or vlan range to the certain interface
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.add_vlan(port_list=ports,
                                      vlan_range=vlan_range.replace(' ', ''),
                                      port_mode=port_mode,
                                      qnq=('qnq' in additional_info.lower()))
        handler.logger.info(result_str)

    @context_from_args
    def remove_vlan(self, context, ports, vlan_range, port_mode, additional_info):
        """
        Remove vlan or vlan range from the certain interface
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.remove_vlan(port_list=ports,
                                         vlan_range=vlan_range, port_mode=port_mode)
        handler.logger.info(result_str)

    @context_from_args
    def send_custom_config_command(self, context, command):
        handler = inject.instance("handler")
        result_str = handler.sendConfigCommand(cmd=command)
        return handler.normalize_output(result_str)

    @context_from_args
    def shutdown(self, context):
        pass
