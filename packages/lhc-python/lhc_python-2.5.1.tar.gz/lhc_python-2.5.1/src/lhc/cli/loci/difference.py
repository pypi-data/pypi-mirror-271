import argparse
import sys

from typing import Iterator
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def difference(as_, bs, target_set='b', stranded=False) -> Iterator[GenomicInterval]:
    previous_hits = set()
    for a in as_:
        hits = bs[a]
        if target_set == 'a':
            yield a
        elif target_set == 'b':
            next_previous_hits = set()
            for hit in hits:
                if hit in previous_hits:
                    next_previous_hits.add(hit)
                else:
                    yield hit
            previous_hits = next_previous_hits
        elif target_set == 'ab':
            yield from (a.intersect(hit) for hit in hits)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Remove parts of the loci that intersect with the given set of loci'


def define_parser(parser):
    parser.add_argument('a', nargs='?',
                        help='name of the intervals file to be sheared (default: stdin).')
    parser.add_argument('b',
                        help='name of the sheared intervals file (default: stdout).')
    parser.add_argument('-t', '--target', default='b', choices=('a', 'b'),
                        help='a: b - a. b: a - b')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='gtf',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('--stranded', action='store_true',
                        help='whether to shear loci on both strands or just the same orientation')
    parser.set_defaults(func=init_shear)
    return parser


def init_shear(args):
    with open_locus_file(args.input, format=args.input_format) as input,\
            open_locus_file(args.output, 'w', format=args.output_format) as output:
        shears = pysam.TabixFile(args.shears)
        for interval in shear(input, shears, args.stranded):
            output.write(interval)


if __name__ == '__main__':
    sys.exit(main())
