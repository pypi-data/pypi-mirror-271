import argparse

from lhc.io.methpat.tools import extract_patterns


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # Compare parser
    extract_patterns_parser = subparsers.add_parser('extract_patterns')
    extract_patterns_parser.define_parser(extract_patterns_parser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
