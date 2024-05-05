# Welcome to Argufy

Inspection-based command line interface (CLI) written in Python.

## Overview

Argufy is built around Argparse to create CLI's.

First, inspection is used to determine each command and arguments to be created.

Next, docstrings are parsed to fill in any additional settings.

## Motivation

This parser was created because there wasn't a parser that built on what I
believed are some real strenths of Python.

Inspection is a really powerfull tool and I wanted a CLI that would be updated with minimal effort. Argufy
does this by building CLI's from the functions directly. It then parses docstrings to fill in any additional content to create a parser.

In short, the more code-complete your application is the more complete the CLI.

## Design Principles

## Design Choices

## Alternatives

There are multiple alternatives such as Click and Docpopt. These are
great options but each have their own trade-offs.

=== "Argparse"
    Argparse is a great parser with many built-in features. But, it is an
    additional layer of complexity that needs to be managed when
    developing with it. 

=== "Click"
    Click is a great alternative and is widely used. It is also part of
    the Pallets Projects suite of tools. Click is a decorator based CLI
    parser. Decorators are easy and convenient but prevent inspection
    from being used without a performance and capability hit. It also
    requires that your code be wrapped with the decorators. This is
    less usefull when needing the tools to function also as a library.

=== "Docopt"
    Docopt is another great option for CLI parsers and is similar in
    scope to Argufy. It works by parsing docstrings directly in the 
    main module of an applications. A CLI is created by adding the 
    syntax directly into docstrings. Updates to an application still 
    requires that the CLI also be updated independently.
