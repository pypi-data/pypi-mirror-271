from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


class IPersistenceManager(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def save(path, encoded_data):
        pass

    @staticmethod
    @abstractmethod
    def load(path):
        pass


@dataclass
class INode(metaclass=ABCMeta):
    char: str
    freq: int

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass


class IEncoder(metaclass=ABCMeta):
    @abstractmethod
    def encode_string(self, encoding_table, message):
        pass

    @abstractmethod
    def decode_string(self, encoding_table, encoded_message):
        pass
