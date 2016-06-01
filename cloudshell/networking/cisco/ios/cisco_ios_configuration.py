from cloudshell.networking.cisco.ios.cisco_ios_handler import CiscoIOSHandler


my_handler = CiscoIOSHandler


def get_handler():
    return my_handler


HANDLER_CLASS = CiscoIOSHandler
DEFAULT_PROMPT = '.*>\s*$|.*#\s*$'
ENABLE_PROMPT = '.*#\s*$'
CONFIG_MODE_PROMPT = '\(config.*\)#\s*$'

def send_default_actions(session):
    """Send default commands to configure/clear session outputs
    :return:
    """

    session.hardware_expect('terminal length 0', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)
    session.hardware_expect('terminal no exec prompt timestamp', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)
    session.hardware_expect(ENTER_CONFIG_MODE_PROMPT_COMMAND, CONFIG_MODE_PROMPT)
    session.hardware_expect('no logging console', CONFIG_MODE_PROMPT)
    session.hardware_expect('exit', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)

ENTER_CONFIG_MODE_PROMPT_COMMAND = 'configure terminal'
EXIT_CONFIG_MODE_PROMPT_COMMAND = 'exit'
DEFAULT_ACTIONS = send_default_actions

