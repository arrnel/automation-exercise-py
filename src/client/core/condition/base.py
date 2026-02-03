from abc import ABC, abstractmethod
from typing import Tuple

from httpx import Response


class Condition(ABC):

    @abstractmethod
    def check(self, response: Response) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()
