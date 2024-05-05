#!/usr/bin/python3
"""Simple argparse."""

import sys

from argufy import Parser

module = sys.modules[__name__]


def switch():  # type: ignore
    """Empty function to check switch."""
    print('test empty switch')


def positional(test: str):  # type: ignore
    """Run example positional."""
    print(test)


def example_bool(bool_check=False):  # type: ignore
    """Run example bool."""
    print(bool_check)


def example_choice(choice_check='A'):  # type: ignore
    """Run example choice."""
    print(choice_check)


parser = Parser(version='1.2.3')
parser.add_commands(module)
parser.dispatch()
