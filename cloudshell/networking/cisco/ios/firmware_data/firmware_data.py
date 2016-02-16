__author__ = 'g8y3e'

from abc import ABCMeta
from abc import abstractmethod


class FirmwareData:
    __metaclass__ = ABCMeta

    def __init__(self, file_path):
        result_parse = self._parse_file_path(file_path)

        self._file_path = file_path

        if result_parse is not None:
            self._name = result_parse[0]
            self._extension = result_parse[1]
        else:
            self._name = None
            self._extension = None

    @abstractmethod
    def _parse_file_path(self, file_path):
        """
        :param file_path:
        :return: need to return tuple, were 0 - name, 1 - version, 2 - extension
        """
        pass

    @abstractmethod
    def is_valid_version(self):
        pass

    @abstractmethod
    def is_valid_extension(self):
        pass

    def get_file_path(self):
        return self._file_path

    def get_name(self):
        return self._name

    def get_extension(self):
        return self._extension
