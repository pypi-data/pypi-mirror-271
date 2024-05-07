import argparse
import sys

from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.variant import open_variant_file


def difference(left_iterator, right_set):
    for left in left_iterator:
        rights = right_set.fetch(GenomicInterval(left.pos, left.pos + len(left.ref), chromosome=left.chr))
        matching = len(rights)
        for right in rights:
            if left.pos == right.pos and left.alt == right.alt:
                matching -= 1
        if len(rights) == 0:
            yield left


def main():
    args = get_parser().parse_args()
    args.func(args)

    
def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Find the set difference for two sets of variants.'


def define_parser(parser):
    parser.add_argument('left', nargs='?',
                        help='left side (default: stdin)')
    parser.add_argument('right',
                        help='right side')
    parser.add_argument('-o', '--output', nargs='?',
                        help='output file (default: stdout)')
    parser.add_argument('-l', '--left-format')
    parser.add_argument('-f', '--output-format', default='vcf')
    parser.set_defaults(func=init_difference)
    return parser


def init_difference(args):
    with open_variant_file(args.left, format=args.left_format) as left,\
        open_variant_file(args.right, mode='q') as right,\
        open_variant_file(args.output, 'w', format=args.output_format) as output\
    :
        if hasattr(left, 'header') and hasattr(output, 'header'):
            output.set_header(left.header, left.samples)
        for line in difference(left, right):
            output.write(line)


if __name__ == '__main__':
    sys.exit(main())
