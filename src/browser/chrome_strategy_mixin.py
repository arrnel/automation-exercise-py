from abc import abstractmethod, ABCMeta
from pathlib import Path
from typing import List, Any

from selenium.webdriver.chrome.options import Options

from src.config.config import CFG


class ChromeStrategyMixin(metaclass=ABCMeta):

    def _build_chrome_options(self) -> Options:
        options = Options()
        self.__set_chrome_args(options)
        self.__install_extensions(options)
        self.__set_experimental_options(options)
        self.__set_capabilities(options)
        return options

    @abstractmethod
    def chrome_args(self) -> List[str]:
        pass

    @abstractmethod
    def chrome_experimental_options(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def chrome_extensions(self) -> List[str]:
        pass

    @abstractmethod
    def capabilities(self) -> dict[str, Any]:
        pass

    def __set_chrome_args(self, options: Options) -> None:
        for arg in self.chrome_args():
            options.add_argument(arg)

    def __set_experimental_options(self, options: Options) -> None:
        options.add_experimental_option("prefs", self.chrome_experimental_options())

    def __install_extensions(self, options: Options) -> None:
        """
        Install chrome extensions.
        Extensions for Chrome version greater than 142 installing in driver
        """
        browser_version = float(CFG.browser_version)

        if browser_version >= 137.0:
            options.add_argument(
                "--disable-features=DisableLoadExtensionCommandLineSwitch"
            )

        for extension in self.chrome_extensions():
            path = Path(extension)

            if not path.exists():
                raise FileNotFoundError(f"Extension path does not exist: {str(path)}")
            if path.is_file():
                options.add_extension(str(path))
            elif path.is_dir() and browser_version < 142.0:
                options.add_argument(f"--load-extension={str(path)}")

    def __set_capabilities(self, options: Options) -> None:
        for key, value in self.capabilities().items():
            options.set_capability(key, value)
