import re
from cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload
from cloudshell.networking.cisco.cisco_configuration_operations import CiscoConfigurationOperations
from cloudshell.networking.cisco.cisco_connectivity_operations import CiscoConnectivityOperations
from cloudshell.networking.cisco.cisco_send_command_operations import CiscoSendCommandOperations
from cloudshell.shell.core.context_utils import get_decrypted_password_by_attribute_name_wrapper


DEFAULT_PROMPT = '.*>\s*$|.*#\s*$'
ENABLE_PROMPT = '.*#\s*$'
CONFIG_MODE_PROMPT = '\(config.*\)#\s*$'


def send_default_actions(session):
    """Send default commands to configure/clear session outputs
    :return:
    """
    enter_enable_mode(session=session)
    session.hardware_expect('terminal length 0', ENABLE_PROMPT)
    session.hardware_expect('terminal no exec prompt timestamp', ENABLE_PROMPT)
    session.hardware_expect(ENTER_CONFIG_MODE_PROMPT_COMMAND, CONFIG_MODE_PROMPT)
    session.hardware_expect('no logging console', CONFIG_MODE_PROMPT)
    session.hardware_expect('exit', DEFAULT_PROMPT + '|' + ENABLE_PROMPT)


ENTER_CONFIG_MODE_PROMPT_COMMAND = 'configure terminal'
EXIT_CONFIG_MODE_PROMPT_COMMAND = 'exit'
DEFAULT_ACTIONS = send_default_actions
SUPPORTED_OS = ['IOS', 'IOS-XE', 'CATOS']


def enter_enable_mode(session):
    session.hardware_expect('enable', re_string=DEFAULT_PROMPT + '|' + ENABLE_PROMPT,
                            expect_map={'[Pp]assword': lambda session: session.send_line(
                                get_decrypted_password_by_attribute_name_wrapper('Enable Password')())})
    result = session.hardware_expect('', re_string=DEFAULT_PROMPT + '|' + ENABLE_PROMPT)
    if not re.search(ENABLE_PROMPT, result):
        raise Exception('enter_enable_mode', 'Enable password is incorrect')


CONNECTIVITY_OPERATIONS_CLASS = CiscoConnectivityOperations
CONFIGURATION_OPERATIONS_CLASS = CiscoConfigurationOperations
FIRMWARE_OPERATIONS_CLASS = CiscoConfigurationOperations
AUTOLOAD_OPERATIONS_CLASS = CiscoGenericSNMPAutoload
SEND_COMMAND_OPERATIONS_CLASS = CiscoSendCommandOperations
