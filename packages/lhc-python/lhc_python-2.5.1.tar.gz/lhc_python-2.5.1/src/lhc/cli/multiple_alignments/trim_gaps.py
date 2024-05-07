import argparse

from collections import Counter
from lhc.io.sequence import open_sequence_file, Sequence
from typing import Iterator, List


def trim_gaps(sequences: List[Sequence], gap_threshold: 0.1) -> Iterator[Sequence]:
    positions = list(zip(*sequences))
    fr = 0
    to = 0
    for position in positions:
        count = Counter(position)
        if count['-'] / sum(count.values()) < gap_threshold:
            break
        fr += 1
    for position in reversed(positions):
        count = Counter(position)
        if count['-'] / sum(count.values()) < gap_threshold:
            break
        to -= 1
    yield from (Sequence(sequence.identifier, sequence.sequence[fr:to]) for sequence in sequences)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return "Trim 5' and 3' ends of a multiple alignments if mostly gaps are present."


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    parser.add_argument('-i', '--input-format')
    parser.add_argument('-o', '--output-format', default='fasta')
    parser.add_argument('-g', '--gap-threshold', type=float, default=0.1)
    parser.set_defaults(func=init_trim)
    return parser


def init_trim(args):
    with open_sequence_file(args.input, format=args.input_format) as alignment_file,\
            open_sequence_file(args.output, mode='w', format=args.output_format) as trimmed_alignment_file:
        trimmed_alignment = trim_gaps(list(alignment_file), args.gap_threshold)
        for sequence in trimmed_alignment:
            trimmed_alignment_file.write(sequence)


if __name__ == '__main__':
    import sys
    sys.exit(main())
