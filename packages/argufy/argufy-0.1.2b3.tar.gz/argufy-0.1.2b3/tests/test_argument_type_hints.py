# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test arguments.'''

import sys
from inspect import getmembers, isfunction, signature

from docstring_parser import parse

from argufy import Argument

module = sys.modules[__name__]


def argument_type_hints_simple(check: int) -> None:
    '''Example demonstrating minimal CLI.'''
    pass


def test_argument_type_hints_simple() -> None:
    '''Test simple argument.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_type_hints_simple'
    ][0]
    sig = signature(fn)
    docstring = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        document = next(
            (d for d in docstring.params if d.arg_name == arg), None
        )
        arguments.append(
            Argument(parameters=sig.parameters[arg], docstring=document)
        )
    # print('Arguments: ', arguments[0].__dict__)
    assert not hasattr(arguments[0], 'default')
    # assert arguments[0].metavar == 'INT'


def argument_type_hints_bool(
    check_false: bool = False, check_true: bool = True
) -> None:
    '''Example bool.'''
    pass


def test_argument_type_hints_bool() -> None:
    '''Test simple boolean.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_type_hints_bool'
    ][0]
    sig = signature(fn)
    docstring = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        document = next(
            (d for d in docstring.params if d.arg_name == arg), None
        )
        arguments.append(
            Argument(parameters=sig.parameters[arg], docstring=document)
        )
    # print(arguments[0].__dict__)
    assert arguments[0].default is False
    assert arguments[1].default is True


def argument_type_hints_all(
    string_check: str = 'A',
    bool_check: bool = False,
    integer_check: int = 1,
    float_check: float = 1.5,
    list_check: list = ['A'],
    set_check: set = {'a'},
    tuple_check: tuple = ('A',),
    # file_check: open = 'test.toml',
) -> None:
    '''Example full.'''
    pass


def test_argument_type_hints_all() -> None:
    '''Test full type set.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_type_hints_all'
    ][0]
    sig = signature(fn)
    document = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        docstring = next(
            (d for d in document.params if d.arg_name == arg), None
        )
        arguments.append(
            Argument(parameters=sig.parameters[arg], docstring=docstring)
        )
    # print(arguments[0].__dict__)
    assert arguments[0].type == str
    assert arguments[0].default == 'A'

    # print(arguments[1].__dict__)
    # NOTE: Argparse does not store bool type
    assert not hasattr(arguments[1], 'type')
    assert arguments[1].default is False

    # print(arguments[2].__dict__)
    assert arguments[2].type == int
    assert arguments[2].default == 1

    # print(arguments[3].__dict__)
    assert arguments[3].type == float
    assert arguments[3].default == 1.5

    # print(arguments[4].__dict__)
    # assert arguments[4].type == list
    assert arguments[4].default == ['A']

    # print(arguments[5].__dict__)
    # assert arguments[5].type == set
    assert arguments[5].default == {'a'}

    # print(arguments[6].__dict__)
    # assert arguments[6].type == tuple
    assert arguments[6].default == ('A',)
