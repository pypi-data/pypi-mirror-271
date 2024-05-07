import argparse
import importlib
import os
import sys


def main_with_tools(tools_dir, package_name, *, description=''):
    parser = define_parser(argparse.ArgumentParser(description=description), tools_dir, package_name)
    args = parser.parse_args()
    args.func(args)


def define_parser(parser, tools_dir, package_name):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()
    for module_file in os.listdir(tools_dir):
        module_name = module_file.rsplit(".", 1)[0]
        if not module_file.endswith('.py') or module_file.startswith('__'):
            continue
        try:
            module = importlib.import_module(f'{package_name}.{module_name}')
            if hasattr(module, 'define_parser'):
                description = module.get_description() if hasattr(module, 'get_description') else ''
                subparser = subparsers.add_parser(
                    module_name,
                    help=description,
                    description=description,
                )
                module.define_parser(subparser)
            else:
                sys.stderr.write(f'warning: module "{module_name}" does not define `define_parser` function\n')
        except ModuleNotFoundError as e:
            sys.stderr.write(f'warning: unable to import module "{module_name}": {e}\n')
    return parser
