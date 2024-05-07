import argparse

from lhc.io.sequence import open_sequence_file


def interleave(sequences1, sequences2):
    for sequence1, sequence2 in zip(sequences1, sequences2):
        yield sequence1
        yield sequence2


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Interleave the sequences from two different files into one file.'


def define_parser(parser):
    parser.add_argument('fastq1')
    parser.add_argument('fastq2')
    parser.set_defaults(func=init_interleave)
    return parser


def init_interleave(args):
    with open_sequence_file(args.sequences1) as sequences1, open_sequence_file(args.sequences2) as sequences2, open_sequence_file(args.output) as output:
        for sequence in interleave(sequences1, sequences2):
            output.write(sequence)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

