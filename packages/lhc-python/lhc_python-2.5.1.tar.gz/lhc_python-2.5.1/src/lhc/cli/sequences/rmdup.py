import argparse
import numpy

from lhc.io.sequence import open_sequence_file, SequenceFile


def rmdup(input_: SequenceFile):
    from collections import defaultdict

    visited = defaultdict(list)
    for sequence in input_:
        visited[sequence.identifier].append(sequence)
    for sequences in visited:
        sequences = sorted(sequences, key=lambda sequence_: numpy.mean(convert_qualities(sequence_.data['quality'])))
        yield sequences[-1]


def convert_qualities(qua, offset=33):
    return [ord(char) - offset for char in qua]


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Remove duplicates from the given set of sequences'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                              help='input file (default: stdin)')
    parser.add_argument('output', nargs='?',
                              help='output file (default: stdout)')
    parser.set_defaults(func=init_rmdup)
    return parser


def init_rmdup(args):
    with open_sequence_file(args.input) as input_, open_sequence_file(args.output) as output:
        for sequence in rmdup(input_):
            output.write(sequence)


if __name__ == '__main__':
    import sys
    sys.exit(main())
