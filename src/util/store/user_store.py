import logging
import threading
from typing import List, Optional

from src.model.user import User
from src.service.user_api_service import UserApiService
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore

GLOBAL_USERS_KEY = "GLOBAL_USERS"


class ThreadSafeUserStore:
    """Thread-safe user storage"""

    _instance = None
    _lock = threading.Lock()
    _users_store: dict[str, dict[str, User]] = {}
    _not_removed_users: list[User] = []
    _storage_lock = threading.RLock()
    _user_service = UserApiService()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _get_key() -> str:
        return ThreadSafeTestThreadsStore().current_thread_test_name()

    def add_user(self, user: User) -> None:
        test_id = self._get_key()
        with self._storage_lock:
            if test_id not in self._users_store:
                self._users_store[test_id] = {}
            self._users_store[test_id][user.email] = user

    def add_users(self, *users: User) -> None:
        test_id = self._get_key()
        with self._storage_lock:
            if test_id not in self._users_store:
                self._users_store[test_id] = {}
            for user in users:
                self._users_store[test_id][user.email] = user

    def get_user(self, email: str) -> Optional[User]:
        test_id = self._get_key()
        with self._storage_lock:
            return self._users_store.get(test_id, {}).get(email)

    def get_users(self) -> List[User]:
        test_id = self._get_key()
        with self._storage_lock:
            return list(self._users_store.get(test_id, {}).values())

    def get_all_users_as_list(self) -> List[User]:
        with self._storage_lock:
            users: list[User] = []
            for user_dict in self._users_store.values():
                users.extend(user_dict.values())
            return users

    def update_user(self, email: str, new_user: User) -> bool:
        test_id = self._get_key()
        with self._storage_lock:
            users = self._users_store.get(test_id, {})
            if email in users:
                users[email] = new_user
                return True
            return False

    def remove_test_users(self) -> None:
        with self._storage_lock:
            self._remove_users_from_backend(self.get_users())
            if self._get_key() in self._users_store:
                del self._users_store[self._get_key()]

    def remove_all_tests_users(self) -> None:
        with self._storage_lock:
            self._remove_users_from_backend(self.get_all_users_as_list())
            try:
                self._users_store.clear()
            except KeyError:
                logging.info(
                    f"Failed to delete users. Thread key = [{self._get_key()}] not exists."
                )

    def _remove_users_from_backend(self, users: list[User]):

        if users:

            for user in users:

                try:
                    self._user_service.delete_user(user.email, user.test_data.password)
                except Exception:
                    with self._storage_lock:
                        self._not_removed_users.append(user)

            with self._storage_lock:
                if self._not_removed_users:
                    users_credentials_text = [
                        (
                            f"Email = {user.email}, "
                            f"password = [{user.password}], "
                            f"test_data_password = [{user.test_data.password}]"
                        )
                        for user in self._not_removed_users
                    ]

                    logging.warning(
                        "Failed to remove user(s):\n"
                        + "\n".join(users_credentials_text)
                    )
