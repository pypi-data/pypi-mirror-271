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
import sys

import pytest

from argufy import __version__, Parser

sys.path.append('.')
import subcommands_parser  # noqa: E402


def test_help():
    '''Do help function for CLI.'''
    # NOTE: getting varying results
    # 0 displays help
    # 2 dumps error (invalid choice)

    parser = Parser(__version__, command_type='subcommand')
    parser.add_commands(subcommands_parser, exclude_prefixes=['test_'])

    with pytest.raises(SystemExit) as blank_err:
        parser.dispatch([])
    assert blank_err.type == SystemExit

    with pytest.raises(SystemExit) as help_err:
        parser.dispatch(['--help'])
    assert help_err.type == SystemExit
    assert help_err.type == blank_err.type

    with pytest.raises(SystemExit) as err:
        parser.dispatch(['subcommands-parser', 'example-bool', '--help'])
    assert err.type == SystemExit
    assert err.value.code == 0


def test_bool(capsys):
    '''Do main function for CLI.'''
    parser = Parser(command_type='subcommand')
    parser.add_commands(subcommands_parser, exclude_prefixes=['test_'])
    parser.dispatch([
        'subcommands-parser',
        'example-bool',
        '--bool-check',
    ])
    capture = capsys.readouterr()
    assert literal_eval(capture.out) is True


def test_choice(capsys):
    '''Do main function for CLI.'''
    parser = Parser(command_type='subcommand')
    parser.add_commands(subcommands_parser, exclude_prefixes=['test_'])
    parser.dispatch([
        'subcommands-parser',
        'example-choice',
        '--choice-check',
        'B',
    ])
    capture = capsys.readouterr()
    assert literal_eval(capture.out) is True
