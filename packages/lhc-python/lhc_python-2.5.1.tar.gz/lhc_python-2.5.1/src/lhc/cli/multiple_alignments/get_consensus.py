import argparse

from collections import Counter
from lhc.io.sequence import open_sequence_file, Sequence
from typing import Iterator


def get_consensus(sequences: Iterator[Sequence]) -> Sequence:
    consensus = []
    positions = zip(*sequences)
    for position in positions:
        identity = sorted(Counter(position).items(), key=lambda item: item[1])[-1][0]
        if identity != '-':
            consensus.append(identity)
    return Sequence('consensus', ''.join(consensus))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Get consensus sequences from multiple alignments.'


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    parser.add_argument('-i', '--input-format')
    parser.add_argument('-o', '--output-format', default='fasta')
    parser.set_defaults(func=init_get_consensus)
    return parser


def init_get_consensus(args):
    with open_sequence_file(args.input, format=args.input_format) as alignment_file,\
        open_sequence_file(args.output, mode='w', format=args.output_format) as consensus_file:
        consensus = get_consensus(alignment_file)
        consensus_file.write(consensus)


if __name__ == '__main__':
    import sys
    sys.exit(main())
