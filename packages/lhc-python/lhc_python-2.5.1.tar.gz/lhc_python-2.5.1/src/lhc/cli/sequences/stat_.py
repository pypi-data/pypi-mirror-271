import argparse

from lhc.io.sequence import open_sequence_file


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Get descriptive statistics for the given set of sequences.'


def define_parser(parser):
    parser.add_argument('input', nargs='*',
                        help='sequences to stat (default: stdin).')
    parser.set_defaults(func=init_stat)
    return parser


def init_stat(args: argparse.Namespace):
    for input_file in args.input:
        with open_sequence_file(input_file) as sequences:
            for sequence in sequences:
                sys.stdout.write('{}\t{}\n'.format(sequence.identifier, len(sequence.sequence)))


if __name__ == '__main__':
    import sys
    sys.exit(main())
