import argparse
import sys

from functools import partial
from typing import Iterable
from lhc.entities.genomic_coordinate import GenomicPosition, GenomicInterval
from lhc.io.locus.bed import BedFile
from lhc.io.variant import open_variant_file, VariantFile


def filter_(variants: VariantFile, filters=None) -> Iterable[GenomicPosition]:
    for variant in variants:
        if all(filter(variant) for filter in filters):
            yield variant


def filter_variant(variant, filter) -> bool:
    local_variables = {'chrom': variant.chromosome, 'pos': variant.position.position}
    local_variables.update(variant.data)
    return eval(filter, local_variables)


def filter_in_region(variant, region_set) -> bool:
    regions = region_set[variant]
    return regions is not None and len(regions) > 0


def filter_out_region(variant, region_set) -> bool:
    regions = region_set[variant]
    return regions is None or len(regions) == 0


def exclude_variant(variant, variant_set: VariantFile) -> bool:
    variants = variant_set.fetch(GenomicInterval(variant.pos, variant.pos + 1))
    return variants is None or len(variants) == 0


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Filter a set of variants based on the given filters'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the vcf_ file to be filtered (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the filtered vcf_ file (default: stdout).')
    parser.add_argument('-f', '--filter', action='append', default=[],
                        help='filter to apply (default: none).')
    parser.add_argument('-i', '--filter-in', action='append', default=[],
                        help='filter in region (default: none).')
    parser.add_argument('-o', '--filter-out', action='append', default=[],
                        help='filter out region (default: none).')
    parser.add_argument('-x', '--exclude', action='append', default=[],
                        help='exclude matches to variants file (default: none)')
    parser.set_defaults(func=init_filter)
    return parser


def init_filter(args):
    filters = []
    for filter_normal in args.filter_:
        filters.append(partial(filter_variant, filter=filter_normal))
    for filter_in in args.filter_in:
        filters.append(partial(filter_in_region, region_set=BedFile(filter_in)))
    for filter_out in args.filter_out:
        filters.append(partial(filter_out_region, region_set=BedFile(filter_out)))
    for exclude in args.exclude:
        filters.append(partial(exclude_variant, variant_set=open_variant_file(exclude, 'q')))

    with open_variant_file(args.input) as variants, open_variant_file(args.output, 'w') as output:
        if hasattr(variants, 'header') and hasattr(output, 'header'):
            output.set_header(variants.header, variants.samples)
        output.set_header(variants.header, variants.samples)
        for variant in filter_(variants, filters):
            output.write(variant)


if __name__ == '__main__':
    sys.exit(main())
