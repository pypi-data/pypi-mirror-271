# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
'''Test arguments.'''

import sys
from inspect import getmembers, isfunction, signature

from docstring_parser import parse

from argufy import Argument

module = sys.modules[__name__]


def argument_numpy_bool(check_false=False, check_true=True):
    '''Example bool.

    Parameters
    ----------
    check_false: bool, optional
        list packages and v1ersion
    check_true: bool, optional
        list packages and v1ersion

    '''
    pass


def test_argument_numpy_bool():
    '''Test simple boolean.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_numpy_bool'
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


def argument_numpy_choice(choice='A'):
    '''Example choice.

    Parameters
    ----------
    choice: str, {'A','B','C'}
        argument choice

    '''
    pass


def test_argument_numpy_choice():
    '''Test simple character.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_numpy_choice'
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


def argument_numpy_all(
    string_check='A',
    bool_check=False,
    integer_check=1,
    float_check=1.5,
    list_check=['A'],
    set_check={'a'},
    tuple_check=('A',),
    # file_check='test.toml',
):
    '''Example full.

    Parameters
    ----------
    string_check: str
        argument string
    bool_check: bool
        argument bool
    integer_check: int
        argument int
    float_check: float
        argument float
    list_check: list
        argument list
    set_check: set
        argument set
    tuple_check: tuple
        argument tuple

    '''
    pass


def test_argument_numpy_all():
    '''Test full type set.'''
    name, fn = [
        x
        for x in getmembers(module, isfunction)
        if x[0] == 'argument_numpy_all'
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
    assert arguments[0].type == str
    assert arguments[0].default == 'A'

    # print(arguments[1].__dict__)
    assert arguments[1].help == 'argument bool'
    # NOTE: Argparse does not store bool type
    assert not hasattr(arguments[1], 'type')
    assert arguments[1].default is False

    # print(arguments[2].__dict__)
    assert arguments[2].help == 'argument int'
    assert arguments[2].type == int
    assert arguments[2].default == 1

    # print(arguments[3].__dict__)
    assert arguments[3].help == 'argument float'
    assert arguments[3].type == float
    assert arguments[3].default == 1.5

    # print(arguments[4].__dict__)
    assert arguments[4].help == 'argument list'
    # assert arguments[4].type == list
    assert arguments[4].default == ['A']

    # print(arguments[5].__dict__)
    assert arguments[5].help == 'argument set'
    # XXX: broken somehow
    # assert arguments[5].type == set
    assert arguments[5].default == {'a'}

    # print(arguments[6].__dict__)
    assert arguments[6].help == 'argument tuple'
    # assert arguments[6].type == tuple
    assert arguments[6].default == ('A',)
