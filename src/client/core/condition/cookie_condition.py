from typing import Tuple

from httpx import Response

from src.client.core.condition.base import Condition


class CookieExistsCondition(Condition):

    def __init__(self, expected_cookie: str, *expected_cookies: str):
        self.expected = [expected_cookie, *expected_cookies]

    def check(self, response: Response) -> Tuple[bool, str]:
        actual = {c.casefold() for c in response.cookies.keys()}
        missing = [
            cookie for cookie in self.expected if cookie.casefold() not in actual
        ]
        if missing:
            return True, (
                f"Cookies not found: {missing}\n"
                f"Expected cookies: {self.expected}\n"
                f"Actual cookies: {actual}"
            )
        else:
            return True, ""

    def __str__(self):
        return f"Cookies exist: {self.expected}"


class CookiesHasValueCondition(Condition):

    def __init__(self, cookies: dict):
        self.cookies = cookies

    def check(self, response: Response) -> Tuple[bool, str]:
        response_cookies = {k.casefold(): v for k, v in response.cookies.items()}

        missing = []
        wrong_values = []

        for key, expected_value in self.cookies.items():
            key_cf = key.casefold()

            if key_cf not in response_cookies:
                missing.append(key)
                continue

            actual_value = response_cookies[key_cf]
            if actual_value != expected_value:
                wrong_values.append((key, expected_value, actual_value))

        if missing or wrong_values:
            wrong_cookies_kv = ", ".join(
                f"{k}: expected={e}, actual={a}" for k, e, a in wrong_values
            )
            return False, (
                f"Cookies mismatch:"
                f"Missing cookies: {missing}"
                f"Wrong value cookies: {wrong_cookies_kv}"
            )
        else:
            return True, ""

    def __str__(self):
        return "Cookies have expected values: " + ", ".join(
            f"{k}={v}" for k, v in self.cookies.items()
        )
