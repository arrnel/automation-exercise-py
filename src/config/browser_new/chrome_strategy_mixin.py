from abc import abstractmethod, ABCMeta
from typing import List, Any

from selenium.webdriver.chrome.options import Options


class ChromeStrategyMixin(metaclass=ABCMeta):

    def _build_chrome_options(self) -> Options:
        options = Options()
        self._set_chrome_args(options)
        self._set_experimental_options(options)
        self._set_capabilities(options, self.capabilities())
        return options

    @abstractmethod
    def chrome_args(self) -> List[str]:
        pass

    @abstractmethod
    def chrome_experimental_options(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def capabilities(self) -> dict[str, Any]:
        pass

    def _set_chrome_args(self, options: Options) -> None:
        for arg in self.chrome_args():
            options.add_argument(arg)

    def _set_experimental_options(self, options: Options) -> None:
        for key, value in self.chrome_experimental_options().items():
            options.add_experimental_option(key, value)

    def _set_capabilities(self, options: Options, capabilities: dict[str, Any]) -> None:
        for key, value in capabilities.items():
            options.set_capability(key, value)
