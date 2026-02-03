from httpx import Response

from src.client.core.condition.base import Condition
from src.client.core.extractor import Extractor


class AssertableResponse:

    def __init__(self, response: Response):
        self.response = response

    def check(self, condition: Condition, *conditions: Condition) -> "AssertableResponse":

        invalid_checks = []
        all_conditions = [condition, *conditions]
        for c in all_conditions:
            c_status, c_msg = c.check(self.response)
            if not c_status:
                invalid_checks.append(f"\n{len(invalid_checks) + 1}. {c_msg}")

        if invalid_checks:
            raise AssertionError(f"{''.join(invalid_checks)}\n")
        return self

    def extract(self) -> Extractor:
        return Extractor(self.response)
