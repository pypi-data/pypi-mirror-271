import argparse
import re

from functools import partial
from textwrap import TextWrapper
from typing import Callable, Dict, Iterator, List, Optional, Tuple
from lhc.io.sequence import open_sequence_file, Sequence, SequenceFile
from lhc.io import FilePool


def split(sequences: SequenceFile, mappers: List[Callable], *, unmapped='discard') -> Iterator[Tuple[str, Sequence]]:
    def map_to_filename(sequence_: Sequence) -> str:
        for mapper in mappers:
            filename_ = mapper(sequence_)
            if filename_:
                return filename_
        return None if unmapped == 'discard' else\
            'unmapped' if unmapped == 'join' else\
            sequence.identifier

    for sequence in sequences:
        if len(sequence.sequence) == 0:
            continue
        filename = map_to_filename(sequence)
        if filename:
            yield filename, sequence


def map_by_map(sequence: Sequence, map_: Dict[str, str]) -> Optional[str]:
    return map_.get(sequence.identifier, None)


def map_by_regx(sequence: Sequence, regx: re.Pattern, replacement: str, description=False) -> Optional[str]:
    match = regx.match(sequence.identifier)
    if match:
        return regx.sub(replacement, sequence.identifier)
    elif description:
        match = regx.match(sequence.identifier)
        if match:
            return regx.sub(replacement, sequence.identifier)
    return None


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Split a set of sequences into several sets based on the given conditions.'


def define_parser(parser):
    parser.add_argument('input', nargs='*',
                        help='sequences to filter (default: stdin).')
    parser.add_argument('-d', '--description', action='store_true',
                        help='search also in description field.')
    parser.add_argument('-o', '--output',
                        help='prefix for output files')
    parser.add_argument('-r', '--regular-expression', nargs=2, action='append',
                        help='split using regular expression')
    parser.add_argument('-m', '--map',
                        help='split using a map')
    parser.add_argument('-u', '--unmapped', choices=['discard', 'keep', 'split'], default='split',
                        help='whether the unmapped sequences should be discarded, output to a single file or output to multiple files')
    parser.set_defaults(func=init_split)
    return parser


def init_split(args: argparse.Namespace):
    wrapper = TextWrapper()
    mappers = []

    outputs = FilePool(mode='w')
    if args.map:
        with open(args.map) as fileobj:
            mappers.append(partial(map_by_map, map_=dict(line.strip().split(maxsplit=1) for line in fileobj)))
    if args.regular_expression:
        for expression in args.regular_expression:
            mappers.append(partial(map_by_regx, regx=re.compile(expression[0]), replacement=expression[1], description=args.description))

    sequence_iterators = [open_sequence_file(input) for input in args.input if input]
    for input_, sequences in sequence_iterators:
        try:
            for filename, sequence in split(sequences, mappers, unmapped=args.unmapped):
                outputs['{}{}.fasta'.format(args.output, filename)].write('>{} "{}"\n{}\n'.format(sequence.identifier, input_, '\n'.join(wrapper.wrap(sequence.sequence.replace('-', '')))))
        except ValueError as error:
            if str(error) == 'Invalid fasta file format.':
                raise ValueError('"{}" has an invalid fasta file format.'.format(input_))
            else:
                raise error


if __name__ == '__main__':
    import sys
    sys.exit(main())
