__author__ = 'CoYe'
from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase

class CiscoIOSHandler(CiscoHandlerBase):
    def __init__(self):
        CiscoHandlerBase.__init__(self)
        self.supported_os = ['IOS', 'IOS-XE', 'CATOS']
