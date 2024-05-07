import argparse

from typing import Iterator
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.sequence import open_sequence_file
from lhc.io.locus import open_locus_file


def generate_from_fasta(sequences) -> Iterator[GenomicInterval]:
    pass


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Generate loci matching the given sequences'


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?',
                        help='sequences file (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='loci file to extract loci to (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='gtf',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-t', '--type', default='exon',
                        help='type of loci for file formats that support having a loci type.')
    parser.set_defaults(func=init_generate)
    return parser


def init_generate(args):
    with open_sequence_file(args.input) as sequences,\
        open_locus_file(args.output, 'w', format=args.output_format) as output\
    :
        for sequence in sequences:
            output.write(GenomicInterval(0, len(sequence), chromosome=sequence.identifier, data={'gene_id': sequence.identifier, 'feature': args.type}))


if __name__ == '__main__':
    main()
