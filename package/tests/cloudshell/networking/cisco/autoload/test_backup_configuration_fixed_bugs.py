from unittest import TestCase
import re

from mock import MagicMock

from cloudshell.networking.cisco.runners.cisco_configuration_runner import CiscoConfigurationRunner
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails
from cloudshell.tests.networking.cisco.save_restore_methods.test_copy_output import TEST_COPY_OUTPUT


class TestCiscoConfigurationOperations(TestCase):
    def _get_handler(self, output):
        cli = MagicMock()
        session = MagicMock()
        session.send_command.return_value = output
        cliservice = MagicMock()
        cliservice.__enter__.return_value = session
        cli.get_session.return_value = cliservice
        # cli.return_value.get_session.return_value = session
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
        # output = '%Error opening tftp://10.10.10.10//CloudShell\n/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        output = '%Error opening tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        handler = self._get_handler(output)
        self.assertRaises(Exception, handler.save, 'tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/')

    def test_save_raises_exception_error_message(self):
        # output = '%Error opening tftp://10.10.10.10//CloudShell\n/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        output = '%Error opening tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/ASR1004-2-running-180516-101627 (Timed out)'
        handler = self._get_handler(output)
        try:
            handler.save('tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/')
        except Exception as e:
            self.assertIsNotNone(e)
            self.assertTrue(output.replace('%', '') in e[-1])

    def test_save_raises_exception_when_cannot_save_file_error_message(self):
        output = '''sw9003-vpp-10-3# copy running-config tftp://10.87.42.120
        Enter destination filename: [sw9003-vpp-10-3-running-config] 123123
        Enter vrf (If no input, current vrf 'default' is considered):
        Trying to connect to tftp server......
        Connection to Server Established.
        TFTP put operation failed:Access violation'''
        handler = self._get_handler(output)
        try:
            handler.save('tftp://10.10.10.10//CloudShell/Configs/Gold/Test1/')
        except Exception as e:
            self.assertIsNotNone(e)
            self.assertTrue('Copy Command failed. TFTP put operation failed:Access violation' in e[-1])

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

    def test_save_cisco_custom_output(self):
        resource_name = 'Very_long name with Spaces'
        config_type = 'running'
        output = """C6504e-1-CE7#copy running-config tftp:
        Address or name of remote host []? 10.10.10.10
        Destination filename [c6504e-1-ce7-confg]? 6504e1
        !!
        [OK - 1811552 bytes]
        1811552 bytes copied in 53.511 secs (34180 bytes/sec)
        C6504e-1-CE7#"""
        handler = self._get_handler(output)
        handler._resource_name = resource_name
        responce_template = '{0}-{1}-{2}'.format(resource_name.replace(' ', '_')[:23], config_type, '\d+\-\d+')
        responce = handler.save('tftp://10.10.10.10/CloudShell/Configs/Gold/Test1/',
                                config_type, 'management')
        self.assertIsNotNone(responce)
        self.assertTrue(re.search(responce_template, responce))

    def test_save_cisco_n6k_customer_report(self):
        resource_name = 'Very_long name with Spaces'
        config_type = 'running'
        output = TEST_COPY_OUTPUT.replace('Copy complete, now saving to disk (please wait)...', '')

        handler = self._get_handler(output)
        handler._resource_name = resource_name
        try:
            responce = handler.save('tftp://10.10.10.10/CloudShell/Configs/Gold/Test1/',
                                    config_type, 'management')
        except Exception as e:
            self.assertIsNotNone(e)
            self.assertTrue(e[-1] != '')

    def test_save_cisco_n6k_success_customer_report(self):
        resource_name = 'Very_long name with Spaces'
        config_type = 'running'
        output = TEST_COPY_OUTPUT
        self.output = output
        handler = self._get_handler(output)
        handler._resource_name = resource_name
        response_template = '{0}-{1}-{2}'.format(resource_name.replace(' ', '_')[:23], config_type, '\d+\-\d+')
        response = handler.save('tftp://10.10.10.10/CloudShell/Configs/Gold/Test1/',
                                config_type, 'management')
        self.assertIsNotNone(response)
        self.assertTrue(re.search(response_template, response))

    def test_orchestration_save_should_save_default_config(self):
        request = """
        {
            "custom_params": {
                "folder_path" : "tftp://10.0.0.1/folder1",
                "vrf_management_name": "network-1"
                }
        }"""
        handler = self._get_handler('Copy complete, now saving to disk (please wait)...')
        json_string = handler.orchestration_save(custom_params=request)
        print json_string

    def test_orchestration_restore_should_save_startup_config(self):
        request = """
        {"saved_artifacts_info": {"saved_artifact": {"artifact_type": "tftp", "identifier": "//10.0.0.1/folder1/resource_name-startup-281216-145700"}, "resource_name": "resource_name", "restore_rules": {"requires_same_resource": true}, "created_date": "2016-12-28T14:57:00.111000"}}"""
        handler = self._get_handler('Copy complete, now saving to disk (please wait)...')
        json_string = handler.orchestration_restore(saved_artifact_info=request)
        print json_string

    def test_orchestration_restore_should_save_default_config(self):
        request = """
        {"saved_artifacts_info": {"saved_artifact": {"artifact_type": "tftp", "identifier": "//10.0.0.1/folder1/resource_name-running-281216-145700"}, "resource_name": "resource_name", "restore_rules": {"requires_same_resource": true}, "created_date": "2016-12-28T14:57:00.111000"}}"""
        handler = self._get_handler('Copy complete, now saving to disk (please wait)...')
        json_string = handler.orchestration_restore(saved_artifact_info=request)
        print json_string