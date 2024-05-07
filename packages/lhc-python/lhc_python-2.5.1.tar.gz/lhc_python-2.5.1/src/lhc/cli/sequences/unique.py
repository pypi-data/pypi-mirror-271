import argparse

from typing import Iterable, Iterator
from lhc.io.sequence import open_sequence_file, Sequence


def unique(sequences: Iterable[Sequence], key_name: str = 'identifier') -> Iterator[Sequence]:
    visited = set()
    for sequence in sequences:
        key = getattr(sequence, key_name)
        if key not in visited:
            yield Sequence(sequence.identifier, sequence.sequence, data=sequence.data)
            visited.add(key)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Remove duplicate sequnces based on the identifiers.'


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?',
                        help='sequences to view (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequences file to write viewed sequences to (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='fasta',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-k', '--key', choices=('identifier', 'sequences'), default='identifier')
    parser.set_defaults(func=init_view)
    return parser


def init_view(args: argparse.Namespace):
    with open_sequence_file(args.input, format=args.input_format) as input_sequences,\
            open_sequence_file(args.output, 'w', format=args.output_format) as output_sequences:
        for sequence in unique(input_sequences, args.key):
            output_sequences.write(sequence)


if __name__ == '__main__':
    import sys
    sys.exit(main())
