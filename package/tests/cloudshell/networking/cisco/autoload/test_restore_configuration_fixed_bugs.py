from unittest import TestCase
import re

from mock import MagicMock

from cloudshell.networking.cisco.runners.cisco_configuration_runner import CiscoConfigurationRunner
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

__author__ = 'CoYe'

class TestCiscoHandlerBase(TestCase):
    def _get_handler(self, output):
        cli = MagicMock()
        session = MagicMock()
        session.send_command.return_value = output
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

    def test_save_raises_exception(self):
        #output = '%Error opening tftp://10.10.10.10//CloudShell\n/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        output = '%Error opening tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        handler = self._get_handler(output)
        self.assertRaises(Exception, handler.save, 'tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/',
                          'running')

    def test_save_raises_exception_error_message(self):
        # output = '%Error opening tftp://10.10.10.10//CloudShell\n/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        output = '%Error opening tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        handler = self._get_handler(output)
        try:
            handler.save('tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/', 'running')
        except Exception as e:
            self.assertIsNotNone(e)
            self.assertTrue(output.replace('%', '') in e[-1])

    def test_save_cisco_nexus_5k_customer_report(self):
        resource_name = 'Very_long name with Spaces'
        config_type = 'running'
        output = """N5K-L3-Sw1#
        N5K-L3-Sw1# copy running-config tftp:
        Enter destination filename: [N5K-L3-Sw1-running-config] N5K1
        Enter vrf (If no input, current vrf 'default' is considered): management
        Enter hostname for the tftp server: 10.10.10.10
        Trying to connect to tftp server......
        Connection to Server Established.

        [                         ]         0.50KB
        [#                        ]         4.50KB

         TFTP put operation was successful
         Copy complete, now saving to disk (please wait)...
         N5K-L3-Sw1#"""
        handler = self._get_handler(output)
        handler._resource_name = resource_name
        responce_template = '{0}-{1}-{2}'.format(resource_name.replace(' ', '_')[:23], config_type, '\d+\-\d+')
        responce = handler.save('tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/',
                                config_type, 'management')
        self.assertIsNotNone(responce)
        self.assertTrue(re.search(responce_template, responce))

    def test_save_cisco_nexus_6k_customer_report(self):
        resource_name = 'Very_long name with Spaces'
        config_type = 'running'
        output = """N6K-Sw1-S1# copy running-config tftp:
        Enter destination filename: [N6K-Sw1-S1-running-config] TestName
        Enter vrf (If no input, current vrf 'default' is considered): management
        Enter hostname for the tftp server: 10.10.10.10Trying to connect to tftp server......
        Connection to Server Established.

        [                         ]         0.50KB
        [#                        ]         4.50KB

         TFTP put operation was successful
         Copy complete, now saving to disk (please wait)...

        N6K-Sw1-S1#"""
        handler = self._get_handler(output)
        handler._resource_name = resource_name
        responce_template = '{0}-{1}-{2}'.format(resource_name.replace(' ', '_')[:23], config_type, '\d+\-\d+')
        responce = handler.save('tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/',
                                config_type, 'management')
        self.assertIsNotNone(responce)
        self.assertTrue(re.search(responce_template, responce))

    def test_save_cisco_asr_1k_no_error_customer_report(self):
        output = """ASR1004-2#copy running-config tftp:
        Address or name of remote host []?
        10.10.10.10
        Destination filename [asr1004-2-confg]?
        ASR1004-2-running-100516-084841
        .....
        %Error opening tftp://10.10.10.10/ASR1004-2-running-100516-084841 (Timed out)
        ASR1004-2#"""
        handler = self._get_handler(output)
        self.assertRaises(Exception, handler.save, 'tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/',
                          'running')

    def test_save_cisco_6504_customer_report(self):
        resource_name = 'Very_long name with Spaces'
        config_type = 'running'
        output = """C6504e-1-CE7#copy running-config tftp:
        Address or name of remote host []? 10.10.10.10
        Destination filename [c6504e-1-ce7-confg]? 6504e1
        !!
        23518 bytes copied in 0.904 secs (26015 bytes/sec)
        C6504e-1-CE7#"""
        handler = self._get_handler(output)
        handler._resource_name = resource_name
        responce_template = '{0}-{1}-{2}'.format(resource_name.replace(' ', '_')[:23], config_type, '\d+\-\d+')
        responce = handler.save('tftp://10.10.10.10/CloudShell/Configs/Gold/Test1/',
                                config_type, 'management')
        self.assertIsNotNone(responce)
        self.assertTrue(re.search(responce_template, responce))
