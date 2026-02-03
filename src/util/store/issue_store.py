import threading
from typing import Optional, List

from src.model.enum.github_issue_type import IssueType


class ThreadSafeIssuesStore:
    _instance: Optional["ThreadSafeIssuesStore"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._issues_store = {}
        return cls._instance

    def set_issue_state(self, issue_id: int, status: Optional[IssueType]) -> None:
        with self._lock:
            self._issues_store[issue_id] = status

    def get_issue_state(self, issue_id: int) -> Optional[IssueType]:
        with self._lock:
            return self._issues_store.get(issue_id)

    def get_all_issue_ids(self) -> List[int]:
        with self._lock:
            return list(self._issues_store.keys())
