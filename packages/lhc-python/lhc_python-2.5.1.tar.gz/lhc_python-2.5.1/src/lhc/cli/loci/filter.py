import sys
import argparse

from typing import Iterable, Iterator, Optional
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def filter(intervals: Iterable[GenomicInterval], filter_: Optional[str] = None) -> Iterator[GenomicInterval]:
    filter_fn = eval('lambda: {}'.format(filter_))
    for interval in intervals:
        local_variables = {
            'chromosome': interval.chromosome,
            'start': interval.start,
            'stop': interval.stop,
            'strand': interval.strand
        }
        if interval.data:
            local_variables.update(interval.data)
        globals().update(local_variables)
        if filter_fn():
            yield interval


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Filter loci using the given conditions.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be filtered (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the filtered intervals file (default: stdout).')
    parser.add_argument('-f', '--filter', required=True,
                        help='filter to apply (default: none).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='gtf',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-v', '--inverse', action='store_true',
                        help='invert filter.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--region',
                       help='apply filter in region (default: none).')
    group.add_argument('-x', '--exclude',
                       help='do not apply filter in region (default: none).')
    parser.set_defaults(func=init_filter)
    return parser


def init_filter(args):
    with open_locus_file(args.input, format=args.input_format) as input,\
            open_locus_file(args.output, 'w', format=args.output_format) as output:
        for interval in filter(input, args.filter_):
            output.write(interval)


if __name__ == '__main__':
    sys.exit(main())
