from abc import ABC, abstractmethod
from typing import Tuple

from httpx import Response


class Condition(ABC):

    @abstractmethod
    def check(self, response: Response) -> Tuple[bool, str]:
        pass
