from urllib.parse import urlparse

from selene import browser

from src.config.config import CFG

_HOSTNAME = urlparse(CFG.base_url).hostname


class CookieUtil:

    @staticmethod
    def add_app_cookie(name: str, value: str) -> None:
        browser.driver.add_cookie(
            {
                "name": name,
                "value": value,
                "path": "/",
                "domain": _HOSTNAME,
                "secure": False,
                "httpOnly": False,
                "sameSite": "Lax",
            }
        )

    @staticmethod
    def add_app_cookies(cookies: dict) -> None:
        for name, value in cookies.items():
            if value is not None:
                CookieUtil.add_app_cookie(name, value)
