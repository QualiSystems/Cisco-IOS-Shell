__author__ = 'g8y3e'

from firmware_data import FirmwareData


class CiscoFirmwareData(FirmwareData):
    def _parse_file_path(self, file_path):
        """
        :param file_path:
        :return: need to return tuple, were 0 - name, 1 - version, 2 - extension
        """
        file_path_parts = file_path.split('/')

        #if len(file_path_parts) == 1:
        #    return None

        firmware_title = file_path_parts[-1]
        firmware_title_parts = firmware_title.split('.')

        name = ''
        for index in range(0, len(firmware_title_parts) - 1):
            name += firmware_title_parts[index] + '.'
        name = name[:-1]

        extension = firmware_title_parts[-1]

        return name, extension

    def is_valid_version(self):
        return True

    def is_valid_extension(self):
        return self._extension == 'bin'
