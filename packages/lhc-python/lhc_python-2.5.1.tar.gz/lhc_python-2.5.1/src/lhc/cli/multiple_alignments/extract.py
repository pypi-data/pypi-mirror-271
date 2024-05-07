import argparse
import sys

from lhc.entities.locus import make_loci
from lhc.io.alignment import open_alignment_file
from lhc.io.locus import open_locus_file


def extract(alignment, loci, filter_=None):
    filter_fn = eval(f'lambda: {filter_}')
    for locus in loci:
        local_variables = {
            'chromosome': locus.chromosome,
            'start': locus.start,
            'stop': locus.stop,
            'strand': locus.strand
        }
        if locus.data:
            local_variables.update(locus.data)
        globals().update(local_variables)
        if not filter_ or filter_fn():
            yield alignment.fetch(str(locus.chromosome), locus.start.position, locus.stop.position)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Extract a portion of a multiple alignments defined by the given loci.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of input alignments file (optional, default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of output alignments file (optional, default: stdout).')
    parser.add_argument('-f', '--filter',
                        help='filter for loci')
    parser.add_argument('-l', '--loci', required=True,
                        help='loci to extract')
    parser.add_argument('-a', '--assemble', action='store_true',
                        help='assembles loci hierarchies into nested loci when set')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (required when reading from stdin)')
    parser.add_argument('-o', '--output-format', default='fasta',
                        help='file format of output file (required when writing to stdout)')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args):
    with open_alignment_file(args.input, format=args.input_format) as alignments,\
            open_alignment_file(args.output, 'w', format=args.output_format) as output,\
            open_locus_file(args.loci) as loci:
        if args.assemble:
            loci = make_loci(loci)
        alignment = next(iter(alignments))
        for sub_alignment in extract(alignment, loci, args.filter):
            output.write(sub_alignment)


if __name__ == '__main__':
    sys.exit(main())
