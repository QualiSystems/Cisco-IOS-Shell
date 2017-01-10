from cloudshell.shell.core.base_autoload_structure_generator import BaseResource


class CiscoIOSDevice(BaseResource):
    SYSTEM_NAME = 'system_name'
    CONTACT_NAME = 'contact_name'
    OS_VERSION = 'os_version'
    VENDOR = 'vendor'
    LOCATION = 'location'
    MODEL = 'model'

    def __init__(self, system_name='', contact_name='', os_version='', vendor='', location='', model=''):
        """
        Represent CiscoIOSDevice resource entity

        :param str system_name: A unique identifier for the device, if exists in the device terminal/os.
        :param str contact_name: The name of a contact registered in the device.
        :param str os_version: Version of the Operating System.
        :param str vendor: The name of the device manufacture.
        :param str location: The device physical location identifier. For example Lab1/Floor2/Row5/Slot4.
        :param str model: The device model. This information is typically used for abstract resource filtering.
        :return CiscoIOSDevice
        """

        BaseResource.__init__(self)
        self.attributes = {
            'System Name': system_name,
            'Contact Name': contact_name,
            'OS Version': os_version,
            'Vendor': vendor,
            'Location': location,
            'Model': model}

    @property
    def system_name(self):
        return self.attributes['System Name']

    @system_name.setter
    def system_name(self, value):
        self.attributes['System Name'] = value

    @property
    def contact_name(self):
        return self.attributes['Contact Name']

    @contact_name.setter
    def contact_name(self, value):
        self.attributes['Contact Name'] = value

    @property
    def os_version(self):
        return self.attributes['OS Version']

    @os_version.setter
    def os_version(self, value):
        self.attributes['OS Version'] = value

    @property
    def vendor(self):
        return self.attributes['Vendor']

    @vendor.setter
    def vendor(self, value):
        self.attributes['Vendor'] = value

    @property
    def location(self):
        return self.attributes['Location']

    @location.setter
    def location(self, value):
        self.attributes['Location'] = value

    @property
    def model(self):
        return self.attributes['Model']

    @model.setter
    def model(self, value):
        self.attributes['Model'] = value


class GenericChassis(BaseResource):
    MODEL = 'model'
    SERIAL_NUMBER = 'serial_number'

    def __init__(self, name, relative_address, resource_model='Generic Chassis', unique_id=None, model='',
                 serial_number=''):
        """
        Represent Generic Chassis resource entity

        :param str model: The device model. This information is typically used for abstract resource filtering.
        :param str serial_number: 
        :return Generic Chassis
        """

        BaseResource.__init__(self, resource_model=resource_model, name=name, relative_address=relative_address, unique_id=unique_id)
        self.attributes = {
            'Model': model,
            'Serial Number': serial_number}

    @property
    def model(self):
        return self.attributes['Model']

    @model.setter
    def model(self, value):
        self.attributes['Model'] = value

    @property
    def serial_number(self):
        return self.attributes['Serial Number']

    @serial_number.setter
    def serial_number(self, value):
        self.attributes['Serial Number'] = value


class GenericModule(BaseResource):
    SERIAL_NUMBER = 'serial_number'
    VERSION = 'version'
    MODEL = 'model'

    def __init__(self, name, relative_address, resource_model='Generic Module', unique_id=None, serial_number='', version='', model=''):
        """
        Represent Generic Module resource entity

        :param str serial_number: 
        :param str version: The firmware version of the resource.
        :param str model: The device model. This information is typically used for abstract resource filtering.
        :return Generic Module
        """

        BaseResource.__init__(self, resource_model=resource_model, name=name, relative_address=relative_address, unique_id=unique_id)
        self.attributes = {
            'Serial Number': serial_number,
            'Version': version,
            'Model': model}

    @property
    def serial_number(self):
        return self.attributes['Serial Number']

    @serial_number.setter
    def serial_number(self, value):
        self.attributes['Serial Number'] = value

    @property
    def version(self):
        return self.attributes['Version']

    @version.setter
    def version(self, value):
        self.attributes['Version'] = value

    @property
    def model(self):
        return self.attributes['Model']

    @model.setter
    def model(self, value):
        self.attributes['Model'] = value


