import sys
import argparse

from typing import Iterable, Iterator
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def deduplicate(interval_file: Iterable[GenomicInterval], *, threshold=0) -> Iterator[GenomicInterval]:
    intervals = iter(interval_file)
    prev = next(intervals, None)
    for interval in intervals:
        if interval.chromosome != prev.chromosome or interval.start - prev.start > threshold:
            yield prev
            prev = interval


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Remove duplicate loci.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be extended (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the extended intervals file (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='gtf',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-t', '--threshold', type=int, default=0,
                        help='loci within the threshold are replaced with the upstream loci')
    parser.set_defaults(func=init_deduplicate)
    return parser


def init_deduplicate(args):
    args.output_format = args.input_format if args.output_format is None else args.output_format
    with open_locus_file(args.input, format=args.input_format) as input,\
            open_locus_file(args.output, 'w', format=args.output_format) as output:
        for interval in deduplicate(input, threshold=args.threshold):
            output.write(interval)


if __name__ == '__main__':
    sys.exit(main())
