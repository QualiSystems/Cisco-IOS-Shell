from unittest import TestCase

from mock import MagicMock

from cloudshell.networking.cisco.runners.cisco_configuration_runner import CiscoConfigurationRunner
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails


class TestCiscoConfigurationOperationsParameterValidation(TestCase):
    def _get_handler(self):
        self.output = """C6504e-1-CE7#copy running-config tftp:
        Address or name of remote host []? 10.10.10.10
        Destination filename [c6504e-1-ce7-confg]? 6504e1
        !!
        23518 bytes copied in 0.904 secs (26015 bytes/sec)
        C6504e-1-CE7#"""
        cli = MagicMock()
        session = MagicMock()
        session.send_command.return_value = self.output
        cliservice = MagicMock()
        cliservice.__enter__.return_value = session
        cli.get_session.return_value = cliservice
        #cli.return_value.get_session.return_value = session
        api = MagicMock()
        logger = MagicMock()
        context = ResourceCommandContext()
        context.resource = ResourceContextDetails()
        context.resource.name = 'resource_name'
        context.reservation = ReservationContextDetails()
        context.reservation.reservation_id = 'c3b410cb-70bd-4437-ae32-15ea17c33a74'
        context.resource.attributes = dict()
        context.resource.attributes['CLI Connection Type'] = 'Telnet'
        context.resource.attributes['Sessions Concurrency Limit'] = '1'
        return CiscoConfigurationRunner(cli=cli, logger=logger, api=api, context=context)

    def test_save_validates_source_filename_parameter(self):
        handler = self._get_handler()
        self.assertRaises(Exception, handler.save, 'tftp://10.10.10.10//////CloudShell/Configs/Gold/Test1/',
                          'runsning')

    def test_save_should_handle_source_filename_not_case_sensitive(self):
        handler = self._get_handler()
        self.assertIsNotNone(handler.save('tftp://10.10.10.10//////CloudShell/Configs/Gold/Test1/',
                                          'running'))
        self.assertIsNotNone(handler.save('tftp://10.10.10.10//////CloudShell/Configs/Gold/Test1/',
                                          'RUNNING'))

        # def test_save_validates_destination_host_host_parameter(self):
        #     handler = self._get_handler()
        #     handler.send_command_operations.send_command = MagicMock(return_value=self.output)
        #     self.assertRaises(Exception, handler.save, 'tftp://10.10.1as0.10//////CloudShell/Configs/Gold/Test1/',
        #                       'running')
        #     self.assertRaises(Exception, handler.save, 'tftp://10.10.1120.10//////CloudShell/Configs/Gold/Test1/',
        #                       'running')
        #     self.assertRaises(Exception, handler.save, 'tftp://10.10.10//////CloudShell/Configs/Gold/Test1/',
        #                       'running')
