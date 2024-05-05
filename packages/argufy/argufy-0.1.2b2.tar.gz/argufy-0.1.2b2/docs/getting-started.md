# Getting Started

The document is intended to help quickly get started using Argufy.

## Installation

`pip install argufy`

## Convert Module to CLI

To create a CLI start with a module of functions to convert.

```
def example_bool(bool_check = False):
    print(bool_check)
```

## Creating a parser

Next create a parser to 

```
from argufy import Parser
from . import cli

def main():
    parser = Parser()
    parser.add_commands(cli)
    parser.dispatch()

if __name__ == '__main__':
    main()
```

## Running Commands

`python -m check.py`


## Example help message

```
usage: argufy [-h] {example-bool,example-choice} ...

Argufier is an inspection based CLI parser.

positional arguments:
  {example-bool}
    example-bool

optional arguments:
  -h, --help            show this help message and exit
```

## Example command with output

<!--- TODO: Need to get doctest working --->
```
$ python -m check.py example-bool --bool-check=True
True
```
