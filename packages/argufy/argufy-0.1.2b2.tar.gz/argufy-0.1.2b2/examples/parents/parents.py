"""Provide prototype for group design."""

import argparse

# from argufy import Parser

# parent_parser = Parser()
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--parent', type=int)

# foo_parser = Parser(parents=[parent_parser])
foo_parser = argparse.ArgumentParser(parents=[parent_parser])
foo_parser.add_argument('foo')
print(foo_parser.parse_args(['--parent', '2', 'XXX']))

# bar_parser = Parser(parents=[parent_parser])
bar_parser = argparse.ArgumentParser(parents=[parent_parser])
bar_parser.add_argument('--bar')
print(bar_parser.parse_args(['--bar', 'YYY']))

# print(parent_parser.parse_args())
