from typing import Any

from selenium.webdriver import Remote
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config.browser.base_driver_strategy import RemoteDriverStrategy
from src.config.config import CFG
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class RemoteFirefoxDriverStrategy(RemoteDriverStrategy):

    def _create_driver(self) -> Remote:
        options = self.firefox_options
        return Remote(
            command_executor=CFG.remote_url,
            options=options,
        )

    @property
    def firefox_options(self) -> FirefoxOptions:
        options = FirefoxOptions()

        options.set_capability("browserVersion", CFG.browser_version)
        options.set_capability("pageLoadStrategy", CFG.browser_page_load_strategy)
        options.set_capability(
            "timeouts",
            {
                "implicit": CFG.browser_timeout,
                "pageLoad": CFG.browser_page_load_timeout,
                "script": CFG.browser_page_load_timeout,
            },
        )

        for arg in self._browser_args():
            options.add_argument(arg)

        for key, value in self._browser_prefs().items():
            options.set_preference(key, value)

        self.remote_capabilities(options)
        return options

    def _browser_args(self) -> list[str]:
        args = [
            f"--width={CFG.browser_size[0]}",
            f"--height={CFG.browser_size[1]}",
            "--no-sandbox",
        ]

        if CFG.browser_headless:
            args.append("--headless")

        return args

    def _browser_prefs(self) -> dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "browser.tabs.warnOnClose": False,
            "browser.download.dir": f"{CFG.browser_download_dir}/{test_name}",
            # "browser.download.useDownloadDir": True,
            "signon.rememberSignons": False,
            "extensions.formautofill.creditCards.enabled": False,
            "dom.webnotifications.enabled": False,
            "intl.accept_languages": "en,en-US",
        }

    def remote_capabilities(self, options: FirefoxOptions) -> None:
        if CFG.remote_type == "selenoid":
            options.set_capability("selenoid:options", self._selenoid_options())
        elif CFG.remote_type == "moon":
            options.set_capability("moon:options", self._moon_options())
