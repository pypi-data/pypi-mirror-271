# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore

'''Test parser.

Attributes
----------
check_attribute: bool
    Check document attributes

'''

from ast import literal_eval

import pytest
import sys

from argufy import __version__, Parser

sys.path.append('.')
import command_parser  # noqa: E402
# module = sys.modules[__name__]


def test_help():
    '''Do help function for CLI.'''
    parser = Parser(version=__version__)
    parser.add_commands(command_parser, exclude_prefixes=['test_'])
    with pytest.raises(SystemExit) as blank_err:
        parser.dispatch([])
    assert blank_err.type == SystemExit
    with pytest.raises(SystemExit) as help_err:
        parser.dispatch(['--help'])
    assert help_err.type == SystemExit
    assert blank_err.value.code == help_err.value.code


def test_bool(capsys):
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_commands(command_parser, exclude_prefixes=['test_'])
    parser.dispatch(['example-bool', '--bool-check'])
    capture = capsys.readouterr()
    assert literal_eval(capture.out) is True


def test_choice(capsys):
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_commands(command_parser, exclude_prefixes=['test_'])
    parser.dispatch(['example-choice', '--choice-check', 'B'])
    capture = capsys.readouterr()
    assert literal_eval(capture.out) is True
