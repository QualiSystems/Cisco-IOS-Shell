__author__ = 'g8y3e'

import re
import time
import ipcalc
import socket

from cloudshell.networking.cisco.cisco_os import CiscoOS

from cloudshell.networking.utils import *
from cloudshell.networking.cisco.cisco_network_interfaces.ethernet import Ethernet
from cloudshell.networking.cisco.cisco_autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload
from cloudshell.networking.cisco.ios.firmware_data.cisco_firmware_data import CiscoFirmwareData
from cloudshell.cli import expected_actions
from cloudshell.api.cloudshell_api import CloudShellAPISession

class CiscoIOS(CiscoOS):
    DEFAULT_PROMPT = '.*> *$'
    ENABLE_PROMPT = '.*# *$'
    CONFIG_MODE_PROMPT = '\(config.*\)# *$'
    ERR_STR = 'Invalid input detected|Incomplete command.'
    SPACE = '<QS_SP>'
    RETURN = '<QS_CR>'
    NEWLINE = '<QS_LF>'

    def __init__(self, connection_manager, logger):
        CiscoOS.__init__(self, connection_manager, logger)
        self.supported_os = ['IOS', 'IOS-XE', 'CATOS']
        self._prompt = "{0}|{1}|{2}".format(self.DEFAULT_PROMPT, self.ENABLE_PROMPT, self.CONFIG_MODE_PROMPT)
        self._snmp_handler = None
        self._cloud_shell_api = None

    @property
    def snmp_handler(self):
        if not self._snmp_handler:
            self.create_snmp_handler()
        return self._snmp_handler

    @snmp_handler.setter
    def snmp_handler(self, hsnmp):
        self._snmp_handler = hsnmp

    def _defaultActions(self):
        """Send default commands to configure/clear session outputs
        :return:
        """
        self._session.setUnsafeMode(True)

        output = self._send_command('')

        if re.search('> *$', output):
            output = self._send_command('enable',
                                        expected_map={'[Pp]assword': expected_actions.send_default_password})

        if re.search('> *$', output):
            raise Exception('Cisco IOSX', "Can't set enable mode!")

        self._set_terminal_length(0)
        self._send_command('terminal no exec prompt timestamp')

        self._enter_configuration_mode()
        self._send_command('no logging console')
        self._exit_configuration_mode()

    def _set_terminal_length(self, length):
        return self._send_command('terminal length {0}'.format(length))

    def _show_ommand(self, data):
        return self._send_command('show {0}'.format(data))

    def _enter_configuration_mode(self):
        """Send 'enter' to SSH console to get prompt,
        if default prompt received , send 'configure terminal' command, change _prompt to CONFIG_MODE
        else: return

        :return: True if config mode entered, else - False
        """
        if not self._get_session_handler():
            self.connect()

        if self._session.__class__.__name__ == 'FileManager':
            return ''

        out = None
        for retry in range(3):
            out = self._send_command(' ')
            if not out:
                self._logger.error('Failed to get prompt, retrying ...')
                time.sleep(1)

            elif not re.search(self.CONFIG_MODE_PROMPT, out):
                out = self._send_command('configure terminal', self.CONFIG_MODE_PROMPT)

            else:
                break

        if not out:
            return False
        return re.search(self._prompt, out)

    def _exit_configuration_mode(self):
        """Send 'enter' to SSH console to get prompt,
        if config prompt received , send 'exit' command, change _prompt to DEFAULT
        else: return

        :return: console output
        """

        if not self._get_session_handler():
            self.connect()

        if self._session.__class__.__name__ == 'FileManager':
            return ''

        out = None
        for retry in range(5):
            out = self._send_command(' ')
            if re.search(self.CONFIG_MODE_PROMPT, out):
                self._send_command('exit')
            else:
                break

        return out

    def send_config_command(self, cmd, expected_str=None, timeout=30):
        """Send command into configuration mode, enter to config mode if needed

        :param cmd: command to send
        :param expected_str: expected output string (_prompt by default)
        :param timeout: command timeout
        :return: received output buffer
        """

        self._enter_configuration_mode()

        if expected_str is None:
            expected_str = self._prompt

        out = self._send_command(command=cmd, expected_str=expected_str, timeout=timeout, is_need_default_prompt=False)
        self._logger.info(out)
        return out

    def send_command(self, cmd, expected_str=None, timeout=30):
        """Send command into default mode, exit config mode if needed

        :param cmd: command to send
        :param expected_str: expected output string (_prompt by default)
        :param timeout: command timeout
        :return: received output buffer
        """

        self._exit_configuration_mode()

        if expected_str is None:
            expected_str = self._prompt

        out = self._send_command(command=cmd, expected_str=expected_str, timeout=timeout, is_need_default_prompt=False)
        self._logger.info(out)
        return out

    def send_commands_list(self, commands_list):
        for command in commands_list:
            self.send_config_command(command)

    def normalize_output(self, output):
        return output.replace(' ', self.SPACE).replace('\r\n', self.NEWLINE).replace('\n', self.NEWLINE).\
            replace('\r', self.NEWLINE)

    def _check_download_from_tftp(self, output):
        status_match = re.search('\[OK - [0-9]* bytes\]', output)
        is_success = (status_match is not None)
        message = ''
        if not is_success:
            match_error = re.search('%', output, re.IGNORECASE)
            if match_error:
                message = output[match_error.end():]
                message = message.split('\n')[0]
            else:
                is_success = True

        return is_success, message

    def _is_valid_copy_filesystem(self, filesystem):
        return not re.match('bootflash$|tftp$|ftp$|harddisk$|nvram$|pram$|flash$|localhost$', filesystem) is None

    def copy(self, source_filesystem='', destination_filesystem='', timeout=30, retries=5, **kwargs):
        if len(source_filesystem) != 0 and not self._is_valid_copy_filesystem(source_filesystem):
            raise Exception('Cisco IOS', 'Copy method: source filesystem \"' + source_filesystem \
                            + '\" is incorrect!')

        if len(destination_filesystem) != 0 and not self._is_valid_copy_filesystem(destination_filesystem):
            raise Exception('Cisco IOS', 'Copy method: destination filesystem \"' + destination_filesystem \
                            + '\" is incorrect!')

        if 'source_filename' not in kwargs or len(kwargs['source_filename']) == 0:
            raise Exception('Cisco IOS', 'Copy method: source filename not set!')

        if source_filesystem != '':
            source_filesystem += ': '
        else:
            source_filesystem = kwargs['source_filename'] + ' '

        if destination_filesystem != '':
            destination_filesystem += ':'
        else:
            if 'destination_filename' in kwargs and len(kwargs['destination_filename']) != 0:
                destination_filesystem = kwargs['destination_filename']
            else:
                destination_filesystem = kwargs['source_filename']

        copy_command_str = 'copy ' + source_filesystem + destination_filesystem

        is_downloaded = (False, '')
        while (not is_downloaded[0]) and (retries > 0):
            retries -= 1

            output = self._send_command(copy_command_str, expected_str='\?')

            while re.search(self._prompt, output) is None:
                if re.search('source filename', output.lower()):
                    output = self._send_command(kwargs['source_filename'], expected_str='\?')
                elif re.search('remote host', output.lower()):
                    if 'remote_host' not in kwargs or len(kwargs['remote_host']) == 0:
                        raise Exception('Cisco IOS', 'Copy method: remote host not set!')

                    if not validateIP(kwargs['remote_host']):
                        raise Exception('Cisco IOS', 'Copy method: remote host ip is not valid!')

                    output = self._send_command(kwargs['remote_host'], expected_str='\?')
                elif re.search('destination filename', output.lower()):
                    destination_filename = ''
                    if 'destination_filename' in kwargs:
                        destination_filename = kwargs['destination_filename']

                    output = self._send_command(destination_filename, expected_str=self._prompt,
                                               expected_map={'\[confirm\]|\?': expected_actions.send_empty_string},
                                               timeout=timeout)

            is_downloaded = self._check_download_from_tftp(output)

        return is_downloaded

    def configure(self, type, timeout=30, retries=5, **kwargs):
        command = 'configure '
        if type == 'replace':
            if 'source_filename' not in kwargs:
                raise Exception('Cisco IOS', "Config replace method doesn't have  source filename!")
            command += 'replace ' + kwargs['source_filename']

            expected_map = {
                '\[no\]|\[yes\]:': expected_actions.send_yes
            }

            output = self._send_command(command, expected_str=self._prompt, expected_map=expected_map,
                                       timeout=timeout)

            match_error = re.search('[Ee]rror:', output)
            if not match_error is None:
                error_str = output[match_error.end() + 1:]
                error_str = error_str[:error_str.find('\n')]
                raise Exception('Cisco IOS', 'Configure replace error: ' + error_str)

    def cloud_shell_api(self):
        if not self._cloud_shell_api:
            hostname = socket.gethostname()
            testshell_ip = socket.gethostbyname(hostname)
            testshell_user = self.reservation_dict['AdminUsername']
            testshell_password = self.reservation_dict['AdminPassword']
            testshell_domain = self.reservation_dict['Domain']
            self._cloud_shell_api = CloudShellAPISession(testshell_ip, testshell_user, testshell_password, testshell_domain)
        return self._cloud_shell_api

    def reload(self, sleep_timeout=60, retry_count=5):
        output = self._send_command('reload', expected_str='\[yes/no\]:|[confirm]')

        if re.search('\[yes/no\]:', output):
            self._send_command('yes', '[confirm]')

        output = self._send_command('', expected_str='.*', expected_map={})

        retry = 0
        is_reloaded = False
        while retry < retry_count:
            retry += 1

            time.sleep(sleep_timeout)
            try:
                output = self._send_command('', expected_str='(?<![#\n])[#>] *$', expected_map={}, timeout=5,
                                           is_need_default_prompt=False)
                if len(output) == 0:
                    continue

                is_reloaded = True
                break
            except Exception as e:
                pass

        return is_reloaded

    def _get_all_interfaces_info(self):
        """Get list of interfaces and their information, trigger 'show ip interface brief' command and parse output

        :return: dictionary with all interfaces' info
        """

        data_str = self._send_command('show ip interface b ')
        interface_data = {}
        data_str = re.sub(' +', ' ', data_str)

        for line in data_str.splitlines():
            match_object = re.search(r'^(?P<interface_name>\S+)' +
                                     '\s+(?P<port_ip>\S+)' +
                                     '\s+(?P<port_state>\S+)' +
                                     '\s+(?P<port_method>\S+)' +
                                     '\s+(?P<port_status>.+)', line.strip())
            if match_object:
                match_dict = match_object.groupdict()

                if 'interface_name' in match_dict and \
                                re.search('[Ii]nterface', match_dict['interface_name']) is None:
                    interface_data[match_dict['interface_name']] = \
                        getDictionaryData(match_dict, ['interface_name'])
        return interface_data

    def _get_data_match(self, reg_exp, data_str):
        data_map = {}

        match_object = re.search(reg_exp, data_str)
        if match_object:
            data_map.update(match_object.groupdict())

        return data_map

    def _is_interface_support_qnq(self, interface_name):
        result = False
        self.send_config_command('interface {0}'.format(interface_name))
        output = self.send_config_command('switchport mode ?')
        if 'dot1q-tunnel' in output.lower():
            result = True
        self._exit_configuration_mode()
        return result

    def _get_resource_full_name(self, port_resource_address, resource_details_map):
        result = None
        for port in resource_details_map.ChildResources:
            if port.FullAddress in port_resource_address and port.FullAddress == port_resource_address:
                return port.Name
            if port.FullAddress in port_resource_address and port.FullAddress != port_resource_address:
                result = self._get_resource_full_name(port_resource_address, port)
            if result is not None:
                return result
        return result

    def configure_vlan(self, vlan_range, port_list, switchport_type, additional_info, remove=False):
        """
        Sends snmp get command
        :param vlan_range: range of vlans to be added, if empty, and switchport_type = trunk,
        trunk mode will be assigned
        :param port_list: List of interfaces Resource Full Address
        :param switchport_type: type of adding vlan ('trunk' or 'access')
        :param additional_info: contains QNQ or CTag parameter
        :param remove: remove or add flag
        :return: success message
        :rtype: string
        """
        self._logger.info('Vlan Configuration Started')
        if len(port_list) < 1:
            raise Exception('Port list is empty')
        if vlan_range == '' and switchport_type == 'access':
            raise Exception('Switchport type is Access, but vlan id/range is empty')
        if (',' in vlan_range or '-' in vlan_range) and switchport_type == 'access':
            raise Exception('Only one vlan could be assigned to the interface in Access mode')
        for port in port_list.split('|'):
            port_resource_map = self.cloud_shell_api().GetResourceDetails(self.attributes_dict['ResourceName'])
            temp_port_name = self._get_resource_full_name(port, port_resource_map)
            if '/' not in temp_port_name:
                self._logger.error('Interface was not found')
                raise Exception('Interface was not found')
            port_name = temp_port_name.split('/')[-1].replace('-', '/')
            self._logger.info('Vlan {0} will be assigned to or removed from interface {1}'.format(vlan_range,
                                                                                                  port_name))

            params_map = dict()

            params_map['configure_interface'] = port_name
            if not remove:
                if 'trunk' in switchport_type and vlan_range == '':
                    params_map['switchport_mode_trunk'] = []
                elif 'trunk' in switchport_type and vlan_range != '':
                    params_map['trunk_allow_vlan'] = [vlan_range]
                elif 'access' in switchport_type and vlan_range != '':
                    params_map['access_allow_vlan'] = [vlan_range]

                if 'qnq' in additional_info.lower():
                    if not self._is_interface_support_qnq(port_name):
                        raise Exception('interface does not support QnQ')
                    if 'switchport_mode_trunk' in params_map:
                        raise Exception('interface cannot have trunk and dot1q-tunneling modes in the same time')
                    params_map['qnq'] = ''

            self.configure_interface_ethernet(**params_map)
            self._exit_configuration_mode()
            if remove:
                self._logger.info('All vlans and switchport mode were removed from the interface {0}'.format(port_name))
            self._logger.info('Vlan {0} was assigned to the interface {1}'.format(vlan_range, port_name))
        return 'Vlan Configuration Completed'

    def configure_interface_ethernet(self, **kwargs):
        """
        Configures interface ethernet
        :param kwargs: dictionary of parameters
        :return: success message
        :rtype: string
        """
        interface_ethernet = Ethernet()
        commands_list = interface_ethernet.get_commands_list(**kwargs)
        current_config = self._send_command('show  running-config interface {0}'.format(kwargs['configure_interface']))

        for line in current_config.splitlines():
            if re.search('^\s*switchport', line):
                commands_list.insert(1, 'no {0}'.format(line))
        self.send_commands_list(commands_list)
        return 'Finished configuration of ethernet interface!'

    def snmp_get(self, get_mib, get_command, get_index, oid=None):
        """
        Sends snmp get command
        :param get_mib: Mib name ('SNMPv2-MIB')
        :param get_command: command name ('sysDescr')
        :param get_index: index name ('0')
        :return: success message
        :rtype: string
        """
        request_command = ''
        if oid:
            request_command = oid
        elif get_mib != '' and get_command != '' and get_index != '':
            request_command = (get_mib, get_command, get_index)
        else:
            self._logger.error('One or several Snmp Get parameters is empty')

        return self.snmp_handler.get(request_command)

    def is_valid_device_os(self):
        """Validate device OS by snmp
        :return: True or False
        """
        version = None

        system_description = self.snmp_handler.get(('SNMPv2-MIB', 'sysDescr'))['sysDescr']
        match_str = re.sub('[\n\r]+', ' ', system_description.upper())
        res = re.search(' (IOS|IOS-XE|CAT[ -]?OS) ', match_str)
        if res:
            version = res.group(0).strip(' \s\r\n')
        if version and version in self.supported_os:
            return True
        self._logger.info('System description from device: \'{0}\''.format(system_description))
        return False

    def discover_snmp(self):
        """Load device structure, and all required Attribute according to Networking Elements Standardization design
        :return: Attributes and Resources matrix,
        currently in string format (matrix separated by '$', lines by '|', columns by ',')
        """

        if not self.is_valid_device_os():
            error_message = 'Incompatible driver! Please use correct resource driver for {0} operation system(s)'. \
                format(str(tuple(self.supported_os)))
            self._logger.error(error_message)
            raise Exception(error_message)

        self._logger.info('************************************************************************')
        self._logger.info('Start SNMP discovery process .....')
        generic_autoload = CiscoGenericSNMPAutoload(self.snmp_handler, self._logger)
        result = generic_autoload.discover()
        self._logger.info('Start SNMP discovery Completed')
        return result

    def update_firmware(self, remote_host, file_path, size_of_firmware=200000000):
        """Update firmware version on device by loading provided image, performs following steps:

            1. Copy bin file from remote tftp server.
            2. Clear in run config boot system section.
            3. Set downloaded bin file as boot file and then reboot device.
            4. Check if firmware was successfully installed.

        :param remote_host: host with firmware
        :param file_path: relative path on remote host
        :param size_of_firmware: size in bytes
        :return: status / exception
        """

        firmware_obj = CiscoFirmwareData(file_path)
        if firmware_obj.getName() is None:
            raise Exception('Cisco IOS', "Invalid firmware name!\n \
                            Firmware file must have: title, extension.\n \
                            Example: isr4400-universalk9.03.10.00.S.153-3.S-ext.SPA.bin\n\n \
                            Current path: " + file_path)

            # if not validateIP(remote_host):
            #     raise Exception('Cisco ISR 4K', "Not valid remote host IP address!")
        free_memory_size = self._get_free_memory_size('bootflash')

        #if size_of_firmware > free_memory_size:
        #    raise Exception('Cisco ISR 4K', "Not enough memory for firmware!")

        is_downloaded = self.copy('tftp', 'bootflash', remote_host=remote_host,
                                  source_filename=file_path, timeout=600, retries=2)

        if not is_downloaded[0]:
            raise Exception('Cisco IOS', "Failed to download firmware from " + remote_host +
                            file_path + "!\n" + is_downloaded[1])

        self._send_command('configure terminal', expected_str='(config)#')
        self._remove_old_boot_system_config()
        output = self._send_command('do show run | include boot')

        is_boot_firmware = False
        firmware_full_name = firmware_obj.getName() + \
                             '.' + firmware_obj.getExtension()

        retries = 5
        while (not is_boot_firmware) and (retries > 0):
            self._send_command('boot system flash bootflash:' + firmware_full_name, expected_str='(config)#')
            self._send_command('config-reg 0x2102', expected_str='(config)#')

            output = self._send_command('do show run | include boot')

            retries -= 1
            is_boot_firmware = output.find(firmware_full_name) != -1

        if not is_boot_firmware:
            raise Exception('Cisco IOS', "Can't add firmware '" + firmware_full_name + "' dor boot!")

        self._send_command('exit')
        output = self._send_command('copy run start', expected_map={'\?': expected_actions.send_empty_string})
        is_reloaded = self.reload()
        output_version = self._send_command('show version | include image file')

        is_firmware_installed = output_version.find(firmware_full_name)
        if is_firmware_installed != -1:
            return 'Finished updating firmware!'
        else:
            raise Exception('Cisco IOS', 'Firmware update was unsuccessful!')

    def _get_resource_attribute(self, resource_full_path, attribute_name):
        try:
            result = self.cloud_shell_api.GetAttributeValue(resource_full_path, attribute_name).Value
        except Exception as e:
            raise Exception(e.message)
        return result

    def backup_configuration(self, custom_destination_host, source_filename):
        """Backup 'startup-config' or 'running-config' from device to provided file_system [ftp|tftp]
        Also possible to backup config to localhost

        :param custom_destination_host:  tftp/ftp server where file be saved
        :param source_filename: what file to backup
        :return: status message / exception
        """

        system_name = self.attributes_dict['ResourceFullName'].replace('.', '_')
        destination_filename = '{0}-{1}-{2}'.format(system_name, source_filename, self._get_time_stamp())
        self._logger.info('destination filename is {0}'.format(destination_filename))

        destination_host = custom_destination_host
        if '//' not in destination_host:
            destination_host = self._get_resource_attribute(self.attributes_dict['ResourceFullName'],
                                                            'Backup Location')
            if '//' not in destination_host:
                raise Exception('Cisco IOS', "Remote filesystem must be 'tftp' or 'ftp'!")

        destination_path = destination_host.split('://')
        remote_host = destination_path[1]
        destination_filesystem = destination_path[0]

        if (source_filename != 'startup-config') and (source_filename != 'running-config'):
            raise Exception('Cisco IOS', "Source filename must be 'startup-config' or 'running-config'!")

        if ('127.0.0.1' in destination_host) or ('localhost' in destination_host) or (destination_host == ''):
            remote_host = 'localhost'

        elif re.match('tftp|ftp', destination_host) is None:
            raise Exception('Cisco IOS', "Remote filesystem must be 'tftp' or 'ftp'!")

        is_uploaded = self.copy(destination_filesystem=destination_filesystem, remote_host=remote_host,
                                source_filename=source_filename, destination_filename=destination_filename,
                                timeout=600, retries=5)

        if is_uploaded[0] is True:
            return 'Finished backing up configuration! Destination file is {0}'.format(destination_filename)
        else:
            return is_uploaded[1]

    def _get_time_stamp(self):
        return time.strftime("%d%m%Y-%H%M%S", time.gmtime())

    def restore_configuration(self, source_file, clear_config='override'):
        """Restore configuration on device from provided configuration file
        Restore configuration from local file system or ftp/tftp server into 'running-config' or 'startup-config'.
        :param source_file: relative path to the file on the remote host tftp://server/sourcefile
        :param clear_config: override current config or not
        :return:
        """
        self._logger.info('Start restoring device configuration from {}'.format(source_file))

        extracted_data = source_file.split('://')
        source_filesystem = extracted_data[0]
        match_data = re.search('startup-config|running-config', extracted_data[1])
        if not match_data:
            raise Exception('Cisco IOS', "Destination filename must be 'startup-config' or 'running-config'!")
        else:
            destination_filename = match_data.group()
        remote_host_match = re.search('^(?P<host>\S+)/', extracted_data[1])
        if not remote_host_match or not remote_host_match.groupdict()['host']:
            raise Exception('Cisco IOS', "Cannot find hostname!")
        else:
            remote_host = remote_host_match.groupdict()['host']

        source_filename = extracted_data[1].replace(remote_host + '/', '')

        if ('127.0.0.1' in source_file) or ('localhost' in source_file):
            remote_host = 'localhost'

        if (clear_config.lower() == 'override') and (destination_filename == 'startup-config'):
            self._send_command('del ' + destination_filename,
                               expected_map={'\?|[confirm]': expected_actions.send_empty_string})

            is_uploaded = self.copy(source_filesystem=source_filesystem, remote_host=remote_host,
                                    source_filename=source_filename, destination_filename=destination_filename,
                                    timeout=600, retries=5)
        elif (clear_config.lower() == 'override') and (destination_filename == 'running-config'):

            if not (remote_host == 'localhost'):
                source_filename = source_file

            self.configure('replace', source_filename=source_filename, timeout=600)
            is_uploaded = (True, '')
        else:
            is_uploaded = self.copy(source_filesystem=source_filesystem, remote_host=remote_host,
                                    source_filename=source_filename, destination_filename=destination_filename,
                                    timeout=600, retries=5)

        if is_uploaded[0] is False:
            raise Exception('Cisco IOS', is_uploaded[1])

        is_downloaded = (True, '')

        if is_downloaded[0] is True:
            return 'Finished restore configuration!'
        else:
            raise Exception('Cisco IOS', is_downloaded[1])

    def _remove_old_boot_system_config(self):
        """Clear boot system parameters in current configuration
        """

        data = self._send_command('do show run | include boot')
        start_marker_str = 'boot-start-marker'
        index_begin = data.find(start_marker_str)
        index_end = data.find('boot-end-marker')

        if index_begin == -1 or index_end == -1:
            return

        data = data[index_begin + len(start_marker_str):index_end]
        data_list = data.split('\n')

        for line in data_list:
            if line.find('boot system') != -1:
                self._send_command('no ' + line, expected_str='(config)#')

    def _get_free_memory_size(self, partition):
        """Get available memory size on provided partition
        :param partition: file system
        :return: size of free memory in bytes
        """

        cmd = 'dir {0}:'.format(partition)
        output = self._send_command(cmd, retry_count=100)

        find_str = 'bytes total ('
        position = output.find(find_str)
        if position != -1:
            size_str = output[(position + len(find_str)):]

            size_match = re.match('[0-9]*', size_str)
            if size_match:
                return int(size_match.group())
            else:
                return -1
        else:
            return -1

    def _get_ethernet_interface_info(self, interface_name):
        """Get interface information. Send 'Show interface X' command and parse returned output
            Method for get ethernet interface info map

        :param interface_name: interface to get information from
        :return: dictionary with interface info
        """

        interface_info = {}
        interface_data = self._send_command('show interface ' + interface_name)

        data_str = re.sub('[\n\r]', '$', interface_data)
        data_str = re.sub(' +', ' ', data_str)

        #hardware
        interface_info.update(self._get_data_match('Hardware is (?P<type>[\w/\-\+\d ]+).*', data_str))
        interface_info.update(self._get_data_match('address is (?P<mac>[\w\d]{4}\.[\d\w]{4}\.[\w\d]{4})', data_str))
        interface_info.update(self._get_data_match(
            'Internet address is (?P<port_ip>(\d+\.){3}\d+)[/ ]{1}(?P<mask>(\d+\.){3}\d+|\d{0,2})', data_str))
        interface_info.update(self._get_data_match('.*MTU (?P<mtu>\d+) bytes,', data_str))
        interface_info.update(self._get_data_match('BW (?P<bandwidth>\d+ .bit/sec), +', data_str))
        interface_info.update(self._get_data_match('DLY (?P<dly>\d+ usec),.*', data_str))
        interface_info.update(self._get_data_match('Encapsulation (?P<encapsulation>\S+),', data_str))
        interface_info.update(self._get_data_match('.*\$ (?P<duplex>Full)? Duplex,', data_str))
        interface_info.update(self._get_data_match('.*media type is (?P<media_type>[^\$]*)\$', data_str))

        if 'port_ip' in interface_info:
            if validateIP(interface_info['port_ip']):
                if 'mask' in interface_info:
                    interface_info['mask'] = ipcalc.Network('{}/{}'.format(interface_info['port_ip'],
                                                                           interface_info['mask'])).netmask()
            else:
                interface_info.pop("port_ip", None)
        elif 'mask' in interface_info:
            interface_info.pop("mask", None)

        return interface_info

    def _get_release_version(self):
        """Get release version information by sending 'show version' command and parsing output
        :return: version string
        """
        version_info = self._send_command('show version | section Version')

        result = ''
        match_object = re.search('(?<=Version )(.*?)(?=,)', version_info)
        if match_object is not None:
            result = match_object.group(1)
        return result

    def _get_firmware_version(self):
        """Get firmware version information by sending 'show version' command and parsing output
        :return: version string
        """
        version_info = self._send_command('show version | include .bin')

        result_version = ''
        index = version_info.find(':')
        if index != -1:
            result_version = version_info[index + 1:]
            result_version = result_version.replace('\n', '$')
            result_version = re.sub('\".*', '', result_version)
        return result_version
