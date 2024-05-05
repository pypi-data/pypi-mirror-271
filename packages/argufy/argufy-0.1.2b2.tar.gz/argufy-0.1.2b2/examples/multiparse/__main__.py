# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide CLI for example."""

import sys
from argufy import Parser

from . import cmd1, cmd2


def main() -> None:
    """Demonstrate main with CLI."""
    parser = Parser(
        # command_type='subcommand',
        version='0.1.0',
        use_module_args=True,
        main_args_builder={
            'module': 'examples.multiparse.cmd2',
            'function': 'builder',
            'instance': '_settings',
            'variables': {
                'var1': 'yey'
            }
        },
        log_level='debug',
        log_handler=sys.stderr,
    )
    parser.add_commands(cmd1)
    parser.add_commands(cmd2)
    parser.dispatch()


if __name__ == '__main__':
    main()
