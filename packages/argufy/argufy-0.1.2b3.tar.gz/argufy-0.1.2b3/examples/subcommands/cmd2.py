# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
"""Test parser two.

Attributes
----------
example_variable: str
    Example variable for testing

"""

from typing import List, Tuple

example_variable2 = 'test2'


def example_list(list_check: List[str] = []) -> None:
    """Demonstrate example bool.

    Parameters
    ----------
    list_check: list, optional
        example boolean

    """
    print(list_check)


def example_tuple(tuple_check: Tuple[str, ...] = ('A', 'B', 'C')) -> None:
    """Demonstrate example choice.

    Parameters
    ----------
    tuple_check: tuple, ('A', 'B', 'C')
        example choice

    """
    print(tuple_check)
