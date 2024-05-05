"""Simple argparse."""

import logging
import sys

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def find(*args: str, **kwargs: str) -> None:
    """Run example key arguments.

    Parameters
    ----------
    test_one: str, optional
        kwargs test one
    test_two: str, optional
        kwargs test two

    """
    if args != []:
        print('args', args)

    if kwargs != {}:
        print('kwargs', kwargs)


def ignore(test: str) -> None:
    """Ignore this."""
    print('this should be ignored:', test)


parser = Parser(
    prog='complete',
    version='1.2.3',
    # log_level='debug',
    # log_handler=sys.stderr,
)
parser.add_commands(module)
parser.dispatch()
