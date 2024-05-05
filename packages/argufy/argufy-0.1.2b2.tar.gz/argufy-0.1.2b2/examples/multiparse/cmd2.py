# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
"""Test parser."""

from . import builder

_settings = builder()


def example_builder() -> None:
    """Demonstrate variable imported from config."""
    print('---', _settings, '---')


def example_args(*args_check: str) -> None:
    """Demonstrate example arguments.

    Parameters
    ----------
    args_check: str
        example arguments

    """
    print(args_check)


def example_kwargs(**kwargs: str) -> None:
    """Demonstrate example keyword arguments.

    Parameters
    ----------
    variable_one: str
        variable one

    variable_test: str
        variable two

    variable_three: str
        variable three

    """
    if kwargs.get('variable_one'):
        print(kwargs['variable_one'])

    if kwargs.get('variable_two'):
        print(kwargs['variable_two'])

    if kwargs.get('variable_three'):
        print(kwargs['variable_three'])
