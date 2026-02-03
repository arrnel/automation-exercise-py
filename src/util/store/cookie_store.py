import threading
from http.cookiejar import CookieJar
from typing import Iterable, Dict, Optional

from httpx import Cookies, Response
from httpx._types import CookieTypes

from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class ThreadSafeCookieStore:
    _instance: Optional["ThreadSafeCookieStore"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cookie_store = {}
        return cls._instance

    def _get_test_id(self) -> str:
        return ThreadSafeTestThreadsStore().current_thread_test_name()

    def _ensure_test_bucket(self, test_id: str):
        if test_id not in self._cookie_store:
            self._cookie_store[test_id] = {}

    def get_cookie(self, name: str) -> Optional[str]:
        test_id = self._get_test_id()
        bucket = self._cookie_store.get(test_id, {})
        return bucket.get(name)

    def get_cookies(self, title: str, *titles: str) -> Dict[str, str]:
        bucket = self._cookie_store.get(self._get_test_id(), {})
        return {t: value for t, value in bucket.items() if t in {title, *titles}}

    def get_test_cookies(self) -> Dict[str, str]:
        return dict(self._cookie_store.get(self._get_test_id(), {}))

    def get_all_tests_cookies(self) -> Dict[str, Dict[str, str]]:
        return {tid: dict(cookies) for tid, cookies in self._cookie_store.items()}

    def add_or_update_cookie(self, name: str, value: str):
        test_id = self._get_test_id()
        with self._lock:
            self._ensure_test_bucket(test_id)
            self._cookie_store[test_id][name] = value

    def add_or_update_cookies(self, cookies: Dict[str, str]):
        test_id = self._get_test_id()
        with self._lock:
            self._ensure_test_bucket(test_id)
            for name, value in cookies.items():
                self._cookie_store[test_id][name] = value

    def update_from_response(self, response: Response):

        def update(test_id: str, cookie_jar: CookieJar):
            for c in cookie_jar:
                self._cookie_store[test_id][c.name] = c.value

        test_id = self._get_test_id()
        with self._lock:
            self._ensure_test_bucket(test_id)

            # Save cookies if response has redirects
            if response.history:
                for h in response.history:
                    if h.cookies:
                        update(test_id, h.cookies.jar)

            # Save final cookies
            if response.cookies:
                update(test_id, response.cookies.jar)

    def update_cookies(self, cookies: CookieTypes):
        test_id = self._get_test_id()
        with self._lock:
            self._ensure_test_bucket(test_id)

            if isinstance(cookies, Cookies) or isinstance(cookies, dict):
                for name, value in cookies.items():
                    self._cookie_store[test_id][name] = value

            elif isinstance(cookies, CookieJar):
                for c in cookies:
                    self._cookie_store[test_id][c.name] = c.value

            elif isinstance(cookies, list):
                for item in cookies:
                    if not (isinstance(item, tuple) and len(item) == 2):
                        raise ValueError(f"Unsupported list item: {item}")
                    name, value = item
                    self._cookie_store[test_id][name] = value
            else:
                raise TypeError(f"Unsupported cookies type: {type(cookies)}")

    def remove_cookies(self, names: Iterable[str]):
        test_id = self._get_test_id()
        with self._lock:
            if test_id in self._cookie_store:
                for name in names:
                    self._cookie_store[test_id].pop(name, None)

    def clear_test_cookies(self):
        with self._lock:
            self._cookie_store[self._get_test_id()] = {}

    def export_as_httpx_cookies(self) -> Cookies:
        cookie_dict = self._cookie_store.get(self._get_test_id(), {})
        return Cookies(cookie_dict)
