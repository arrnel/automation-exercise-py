from urllib.parse import urlparse

from selene import browser

from src.config.config import CFG
from src.util import time_util

_HOSTNAME = urlparse(CFG.base_url).hostname


class CookieUtil:

    @staticmethod
    def add_app_cookie(name: str, value: str) -> None:
        browser.driver.add_cookie(
            {
                "name": name,
                "value": value,
                "expiry": time_util.next_year_unix_datetime(),
                "path": "/",
                "domain": _HOSTNAME,
                "secure": False,
                "httpOnly": False,
                "sameSite": "Lax",
            }
        )

    @staticmethod
    def add_cookies_to_browser(cookies: dict) -> None:
        for name, value in cookies.items():
            if value is not None:
                if browser.driver.get_cookie(name):
                    browser.driver.delete_cookie(name)
                CookieUtil.add_app_cookie(name, value)
