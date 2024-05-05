# python-argufy

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/kuwv/python-argufy.svg?branch=master)](https://travis-ci.org/kuwv/python-argufy)
[![codecov](https://codecov.io/gh/kuwv/python-argufy/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/python-argufy)

## Overview

Inspection based parser built on argparse. Build complex CLI interfaces by
writing more code-complete applications.

## Motivation

Argufy is designed to be an alternative to decorator based parsers such as
Click. Decorators have limitations that prevent effective use of inspection
without drawbacks. This parser easilly allows a CLI to be created with minimal
effort while enabling inspection.

## Install

`pip install argufy`

## Create a parser

```
from argufy import Parser
from . import cli

def main():
    """Do main function for CLI."""
    parser = Parser()
    parser.add_commands(cli)
    parser.dispatch()

if __name__ == '__main__':
    main()
```

## Create the command line subcommands and arguments.

```
"""Example module named CLI."""

def _ignored():
    """This function is ignored."""
    pass

def example(argument: bool = False):
    """Provide an example command.

    Parameters
    ----------
    argument: bool, optional
        Provide an example argument.

    """
    if argument:
        print('This is a true argument')
    else:
        print('This is a false argument')
```

## Example help message.

```
$ command --help
usage: command [-h] {example} ...

positional arguments:
  {example}
    example             Provide an example command.

optional arguments:
  -h, --help            show this help message and exit
```

## Example command help message.

```
$ command example --help
usage: command [-h] [--argument ARGUMENT]

optional arguments:
  -h, --help           show this help message and exit
  --argument ARGUMENT  Provide an example argument.
```
