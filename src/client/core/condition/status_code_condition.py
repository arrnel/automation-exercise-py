from typing import Tuple

from httpx import Response

from src.client.core.condition.base import Condition


class StatusCodeCondition(Condition):
    def __init__(self, status_code: int):
        self.status_code = status_code

    def check(self, response: Response) -> Tuple[bool, str]:
        expected_status_code = self.status_code
        actual_status_code = response.status_code
        if expected_status_code != actual_status_code:
            return (
                False,
                (
                    "Status code mismatch. "
                    f"Expected = [{expected_status_code}], "
                    f"Actual = [{actual_status_code}]"
                ),
            )
        else:
            return True, ""

    def __str__(self):
        return f"Status code: {self.status_code}"
