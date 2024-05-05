# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
"""Test parser.

Attributes
----------
example_variable: str
    Example variable for testing

"""


def example_args(*args_check: str) -> None:
    """Demonstrate example arguments.

    Parameters
    ----------
    args_check: str
        example arguments

    """
    print(args_check)


def example_kwargs(**kwargs_check: str) -> None:
    """Demonstrate example keyword arguments.

    Parameters
    ----------
    kwargs_check: str, {'A': 'a', 'B': 'b', 'C': 'c'}
        example keyword arguments

    """
    print(kwargs_check)
