import argparse
import sys

from typing import List


def cs_to_table(cs) -> List[List[str]]:
    return [[]]


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Convert a CS string (CIGAR string al la minimap) to a table'


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('cs')
    parser.set_defaults(func=init_cs_to_table)
    return parser


def init_cs_to_table(args: argparse.Namespace):
    sys.stdout.write('\n'.join('\t'.join(line) for line in cs_to_table(args.cs)))


if __name__ == '__main__':
    main()
