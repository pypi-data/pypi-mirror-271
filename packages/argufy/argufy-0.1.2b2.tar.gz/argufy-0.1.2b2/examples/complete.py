"""Simple argparse."""

import inspect
import logging
import sys
from typing import Optional

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def switch():  # type: ignore
    """Run empty function to check switch."""
    print('test empty switch')


def positional(test: str) -> None:
    """Run example positional.

    Parameters
    ----------
    test: str
        example test variable

    """
    print(test)


def boolean(bool_check=False):  # type: ignore
    """Run example bool."""
    print(bool_check)


def choice(choice_check='A'):  # type: ignore
    """Run example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    """
    print(choice_check)


def optional(variable: Optional[str]) -> None:
    """Run example optional."""
    if variable:
        print(variable)
    else:
        print('yey! optional is not set')


def arguments(test_arg: str = 'test', *args: str, **kwargs: str) -> None:
    """Run example key arguments.

    Parameters
    ----------
    test_arg: str, optional
        test argument with value
    test1: str, optional
        kwargs test one
    test2: str, optional
        kwargs test two

    """
    print('test_arg', test_arg)
    if args != []:
        print('args', args)

    if kwargs != {}:
        print('kwargs', kwargs)


# frame = inspect.currentframe()
# args, args_paramname, kwargs_paramname, values = (
#     inspect.getargvalues(frame)
# )
# print(args, args_paramname, kwargs_paramname, values)
# for k, v in dict(values).items():
#     print(k, v)
# print(inspect.getfullargspec(arguments))
# for x in inspect.getmembers(arguments):
#     print(x)

sig = inspect.signature(arguments)
# print(sig.parameters['args'])
# print(sig.parameters['kwargs'])

parser = Parser(
    prog='complete',
    version='1.2.3',
    log_level='DEBUG',
    log_handler=sys.stderr,
    # command_scheme='chain',
)
parser.add_commands(module)
parser.dispatch()
