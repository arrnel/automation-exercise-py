from abc import ABC, abstractmethod


class DriverManager(ABC):

    @abstractmethod
    def create_driver(self):
        raise NotImplementedError