class GenericPort(BaseResource):
    MAC_ADDRESS = 'mac_address'
    L2_PROTOCOL_TYPE = 'l2_protocol_type'
    IPV4_ADDRESS = 'ipv4_address'
    IPV6_ADDRESS = 'ipv6_address'
    PORT_DESCRIPTION = 'port_description'
    BANDWIDTH = 'bandwidth'
    MTU = 'mtu'
    DUPLEX = 'duplex'
    ADJACENT = 'adjacent'
    AUTO_NEGOTIATION = 'auto_negotiation'

    def __init__(self, name, relative_address, resource_model='Generic Port', unique_id=None, mac_address='',
                 l2_protocol_type='', ipv4_address='', ipv6_address='', port_description='', bandwidth='0', mtu='0',
                 duplex='Half', adjacent='', auto_negotiation='False'):
        """
        Represent Generic Port resource entity

        :param str mac_address: 
        :param str l2_protocol_type: The L2 protocol type configured on the interface. For example POS, Serial.
        :param str ipv4_address: 
        :param str ipv6_address: 
        :param str port_description: The description of the port as configured in the device.
        :param int bandwidth: The current interface bandwidth, in MB.
        :param int mtu: The current MTU configured on the interface.
        :param str duplex: The current duplex configuration on the interface. Possible values are Half or Full.
        :param str adjacent: The adjacent device (system name) and port, based on LLDP or CDP protocol.
        :param bool auto_negotiation: The current auto negotiation configuration on the interface.
        :return Generic Port
        """

        BaseResource.__init__(self, resource_model=resource_model, name=name, relative_address=relative_address,
                              unique_id=unique_id)
        self.attributes = {
            'MAC Address': mac_address,
            'L2 Protocol Type': l2_protocol_type,
            'IPv4 Address': ipv4_address,
            'IPv6 Address': ipv6_address,
            'Port Description': port_description,
            'Bandwidth': bandwidth,
            'MTU': mtu,
            'Duplex': duplex,
            'Adjacent': adjacent,
            'Auto Negotiation': auto_negotiation}

    @property
    def mac_address(self):
        return self.attributes['MAC Address']

    @mac_address.setter
    def mac_address(self, value):
        self.attributes['MAC Address'] = value

    @property
    def l2_protocol_type(self):
        return self.attributes['L2 Protocol Type']

    @l2_protocol_type.setter
    def l2_protocol_type(self, value):
        self.attributes['L2 Protocol Type'] = value

    @property
    def ipv4_address(self):
        return self.attributes['IPv4 Address']

    @ipv4_address.setter
    def ipv4_address(self, value):
        self.attributes['IPv4 Address'] = value

    @property
    def ipv6_address(self):
        return self.attributes['IPv6 Address']

    @ipv6_address.setter
    def ipv6_address(self, value):
        self.attributes['IPv6 Address'] = value

    @property
    def port_description(self):
        return self.attributes['Port Description']

    @port_description.setter
    def port_description(self, value):
        self.attributes['Port Description'] = value

    @property
    def bandwidth(self):
        return self.attributes['Bandwidth']

    @bandwidth.setter
    def bandwidth(self, value):
        self.attributes['Bandwidth'] = value

    @property
    def mtu(self):
        return self.attributes['MTU']

    @mtu.setter
    def mtu(self, value):
        self.attributes['MTU'] = value

    @property
    def duplex(self):
        return self.attributes['Duplex']

    @duplex.setter
    def duplex(self, value):
        self.attributes['Duplex'] = value

    @property
    def adjacent(self):
        return self.attributes['Adjacent']

    @adjacent.setter
    def adjacent(self, value):
        self.attributes['Adjacent'] = value

    @property
    def auto_negotiation(self):
        return self.attributes['Auto Negotiation']

    @auto_negotiation.setter
    def auto_negotiation(self, value):
        self.attributes['Auto Negotiation'] = value


