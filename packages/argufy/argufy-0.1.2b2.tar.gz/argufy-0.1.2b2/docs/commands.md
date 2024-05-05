# Commands

## Overview

The commands module takes a module as an argument and inspects it for
functions. The results are then used to populate CLI commands. It is
different from the subcommands module in that the module name isn't used as a
command itself.

This command is usefull either for all-in-modules or a module that is holding
functions that combine an applications parts into a CLI.

## Convert Module to CLI

To create a CLI start with a module of functions to convert.

```
def example_bool(bool_check = False):
    print(bool_check)


def example_choice(choice_check = 'A'):
    print(choice_check)
```

## Creating a parser

Next create a parser to

```
from argufy import Parser
from . import cli

def main():
    '''Do main function for a cli module.'''
    parser = Parser()
    parser.add_commands(cli)
    parser.dispatch()

if __name__ == '__main__':
    main()
```

## Pack loading order

Using `__main__` vs `__init__` for CLI instances.
