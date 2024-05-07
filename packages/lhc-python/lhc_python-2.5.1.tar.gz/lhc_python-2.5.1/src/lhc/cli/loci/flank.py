import sys
import argparse

from copy import copy
from typing import Iterable, Iterator
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def flank(intervals: Iterable[GenomicInterval], *, point_one=0, point_two=0, point_three=0, point_four=0, orientation='same') -> Iterator[GenomicInterval]:
    """
    Create flanking intervals for each interval in `intervals`.
    :param intervals: intervals to flank
    :param five_prime: how much upstream to flank
    :param three_prime: how much downstream to flank
    :return: tuple of five- and three-prime flanks
    """
    for interval in intervals:
        strand = interval.strand if orientation == 'same' else '-' if interval.strand == '+' else '+'
        five_prime_interval = None if point_one == point_two else \
            GenomicInterval(interval.start + point_one, interval.start + point_two, chromosome=interval.chromosome,
                            strand=strand, data=copy(interval.data)) if interval.strand == '+' else \
            GenomicInterval(interval.stop - point_two, interval.stop - point_one, chromosome=interval.chromosome,
                            strand=strand, data=copy(interval.data))
        three_prime_interval = None if point_three == point_four else \
            GenomicInterval(interval.stop + point_three, interval.stop + point_four, chromosome=interval.chromosome,
                            strand=strand, data=copy(interval.data)) if interval.strand == '+' else \
            GenomicInterval(interval.start - point_four, interval.start - point_three, chromosome=interval.chromosome,
                            strand=strand, data=copy(interval.data))
        if five_prime_interval and five_prime_interval.start >= 0:
            five_prime_interval.data['gene_id'] += '_5p_flank'
            five_prime_interval.data['transcript_id'] = five_prime_interval.data['gene_id'] + five_prime_interval.data['transcript_id'][five_prime_interval.data['transcript_id'].find('.'):] if 'transcript_id' in five_prime_interval.data else five_prime_interval.data['gene_id'] + '.1'
            five_prime_interval.data['exon_id'] = five_prime_interval.data['gene_id'] + five_prime_interval.data['exon_id'][five_prime_interval.data['exon_id'].find('.'):] if 'exon_id' in five_prime_interval.data else five_prime_interval.data['gene_id'] + '.1'
            five_prime_interval.data['feature'] = '5p_flank'
        if three_prime_interval and three_prime_interval.start >= 0:
            three_prime_interval.data['gene_id'] += '_3p_flank'
            three_prime_interval.data['transcript_id'] = three_prime_interval.data['gene_id'] + three_prime_interval.data['transcript_id'][three_prime_interval.data['transcript_id'].find('.'):] if 'transcript_id' in three_prime_interval.data else three_prime_interval.data['gene_id'] + '.1'
            three_prime_interval.data['exon_id'] = three_prime_interval.data['gene_id'] + three_prime_interval.data['exon_id'][three_prime_interval.data['exon_id'].find('.'):] if 'exon_id' in three_prime_interval.data else three_prime_interval.data['gene_id'] + '.1'
            three_prime_interval.data['feature'] = '3p_flank'
        yield five_prime_interval, three_prime_interval


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Get the intervals flanking the given loci.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be flanked (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the flanked intervals file (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='gtf',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-1', '--point-one', type=int, default=0,
                        help='start the 5\' flank relative to the start coordinate')
    parser.add_argument('-2', '--point-two', type=int, default=0,
                        help='stop the 5\' flank relative to the start coordinate')
    parser.add_argument('-3', '--point-three', type=int, default=0,
                        help='start the 3\' flank relative to the stop coordinate')
    parser.add_argument('-4', '--point-four', type=int, default=0,
                        help='stop the 3\' flank relative to the stop coordinate')
    parser.add_argument('-x', '--orientation', choices=['same', 'opposite'], default='same')
    parser.set_defaults(func=init_flank)
    return parser


def init_flank(args):
    assert args.point_one <= args.point_two
    assert args.point_three <= args.point_four
    args.output_format = args.input_format if args.output_format is None else args.output_format

    with open_locus_file(args.input, format=args.input_format) as input,\
            open_locus_file(args.output, 'w', format=args.output_format) as output:
        flanks = flank(
            input,
            point_one=args.point_one,
            point_two=args.point_two,
            point_three=args.point_three,
            point_four=args.point_four,
            orientation=args.orientation)
        for five_prime, three_prime in flanks:
            if five_prime is not None:
                output.write(five_prime)
            if three_prime is not None:
                output.write(three_prime)


if __name__ == '__main__':
    sys.exit(main())
