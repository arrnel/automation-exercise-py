from abc import ABC, abstractmethod

from selenium import webdriver


class BrowserStrategy(ABC):

    @abstractmethod
    def create_driver(self) -> webdriver.Chrome | webdriver.Firefox | webdriver.Remote:
        pass
