import logging
import threading
from typing import List, Optional

import pytest

from src.model.user import User
from src.service.user_api_service import UserApiService

GLOBAL_USERS_KEY = "GLOBAL_USERS"


class ThreadSafeTestThreadsStore:
    """Thread-safe test threads storage"""

    _instance = None
    _lock = threading.Lock()
    _test_threads_store: dict[str, list[int]] = {}
    _storage_lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _get_thread_id() -> int:
        return threading.get_ident()

    def add_current_thread_to_test(self, test_name: str):
        with self._storage_lock:
            if self._test_threads_store.get(test_name) is None:
                self._test_threads_store[test_name] = []
            thread_id = self._get_thread_id()
            if thread_id not in self._test_threads_store.get(test_name):
                self._test_threads_store[test_name].append(thread_id)

    def get_current_thread_test_name(self) -> Optional[str]:
        thread_id = threading.get_ident()
        with self._storage_lock:
            for test_name, thread_ids in self._test_threads_store.items():
                if thread_id in thread_ids:
                    return test_name
            return None

    def clear_test_threads(self, test_name: str) -> None:
        with self._storage_lock:
            if test_name in self._test_threads_store:
                del self._test_threads_store[test_name]
