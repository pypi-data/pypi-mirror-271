# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
"""Test parser.

Attributes
----------
example_variable: str
    Example variable for testing

"""

import json  # noqa
from typing import Optional

example_variable = 'ex_var'
optional_variable: Optional[str] = None


def print_variable() -> None:
    """Print example variable."""
    print('example_varible', example_variable)
    print('optional_varible', optional_variable)


def example_bool(bool_check: bool = False) -> None:
    """Demonstrate example bool.

    Parameters
    ----------
    bool_check: bool, optional
        example boolean

    """
    print(bool_check)


def example_choice(choice_check: str = 'A') -> None:
    """Demonstrate example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    """
    print(choice_check)
