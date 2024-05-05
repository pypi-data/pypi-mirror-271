"""Simple argparse."""

import logging
import sys
from typing import Optional

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def optional_boolean(
    check: str,
    bool_check: Optional[bool] = None,
) -> None:
    """Run example bool."""
    print('check is:', check)

    if bool_check:
        print(f"tis {bool_check}")
    else:
        print('nothing to see here')


parser = Parser(
    prog='complete',
    version='1.2.3',
    log_level='DEBUG',
    log_handler=sys.stderr,
    # command_scheme='chain',
)
parser.add_commands(module)
parser.dispatch()
