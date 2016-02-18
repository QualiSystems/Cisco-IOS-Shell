__author__ = 'CoYe'

from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase

class CiscoIOSHandler(CiscoHandlerBase):
    def __init__(self, connection_manager, logger=None):
        CiscoHandlerBase.__init__(self, connection_manager, logger)
        self.supported_os = ['IOS', 'IOS-XE', 'CATOS']