class GenericSubModule(BaseResource):
    SERIAL_NUMBER = 'serial_number'
    VERSION = 'version'
    MODEL = 'model'

    def __init__(self, name, relative_address, resource_model='Generic Sub Module', unique_id=None, serial_number='',
                 version='', model=''):
        """
        Represent Generic Sub Module resource entity

        :param str serial_number: 
        :param str version: The firmware version of the resource.
        :param str model: The device model. This information is typically used for abstract resource filtering.
        :return Generic Sub Module
        """

        BaseResource.__init__(self, resource_model=resource_model, name=name, relative_address=relative_address,
                              unique_id=unique_id)
        self.attributes = {
            'Serial Number': serial_number,
            'Version': version,
            'Model': model}

    @property
    def serial_number(self):
        return self.attributes['Serial Number']

    @serial_number.setter
    def serial_number(self, value):
        self.attributes['Serial Number'] = value

    @property
    def version(self):
        return self.attributes['Version']

    @version.setter
    def version(self, value):
        self.attributes['Version'] = value

    @property
    def model(self):
        return self.attributes['Model']

    @model.setter
    def model(self, value):
        self.attributes['Model'] = value


class GenericPowerPort(BaseResource):
    MODEL = 'model'
    SERIAL_NUMBER = 'serial_number'
    VERSION = 'version'
    PORT_DESCRIPTION = 'port_description'

    def __init__(self, name, relative_address, resource_model='Generic Power Port', unique_id=None, model='',
                 serial_number='', version='', port_description=''):
        """
        Represent Generic Power Port resource entity

        :param str model: The device model. This information is typically used for abstract resource filtering.
        :param str serial_number: 
        :param str version: The firmware version of the resource.
        :param str port_description: The description of the port as configured in the device.
        :return Generic Power Port
        """

        BaseResource.__init__(self, resource_model=resource_model, name=name, relative_address=relative_address,
                              unique_id=unique_id)
        self.attributes = {
            'Model': model,
            'Serial Number': serial_number,
            'Version': version,
            'Port Description': port_description}

    @property
    def model(self):
        return self.attributes['Model']

    @model.setter
    def model(self, value):
        self.attributes['Model'] = value

    @property
    def serial_number(self):
        return self.attributes['Serial Number']

    @serial_number.setter
    def serial_number(self, value):
        self.attributes['Serial Number'] = value

    @property
    def version(self):
        return self.attributes['Version']

    @version.setter
    def version(self, value):
        self.attributes['Version'] = value

    @property
    def port_description(self):
        return self.attributes['Port Description']

    @port_description.setter
    def port_description(self, value):
        self.attributes['Port Description'] = value


class GenericPortChannel(BaseResource):
    ASSOCIATED_PORTS = 'associated_ports'
    IPV4_ADDRESS = 'ipv4_address'
    IPV6_ADDRESS = 'ipv6_address'
    PORT_DESCRIPTION = 'port_description'

    def __init__(self, name, relative_address, resource_model='Generic Port Channel', unique_id=None,
                 associated_ports='', ipv4_address='', ipv6_address='', port_description=''):
        """
        Represent Generic Port Channel resource entity

        :param str associated_ports: Ports associated with this port channel. The value is in the format "[portResourceName],...", for example "GE0-0-0-1,GE0-0-0-2"
        :param str ipv4_address: 
        :param str ipv6_address: 
        :param str port_description: The description of the port as configured in the device.
        :return Generic Port Channel
        """

        BaseResource.__init__(self, resource_model=resource_model, name=name, relative_address=relative_address,
                              unique_id=unique_id)
        self.attributes = {
            'Associated Ports': associated_ports,
            'IPv4 Address': ipv4_address,
            'IPv6 Address': ipv6_address,
            'Port Description': port_description}

    @property
    def associated_ports(self):
        return self.attributes['Associated Ports']

    @associated_ports.setter
    def associated_ports(self, value):
        self.attributes['Associated Ports'] = value

    @property
    def ipv4_address(self):
        return self.attributes['IPv4 Address']

    @ipv4_address.setter
    def ipv4_address(self, value):
        self.attributes['IPv4 Address'] = value

    @property
    def ipv6_address(self):
        return self.attributes['IPv6 Address']

    @ipv6_address.setter
    def ipv6_address(self, value):
        self.attributes['IPv6 Address'] = value

    @property
    def port_description(self):
        return self.attributes['Port Description']

    @port_description.setter
    def port_description(self, value):
        self.attributes['Port Description'] = value
