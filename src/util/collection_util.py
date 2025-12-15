from collections import Counter
from typing import TypeVar, Iterable

T = TypeVar('T')



def remove_common_duplicates(l1: Iterable[T], l2: Iterable[T]) -> [list[T], list[T]]:
    """
    Remove duplicates from common elements from 2 collections
    Input:  l1 = [0, 1, 4, 2, 3, 2, 1, 2], l2 = [5, 1, 1, 1, 2, 5, 4]
    Result: l1 = [0, 2, 3, 2],          l2 = [5, 1, 5]
    """

    if l1 == l2:
        return [], []

    if not l1 or not l2:
        return list(l1), list(l2)


    count1 = Counter(l1)
    count2 = Counter(l2)
    all_elements = set(l1) | set(l2)

    result_l1 = []
    result_l2 = []

    for elem in all_elements:
        delta = count1.get(elem, 0) - count2.get(elem, 0)
        if delta > 0:
            result_l1.extend([elem] * delta)
        elif delta < 0:
            result_l2.extend([elem] * -delta)

    return result_l1, result_l2