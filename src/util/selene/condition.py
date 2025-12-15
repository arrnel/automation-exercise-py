from selene import Element, query
from selene.common import predicate
from selene.core.conditions import ElementCondition

from src.client.core.condition.base import Condition


def text_in(
    expected: set[str],
) -> Condition[Element]:
    return ElementCondition.raise_if_not_actual(
        f"text in: {expected}",
        query.text,
        predicate.includes,
    )

def value_in(
    expected: set[str],
) -> Condition[Element]:
    return ElementCondition.raise_if_not_actual(
        f"text in: {expected}",
        query.value,
        predicate.includes,
    )