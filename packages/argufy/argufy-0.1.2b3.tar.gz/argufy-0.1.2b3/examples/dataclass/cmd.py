# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
"""Test parser.

Attributes
----------
variable: str
    Example variable for testing

"""

from .config import Settings

variable = 'ex_var'


# def print_variable() -> None:
#     """Print example variable."""
#     print('example_varible', variable)


def example_settings(settings: Settings, clear: bool = False) -> None:
    """Demonstrate example settings."""
    # Parameters
    # ----------
    # bool_check: settings
    #     example boolean

    # """
    print(settings, clear)
