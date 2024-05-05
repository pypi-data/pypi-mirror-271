"""Example argument group."""

# import argparse
# import inspect
# import traceback

from argufy import Parser

parser = Parser()
# parser = argparse.ArgumentParser(description='Foo', add_help=False)

group1 = parser.add_argument_group('group1')
# group1.add_argument('test-g1')
group1.add_argument('-1', '--option-one', help='get option one')

group2 = parser.add_argument_group('group2')
# group2.add_argument('test-g2')
group2.add_argument('-2', '--option-two', help='get option two')

print(parser.parse_args())
# parser.dispatch()
