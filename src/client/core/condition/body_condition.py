from collections import Counter
from typing import Tuple

from httpx import Response

from src.client.core.condition.base import Condition
from src.client.core.extractor import Extractor
from src.util.api.json_path_util import matches_by_json_path


class BodyFieldExistsCondition(Condition):

    def __init__(self, path: str):
        self.path = path

    def check(self, response: Response) -> Tuple[bool, str]:
        try:
            response.json().get(self.path)
            return True, ""
        except Exception:
            return (
                False,
                f"Body field '{self.path}' not found",
            )

    def __str__(self):
        return f"Body field '{self.path}' exists"


class BodyFieldEqualsCondition(Condition):

    def __init__(self, path: str, expected_value):
        self.path = path
        self.expected = expected_value

    def check(self, response: Response) -> Tuple[bool, str]:
        actual = Extractor(response).as_value(self.path)
        if actual == self.expected:
            return True, ""
        else:
            return (
                False,
                (
                    f"Body field '{self.path}' value mismatch.\b"
                    f"Expected = [{self.expected}]\b"
                    f"Actual = [{actual}]\b"
                ),
            )

    def __str__(self):
        return f"Body field '{self.path}' has value = [{self.expected}]"


class BodyFieldNotEqualsCondition(Condition):

    def __init__(self, path: str, expected_value, *expected_values):
        self.path = path
        self.expected = [expected_value, *expected_values]
        if len(self.expected) == 0:
            self.text = f"equals: {self.expected[0]}"
        else:
            self.text = f"in: {str(self.expected)}"

    def check(self, response: Response) -> Tuple[bool, str]:
        actual = Extractor(response).as_value(self.path)
        if actual in self.expected:
            return (
                False,
                f"Body field value '{self.path}' mismatch.\n"
                f"Expected not {self.text}\n"
                f"Actual: {actual}",
            )
        else:
            return True, ""

    def __str__(self):
        return f"Body field '{self.path}' value should not {self.text}"


class BodyArrayHasSizeCondition(Condition):

    def __init__(self, path: str, count: int):

        if count <= 0:
            raise ValueError("Count must be greater than 0")

        self.path = path
        self.expected = count

    def check(self, response: Response) -> Tuple[bool, str]:
        body = response.json()
        actual = len(matches_by_json_path(body, self.path))

        if self.expected != actual:
            return (
                False,
                (
                    f"Invalid body array size: [{self.path}]. "
                    f"Expected = [{self.expected}],"
                    f"actual = [{actual}]"
                ),
            )
        else:
            return True, ""

    def __str__(self):
        return f"Body array '{self.path}' has size: [{self.expected}]"


class BodyArrayIsEmptyCondition(Condition):

    def __init__(self, path: str):

        if not path.endswith("[*]"):
            raise ValueError("Invalid path. Path should ends with '[*]'")

        self.path = path

    def check(self, response: Response) -> Tuple[bool, str]:
        body = response.json()
        actual = matches_by_json_path(body, self.path)

        if not actual:
            return True, ""
        else:
            return (
                False,
                f"Body array should be empty. Path: {self.path}",
            )

    def __str__(self):
        return f"Body array '{self.path}' should be empty"


class BodyArrayContainsCondition(Condition):

    def __init__(self, path: str, expected_value, *expected_values):
        self.path = path
        self.expected = [expected_value, *expected_values]

    def check(self, response: Response) -> Tuple[bool, str]:
        body = response.json()
        actual = matches_by_json_path(body, self.path)

        missing = [v for v in self.expected if v not in actual]

        if missing:
            return False, (
                f"Body array '{self.path}' not contains values:\n"
                f"Missing: {missing}.\n"
                f"Expected: {self.expected}\n"
                f"Actual: {actual}"
            )
        else:
            return True, ""

    def __str__(self):
        return f"Array at '{self.path}' contains: {self.expected}"


class BodyArrayNotContainsCondition(Condition):

    def __init__(self, path: str, expected_value, *expected_values):
        self.path = path
        self.expected = [expected_value, *expected_values]

    def check(self, response: Response) -> Tuple[bool, str]:
        body = response.json()
        actual = matches_by_json_path(body, self.path)

        exist = [v for v in self.expected if v in actual]

        if exist:
            return False, (
                f"Body array '{self.path}' not contains values:\n"
                f"Contains: {exist}.\n"
                f"Expected: {self.expected}\n"
                f"Actual: {actual}"
            )
        else:
            return True, ""

    def __str__(self):
        return f"Array at '{self.path}' not contains: {self.expected}"


class BodyArrayHasCondition(Condition):

    def __init__(self, path: str, expected_value, *expected_values):
        self.path = path
        self.expected = [expected_value, *expected_values]

    def check(self, response: Response) -> Tuple[bool, str]:
        actual = matches_by_json_path(response.json(), self.path)

        if len(self.expected) != len(actual):
            return (
                False,
                (
                    "Different elements count. "
                    f"Expected = [{len(self.expected)}], "
                    f"Actual = [{len(actual)}]"
                ),
            )

        counter_actual = Counter(actual)
        counter_expected = Counter(self.expected)
        diff = list((counter_actual - counter_expected).elements())
        if diff:
            return False, (
                f"Body array '{self.path}' has diff:\n"
                f"Diff: {diff}.\n"
                f"Expected: {self.expected}\n"
                f"Actual: {actual}"
            )
        else:
            return True, ""

    def __str__(self):
        return f"Array at '{self.path}' has: {self.expected}"


class BodyArrayHasOrderedCondition(Condition):

    def __init__(self, path: str, expected_value, *expected_values):
        self.path = path
        self.expected = [expected_value, *expected_values]

    def check(self, response: Response) -> Tuple[bool, str]:
        actual = matches_by_json_path(response.json(), self.path)

        if len(self.expected) != len(actual):
            return (
                False,
                (
                    "Different elements count. "
                    f"Expected = [{len(self.expected)}], "
                    f"Actual = [{len(actual)}]"
                ),
            )
        elif actual != self.expected:
            return False, (
                f"Body array '{self.path}' has diff:\n"
                f"Expected: {self.expected}\n"
                f"Actual: {actual}"
            )
        else:
            return True, ""

    def __str__(self):
        return f"Array at '{self.path}' has ordered: {self.expected}"
