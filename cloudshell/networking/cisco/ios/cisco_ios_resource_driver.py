import inject

from cloudshell.shell.core.context.context_utils import context_from_args
from cloudshell.shell.core.driver_bootstrap import DriverBootstrap
import cloudshell.networking.cisco.ios.cisco_ios_configuration as config


class CiscoIOSResourceDriver:
    def __init__(self):
        bootstrap = DriverBootstrap()
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
    @inject.params(logger='logger', context='context', handler='handler')
    def simple_command(self, context, command, logger=None, handler=None):
        print(handler.send_command())
        logger.info('Command completed')
        return None

    @context_from_args
    def get_inventory(self, context):
        handler = inject.instance('handler')
        test = handler.discover_snmp()
        return test

