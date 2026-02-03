from selene import Element, query
from selene.common import predicate
from selene.core.condition import Condition
from selene.core.conditions import ElementCondition


def text_in(expected_texts: set[str]) -> Condition[Element]:
    return ElementCondition.raise_if_not_actual(
        f"text in: {expected_texts}",
        query.text,
        predicate.includes,
    )


def value_in(expected_values: set[str]) -> Condition[Element]:
    return ElementCondition.raise_if_not_actual(
        f"value in: {expected_values}",
        query.value,
        predicate.includes,
    )
