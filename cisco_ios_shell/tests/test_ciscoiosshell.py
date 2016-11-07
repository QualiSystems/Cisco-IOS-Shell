#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `CiscoiosshellDriver`
"""
from mock import MagicMock, patch, create_autospec

import cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload as cisco_generic_snmp_autoload
import cloudshell.networking.cisco.cisco_connectivity_operations as cisco_connectivity_operations
import cloudshell.networking.cisco.cisco_run_command_operations as cisco_run_command_operations
import cloudshell.networking.cisco.cisco_state_operations as cisco_state_operations
import unittest
from cloudshell.shell.core.context import ResourceCommandContext
import src.cisco_ios_resource_driver as driver
import cloudshell.networking.driver_helper as driver_helper


class TestCiscoIOSShellDriver(unittest.TestCase):
    CONTEXT = create_autospec(ResourceCommandContext, return_value=MagicMock())

    def setUp(self):
        self.driver = driver.CiscoIOSResourceDriver()

    # def test_initialize(self):
    #     # Act
    #     result = self.driver.initialize(self.CONTEXT)
    #     # Assert
    #     self.assertTrue(result, 'Finished initializing')

    # @patch.object(cisco_run_command_operations, 'CiscoRunCommandOperations')
    # def test_run_custom_command(self, mocked_class):
    #     # Arrange
    #     command = 'test command'
    #     response = 'response'
    #     mocked_class.return_value.run_custom_command.return_value = response
    #
    #     # Act
    #     result = self.driver.run_custom_command(self.CONTEXT, command)
    #
    #     # Assert
    #     self.assertTrue(response, result)
    #     mocked_class.return_value.run_custom_command.assert_called_with(custom_command=command)
    #
    # @patch.object(cisco_run_command_operations, 'CiscoRunCommandOperations')
    # def test_run_custom_config_command(self, mocked_class):
    #     # Arrange
    #     command = 'test command'
    #     response = 'response'
    #     mocked_class.return_value.run_custom_config_command.return_value = response
    #
    #     # Act
    #     result = self.driver.run_custom_config_command(self.CONTEXT, command)
    #
    #     # Assert
    #     self.assertTrue(response, result)
    #     mocked_class.return_value.run_custom_config_command.assert_called_with(custom_command=command)
    #
    # @patch.object(cisco_run_command_operations, 'CiscoRunCommandOperations')
    # def test_send_custom_command(self, mocked_class):
    #     # Arrange
    #     command = 'test command'
    #     response = 'response'
    #     mocked_class.return_value.run_custom_command.return_value = response
    #
    #     # Act
    #     result = self.driver.send_custom_command(self.CONTEXT, command)
    #
    #     # Assert
    #     self.assertTrue(response, result)
    #     mocked_class.return_value.run_custom_command.assert_called_with(custom_command=command)
    #
    # @patch.object(cisco_run_command_operations, 'CiscoRunCommandOperations')
    # def test_send_custom_config_command(self, mocked_class):
    #     # Arrange
    #     command = 'test command'
    #     response = 'response'
    #     mocked_class.return_value.run_custom_config_command.return_value = response
    #
    #     # Act
    #     result = self.driver.send_custom_config_command(self.CONTEXT, command)
    #
    #     # Assert
    #     self.assertTrue(response, result)
    #     mocked_class.return_value.run_custom_config_command.assert_called_with(custom_command=command)
    #
    # @patch.object(cisco_generic_snmp_autoload, 'CiscoGenericSNMPAutoload')
    # def test_get_inventory(self, mocked_class):
    #     # Arrange
    #     mocked_class.return_value.discover.return_value = ''
    #
    #     # Act
    #     self.driver.get_inventory(self.CONTEXT)
    #
    #     # Assert
    #     mocked_class.return_value.discover.assert_called()
    #
    # @patch.object(cisco_state_operations, 'CiscoStateOperations')
    # @patch('cloudshell.networking.driver_helper.get_logger_with_thread_id')
    # def test_health_check(self, mocked_class, logger):
    #     # Arrange
    #     logger.return_value = MagicMock()
    #     mocked_class.return_value.health_check.return_value = ''
    #
    #     # Act
    #     self.driver.health_check(self.CONTEXT)
    #
    #     # Assert
    #     mocked_class.return_value.health_check.assert_called()

    # @patch.object('cloudshell.networking.cisco.cisco_firmware_operations', 'CiscoFirmwareOperations')
    # def test_load_firmware(self, mocked_class):
    #     # Arrange
    #     path = 'test'
    #     vrf_management_name = 'response'
    #     mocked_class.return_value.load_firmware.return_value = ''
    #
    #     # Act
    #     self.driver.load_firmware(self.CONTEXT, path=path, vrf_management_name=vrf_management_name)
    #
    #     # Assert
    #     mocked_class.return_value.load_firmware.assert_called_with(path=path, vrf_management_name=vrf_management_name)

    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_load_firmware_no_vrf(self, mocked_class):
    #     # Arrange
    #     path = 'test'
    #     vrf_management_name = None
    #     mocked_class.return_value.load_firmware.return_value = ''
    #
    #     # Act
    #     self.driver.load_firmware(self.CONTEXT, path=path)
    #
    #     # Assert
    #     mocked_class.return_value.load_firmware.assert_called_with(path=path, vrf_management_name=vrf_management_name)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_update_firmware(self, mocked_class):
    #     # Arrange
    #     remote_host = 'test'
    #     file_path = 'response'
    #     mocked_class.return_value.load_firmware.return_value = ''
    #
    #     # Act
    #     self.driver.update_firmware(self.CONTEXT, remote_host=remote_host, file_path=file_path)
    #
    #     # Assert
    #     mocked_class.return_value.load_firmware.assert_called_with(path=remote_host)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_save_no_params(self, mocked_class):
    #     # Arrange
    #     mocked_class.return_value.save.return_value = ''
    #
    #     # Act
    #     self.driver.save(self.CONTEXT)
    #
    #     # Assert
    #     mocked_class.return_value.save.assert_called()
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_save_all_params(self, mocked_class):
    #     # Arrange
    #     folder_path = 'ftp://ftpuser:ftppass@server/folder'
    #     configuration_type = 'running'
    #     vrf_management_name = 'vrf'
    #
    #     mocked_class.return_value.save.return_value = ''
    #
    #     # Act
    #     self.driver.save(self.CONTEXT, folder_path=folder_path, configuration_type=configuration_type,
    #                      vrf_management_name=vrf_management_name)
    #
    #     # Assert
    #     mocked_class.return_value.save.assert_called_with(folder_path,
    #                                                       configuration_type,
    #                                                       vrf_management_name)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_save_all_params(self, mocked_class):
    #     # Arrange
    #     folder_path = 'ftp://ftpuser:ftppass@server/folder'
    #     configuration_type = 'running'
    #     vrf_management_name = 'vrf'
    #
    #     mocked_class.return_value.save.return_value = ''
    #
    #     # Act
    #     self.driver.save(self.CONTEXT, folder_path=folder_path, configuration_type=configuration_type,
    #                      vrf_management_name=vrf_management_name)
    #
    #     # Assert
    #     mocked_class.return_value.save.assert_called_with(folder_path,
    #                                                       configuration_type,
    #                                                       vrf_management_name)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_save_no_vrf(self, mocked_class):
    #     # Arrange
    #     folder_path = 'ftp://ftpuser:ftppass@server/folder'
    #     configuration_type = 'running'
    #
    #     mocked_class.return_value.save.return_value = ''
    #
    #     # Act
    #     self.driver.save(self.CONTEXT, folder_path=folder_path, configuration_type=configuration_type)
    #
    #     # Assert
    #     mocked_class.return_value.save.assert_called_with(folder_path,
    #                                                       configuration_type, None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_save_no_vrf_no_folder_path(self, mocked_class):
    #     # Arrange
    #     configuration_type = 'startup'
    #
    #     mocked_class.return_value.save.return_value = ''
    #
    #     # Act
    #     self.driver.save(self.CONTEXT, configuration_type=configuration_type)
    #
    #     # Assert
    #     mocked_class.return_value.save.assert_called_with('', configuration_type, None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_save_no_vrf_no_config_file(self, mocked_class):
    #     # Arrange
    #     folder_path = 'ftp://ftpuser:ftppass@server/folder'
    #
    #     mocked_class.return_value.save.return_value = ''
    #
    #     # Act
    #     self.driver.save(self.CONTEXT, folder_path=folder_path)
    #
    #     # Assert
    #     mocked_class.return_value.save.assert_called_with(folder_path,
    #                                                       'running', None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_restore_all_params(self, mocked_class):
    #     # Arrange
    #     path = 'ftp://ftpuser:ftppass@server/folder'
    #     configuration_type = 'startup'
    #     restore_method = 'append'
    #     vrf_management_name = 'vrf'
    #     mocked_class.return_value.restore.return_value = ''
    #
    #     # Act
    #     self.driver.restore(self.CONTEXT, path=path, configuration_type=configuration_type,
    #                         restore_method=restore_method, vrf_management_name=vrf_management_name)
    #
    #     # Assert
    #     mocked_class.return_value.restore.assert_called_with(path=path, configuration_type=configuration_type,
    #                                                          restore_method=restore_method,
    #                                                          vrf_management_name=vrf_management_name)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_restore_no_vrf(self, mocked_class):
    #     # Arrange
    #     path = 'ftp://ftpuser:ftppass@server/folder'
    #     configuration_type = 'startup'
    #     restore_method = 'append'
    #     mocked_class.return_value.restore.return_value = ''
    #
    #     # Act
    #     self.driver.restore(self.CONTEXT, path=path, configuration_type=configuration_type,
    #                         restore_method=restore_method)
    #
    #     # Assert
    #     mocked_class.return_value.restore.assert_called_with(path=path, configuration_type=configuration_type,
    #                                                          restore_method=restore_method, vrf_management_name=None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_restore_no_vrf_no_restore_method(self, mocked_class):
    #     # Arrange
    #     path = 'ftp://ftpuser:ftppass@server/folder'
    #     configuration_type = 'startup'
    #     mocked_class.return_value.restore.return_value = ''
    #
    #     # Act
    #     self.driver.restore(self.CONTEXT, path=path, configuration_type=configuration_type)
    #
    #     # Assert
    #     mocked_class.return_value.restore.assert_called_with(path=path, configuration_type=configuration_type,
    #                                                          restore_method='override', vrf_management_name=None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_restore_no_optional_params(self, mocked_class):
    #     # Arrange
    #     path = 'ftp://ftpuser:ftppass@server/folder'
    #     mocked_class.return_value.restore.return_value = ''
    #
    #     # Act
    #     self.driver.restore(self.CONTEXT, path=path)
    #
    #     # Assert
    #     mocked_class.return_value.restore.assert_called_with(path=path, configuration_type='running',
    #                                                          restore_method='override', vrf_management_name=None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_orchestration_save_no_optional_params(self, mocked_class):
    #     # Arrange
    #     mocked_class.return_value.orchestration_save.return_value = ''
    #
    #     # Act
    #     self.driver.orchestration_save(self.CONTEXT)
    #
    #     # Assert
    #     mocked_class.return_value.orchestration_save.assert_called_with(mode='shallow', custom_params=None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_orchestration_save(self, mocked_class):
    #     # Arrange
    #     mode = 'shallow'
    #     custom_params = 'test json'
    #     mocked_class.return_value.orchestration_save.return_value = ''
    #
    #     # Act
    #     self.driver.orchestration_save(self.CONTEXT, mode=mode, custom_params=custom_params)
    #
    #     # Assert
    #     mocked_class.return_value.orchestration_save.assert_called_with(mode=mode, custom_params=custom_params)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_orchestration_save_no_custom_params(self, mocked_class):
    #     # Arrange
    #     mocked_class.return_value.orchestration_save.return_value = ''
    #
    #     # Act
    #     self.driver.orchestration_save(self.CONTEXT, mode='shallow')
    #
    #     # Assert
    #     mocked_class.return_value.orchestration_save.assert_called_with(mode='shallow', custom_params=None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_orchestration_restore_no_custom_params(self, mocked_class):
    #     # Arrange
    #     saved_artifact_info = 'test json'
    #     mocked_class.return_value.orchestration_restore.return_value = ''
    #
    #     # Act
    #     self.driver.orchestration_restore(self.CONTEXT, saved_artifact_info)
    #
    #     # Assert
    #     mocked_class.return_value.orchestration_restore.assert_called_with(saved_artifact_info=saved_artifact_info,
    #                                                                        custom_params=None)
    #
    # @patch.object(cisco_nxos_configuration_operations, 'CiscoNXOSConfigurationOperations')
    # def test_orchestration_restore_all_params(self, mocked_class):
    #     # Arrange
    #     saved_artifact_info = 'test json'
    #     custom_params = 'test json'
    #     mocked_class.return_value.orchestration_restore.return_value = ''
    #
    #     # Act
    #     self.driver.orchestration_restore(self.CONTEXT, saved_artifact_info, custom_params)
    #
    #     # Assert
    #     mocked_class.return_value.orchestration_restore.assert_called_with(saved_artifact_info=saved_artifact_info,
    #                                                                        custom_params=custom_params)

    # @patch.object(cisco_connectivity_operations, 'CiscoConnectivityOperations')
    # def test_apply_connectivity_changes(self, mocked_class):
    #     # Arrange
    #     request = 'test json'
    #     mocked_class.return_value.apply_connectivity_changes.return_value = ''
    #
    #     # Act
    #     self.driver.ApplyConnectivityChanges(self.CONTEXT, request=request)
    #
    #     # Assert
    #     mocked_class.return_value.apply_connectivity_changes.assert_called_with(request)



if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
