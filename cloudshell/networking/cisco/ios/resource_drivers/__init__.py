__author__ = 'coye'
from pkgutil import extend_path

from cloudshell.networking.cisco.ios.cisco_ios import CiscoIOS
from cloudshell.shell.core.handler_factory import HandlerFactory

__path__ = extend_path(__path__, __name__)
HandlerFactory.handler_classes['CATALYST_2950'] = CiscoIOS
HandlerFactory.handler_classes['IOS'] = CiscoIOS