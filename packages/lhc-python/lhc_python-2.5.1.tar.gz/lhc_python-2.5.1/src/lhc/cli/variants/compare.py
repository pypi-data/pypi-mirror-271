import argparse

from lhc.cli.variants.filter import filter_variant
from lhc.io.variant import open_variant_file, VariantFile


def compare(a: VariantFile, b: VariantFile, filter_=''):
    set_a = set((line.chr, line.pos, line.ref, line.alt) for line in a if filter_variant(a, filter_))
    set_b = set((line.chr, line.pos, line.ref, line.alt) for line in b if filter_variant(b, filter_))
    sys.stdout.write('{}\t{}\t{}'.format(len(set_a - set_b), len(set_b - set_a), len(set_a & set_b)))


def main():
    args = get_parser().parse_args()
    args.func(args)

    
def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Get the size of the intersection and the unique variants given two sets of variants'


def define_parser(parser):
    add_arg = parser.add_argument
    add_arg('a')
    add_arg('b')
    add_arg('-f', '--filter',
            help='filter for variants (default: none).')
    parser.set_defaults(func=init_compare)
    return parser


def init_compare(args):
    with open_variant_file(args.a, encoding='utf-8') as a, \
            open_variant_file(args.b, encoding='utf-8') as b:
        compare(a, b, args.filter_)


if __name__ == '__main__':
    import sys
    sys.exit(main())
