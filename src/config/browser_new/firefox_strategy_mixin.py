from abc import abstractmethod, ABCMeta
from typing import List, Any

from selenium.webdriver.firefox.options import Options


class FirefoxStrategyMixin(metaclass=ABCMeta):

    def _build_firefox_options(self) -> Options:
        options = Options()
        self._set_chrome_args(options)
        self._set_prefs(options)
        self._set_capabilities(options, self.capabilities())
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

    def _set_chrome_args(self, options: Options) -> None:
        for arg in self.firefox_args():
            options.add_argument(arg)

    def _set_prefs(self, options: Options) -> None:
        for key, value in self.firefox_prefs().items():
            options.set_preference(key, value)

    def _set_capabilities(self, options: Options, capabilities: dict[str, Any]) -> None:
        for key, value in capabilities.items():
            options.set_capability(key, value)
