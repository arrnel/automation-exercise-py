from abc import abstractmethod, ABCMeta
from typing import List, Any

from selenium.webdriver.firefox.options import Options


class FirefoxStrategyMixin(metaclass=ABCMeta):

    def _build_firefox_options(self) -> Options:
        options = Options()
        self.__set_firefox_args(options)
        self.__set_prefs(options)
        self.__set_capabilities(options)
        return options

    @abstractmethod
    def firefox_args(self) -> List[str]:
        pass

    @abstractmethod
    def firefox_prefs(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def capabilities(self) -> dict[str, Any]:
        pass

    def __set_firefox_args(self, options: Options) -> None:
        for arg in self.firefox_args():
            options.add_argument(arg)

    def __set_prefs(self, options: Options) -> None:
        for key, value in self.firefox_prefs().items():
            options.set_preference(key, value)

    def __set_capabilities(self, options: Options) -> None:
        for key, value in self.capabilities().items():
            options.set_capability(key, value)
