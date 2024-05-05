# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
'''Test restructured arguments.'''

import sys
from inspect import getmembers, isfunction, signature

from docstring_parser import parse

from argufy import Argument

module = sys.modules[__name__]


def argument_restructured_bool(check_false=False, check_true=True):
    '''Mock restructured example bool.

    :param bool_check: list packages and v1ersion
    :type bool_check: bool

    '''
    pass


def test_argument_restructured_bool():
    '''Test restructured example boolean.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_restructured_bool'
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


def argument_restructured_choice(choice='A'):
    '''Mock restructured example choice.

    {'A','B','C'}

    :param choice: argument choice
    :type str: choice

    '''
    pass


def test_argument_restructured_choice():
    '''Test restructured choices.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_restructured_choice'
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
    assert arguments[0].help == 'argument choice'
    assert arguments[0].default == 'A'


def argument_restructured_all(
    string_check='A',
    bool_check=False,
    integer_check=1,
    float_check=1.5,
    list_check=['A'],
    set_check={'a'},
    tuple_check=('A',),
    # file_check='test.toml',
):
    '''Mock restructured full type set.

    :param string_check: argument string
    :type string_check: str
    :param bool_check: argument bool
    :type bool_check: bool
    :param integer_check: argument int
    :type integer_check: int
    :param float_check: argument float
    :type float_check: float
    :param list_check: argument list
    :type list_check: list
    :param set_check: argument set
    :type set_check: set
    :param tuple_check: argument tuple
    :type tuple_check: tuple

    '''
    pass


def test_argument_restructured_all():
    '''Test restructured full type set.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_restructured_all'
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
    assert arguments[0].help == 'argument string'
    # assert arguments[0].type == str
    assert arguments[0].default == 'A'

    # print(arguments[1].__dict__)
    assert arguments[1].help == 'argument bool'
    # NOTE: Argparse does not store bool type
    # assert not hasattr(arguments[1], 'type')
    assert arguments[1].default is False

    # print(arguments[2].__dict__)
    assert arguments[2].help == 'argument int'
    # assert arguments[2].type == int
    assert arguments[2].default == 1

    # print(arguments[3].__dict__)
    assert arguments[3].help == 'argument float'
    # assert arguments[3].type == float
    assert arguments[3].default == 1.5

    # print(arguments[4].__dict__)
    assert arguments[4].help == 'argument list'
    # assert arguments[4].type == list
    assert arguments[4].default == ['A']

    # print(arguments[5].__dict__)
    assert arguments[5].help == 'argument set'
    # assert arguments[5].type == set
    assert arguments[5].default == {'a'}

    # print(arguments[6].__dict__)
    assert arguments[6].help == 'argument tuple'
    # assert arguments[6].type == tuple
    assert arguments[6].default == ('A',)
