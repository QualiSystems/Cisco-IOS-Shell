from cloudshell.networking.cisco.ios.cisco_ios_handler import CiscoIOSHandler
from cloudshell.shell.core.context.context_utils import get_attribute_by_name
import re, inject

my_handler = CiscoIOSHandler


def get_handler():
    return my_handler


HANDLER_CLASS = CiscoIOSHandler
DEFAULT_PROMPT = '.*>\s*$|.*#\s*$'
ENABLE_PROMPT = '.*#\s*$'
CONFIG_MODE_PROMPT = '\(config.*\)#\s*$'

@inject.params(logger='logger')
def send_default_actions(session, logger=None):
    """Send default commands to configure/clear session outputs
    :return:
    """
    session.hardware_expect('terminal length 0', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)
    session.hardware_expect('terminal no exec prompt timestamp', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)
    session.hardware_expect(ENTER_CONFIG_MODE_PROMPT_COMMAND, CONFIG_MODE_PROMPT)
    session.hardware_expect('no logging console', CONFIG_MODE_PROMPT)
    session.hardware_expect('exit', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)

CONNECTION_TYPE = 'ssh'
ENTER_CONFIG_MODE_PROMPT_COMMAND = 'configure terminal'
EXIT_CONFIG_MODE_PROMPT_COMMAND = 'exit'
DEFAULT_ACTIONS = send_default_actions

