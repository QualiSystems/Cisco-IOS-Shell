__author__ = 'g8y3e'

from abc import ABCMeta
from abc import abstractmethod

class FirmwareData:
    __metaclass__ = ABCMeta

    def __init__(self, file_path):
        result_parse = self._parseFilePath(file_path)

        self._file_path = file_path

        if not result_parse is None:
            self._name = result_parse[0]
            self._extension = result_parse[1]
        else:
            self._name = None
            self._extension = None

    @abstractmethod
    def _parseFilePath(self, file_path):
        """
        :param file_path:
        :return: need to return tuple, were 0 - name, 1 - version, 2 - extension
        """
        pass

    @abstractmethod
    def isValidVersion(self):
        pass

    @abstractmethod
    def isValidExtension(self):
        pass

    def getFilePath(self):
        return self._file_path

    def getName(self):
        return self._name

    def getExtension(self):
        return self._extension