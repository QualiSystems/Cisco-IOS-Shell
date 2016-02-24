from cloudshell.networking.cisco.ios.cisco_ios_handler import CiscoIOSHandler
from cloudshell.shell.core.handler_factory import HandlerFactory
from cloudshell.networking.cisco.resource_drivers_map import CISCO_RESOURCE_DRIVERS_MAP
from cloudshell.networking.platform_detector.hardware_platform_detector import HardwarePlatformDetector

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

HandlerFactory.handler_classes['CATALYST_2950'] = CiscoIOSHandler
HandlerFactory.handler_classes['IOS'] = CiscoIOSHandler
HardwarePlatformDetector.RESOURCE_DRIVERS_MAP = CISCO_RESOURCE_DRIVERS_MAP
