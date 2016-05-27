__author__ = 'CoYe'
from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase

class CiscoIOSHandler(CiscoHandlerBase):
    def __init__(self):
        CiscoHandlerBase.__init__(self)
        self.supported_os = ['IOS', 'IOS-XE', 'CATOS']

    # @inject.params(cli='cli_service', logger='logger', snmp='snmp_handler', api='api')
    # def __init__(self, cli, logger, snmp, api):
    #     CiscoHandlerBase.__init__(self, cli=cli, logger=logger, snmp=snmp, api=api)
    #     self.supported_os = ['IOS', 'IOS-XE', 'CATOS']
