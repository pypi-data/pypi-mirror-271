import argparse
import sys

from typing import Iterable
from lhc.entities.variant import Variant
from lhc.io.variant import open_variant_file, VariantFile


def shift(variants: VariantFile, amount=0) -> Iterable[Variant]:
    for variant in variants:
        variant.pos += amount
        yield variant


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Shift the position of a set of variants.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the vcf_ file to be filtered (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the filtered vcf_ file (default: stdout).')
    parser.add_argument('-a', '--amount', type=int, default=0,
                        help='amount to shift position by (default: none).')
    parser.set_defaults(func=init_shift)
    return parser


def init_shift(args):
    with open_variant_file(args.input) as input, open_variant_file(args.output, 'w') as output:
        output.set_headers(input.headers, input.samples)
        for line in shift(input, args.amount):
            output.write(line)


if __name__ == '__main__':
    sys.exit(main())
