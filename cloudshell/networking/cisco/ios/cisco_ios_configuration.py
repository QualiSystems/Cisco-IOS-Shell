from cloudshell.networking.cisco.ios.cisco_ios_handler import CiscoIOSHandler

my_handler = CiscoIOSHandler

def get_handler():
    return my_handler

HANDLER_CLASS = CiscoIOSHandler
DEFAULT_PROMPT = '.*> *$'
ENABLE_PROMPT = '.*# *$'
CONFIG_MODE_PROMPT = '\(config.*\)# *$'

#DEFAULT_ACTIONS = CiscoIOSHandler._default_actions()
