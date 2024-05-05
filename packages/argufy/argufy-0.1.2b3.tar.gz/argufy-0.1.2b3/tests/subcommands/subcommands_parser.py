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
check_attribute = 'test-attr'


def example_bool(bool_check: bool = False):
    '''Mock example bool.

    Parameters
    ----------
    bool_check: bool, optional
        list packages and version

    '''
    print(bool_check is True)


def example_choice(choice_check: str = 'A'):
    '''Mock example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    '''
    print(choice_check == 'B')
