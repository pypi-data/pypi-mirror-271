import argparse

from typing import Iterator
from lhc.io.sequence import open_sequence_file, SequenceFile, Sequence


def view(sequences: SequenceFile) -> Iterator[Sequence]:
    for sequence in sequences:
        yield Sequence(sequence.identifier, sequence.sequence.replace('-', ''))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'View the sequences in the given file.'


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?',
                        help='sequences to view (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequences file to write viewed sequences to (default: stdout).')
    parser.add_argument('-i', '--input-format')
    parser.add_argument('-o', '--output-format', default='fasta')
    parser.set_defaults(func=init_view)
    return parser


def init_view(args: argparse.Namespace):
    with open_sequence_file(args.input, format=args.input_format) as sequences,\
        open_sequence_file(args.output, 'w', format=args.output_format) as output\
    :
        for sequence in view(sequences):
            output.write(sequence)


if __name__ == '__main__':
    import sys
    sys.exit(main())
