from abc import ABCMeta, abstractmethod


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse_data(self):
        pass


class LPParser(Parser):
    def parse_data(self):
        pass


class TOUParser(Parser):
    def parse_data(self):
        pass
