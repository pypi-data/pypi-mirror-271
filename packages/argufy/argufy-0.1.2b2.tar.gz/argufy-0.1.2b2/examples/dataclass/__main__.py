# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide CLI for example."""

import sys
from argufy import Parser

from . import cmd


def main() -> None:
    """Demonstrate main with CLI."""
    parser = Parser(
        # command_type='subcommand',
        use_module_args=True,
        version='0.1.0',
        log_level='debug',
        log_handler=sys.stderr,
    )
    parser.add_commands(cmd)
    parser.dispatch()


if __name__ == '__main__':
    main()
