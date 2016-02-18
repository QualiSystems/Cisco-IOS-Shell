__author__ = 'CoYe'

from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase

class CiscoIOSHandler(CiscoHandlerBase):
    def __init__(self, connection_manager, logger):
        CiscoHandlerBase.__init__(self, connection_manager, logger)
