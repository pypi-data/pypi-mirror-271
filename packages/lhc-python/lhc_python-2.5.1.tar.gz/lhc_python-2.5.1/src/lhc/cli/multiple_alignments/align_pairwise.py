import argparse
import os
import sys

from lhc.io.sequence import iter_sequences
from lhc.entities.multiple_alignment import Aligner, Mode, DEFAULT_NUCLEOTIDE_SCORING_MATRIX, DEFAULT_NUCLEOTIDE_ALPHABET


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def get_description() -> str:
    return 'Align two sequences'


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('sequence1')
    parser.add_argument('sequence2')
    parser.add_argument('-m', '--mode', choices=['global', 'local', 'semiglobal'], default='global')
    parser.add_argument('--molecule', choices=['DNA', 'AA'], default='DNA')
    parser.set_defaults(func=init_align)
    return parser


def init_align(args):
    if args.molecule == 'AA':
        raise NotImplementedError('Not yet implemented: Scoring matrices and alphabet missing for proteins')

    aligner = Aligner(
        mode=Mode.LOCAL if args.mode == 'local' else Mode.GLOBAL if args.mode == 'global' else Mode.SEMI,
        scoring_matrix=DEFAULT_NUCLEOTIDE_SCORING_MATRIX if args.molecule == 'DNA' else DEFAULT_NUCLEOTIDE_SCORING_MATRIX,
        alphabet=DEFAULT_NUCLEOTIDE_ALPHABET if args.molecule == 'DNA' else DEFAULT_NUCLEOTIDE_ALPHABET
    )

    sequence1 = next(iter_sequences(args.sequence1)).seq if args.sequence1.endswith('.fasta') and os.path.exists(args.sequence1) else\
        args.sequence1
    sequence2 = next(iter_sequences(args.sequence2)).seq if args.sequence1.endswith('.fasta') and os.path.exists(args.sequence2) else\
        args.sequence2

    alignment = aligner.align(sequence1, sequence2)
    sys.stdout.write(str(alignment))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
