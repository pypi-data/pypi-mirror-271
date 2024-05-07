#!/usr/bin/python

import argparse
import os
import sys

from lhc.io.variant import open_variant_file, VariantFile
from lhc.entities.variant.merger import VariantMerger


def merge(iterators, out: VariantFile, bams, *, variant_fields=[]):
    merger = VariantMerger(iterators, bams=bams, variant_fields=variant_fields)
    out.set_header(merger.hdrs, merger.samples)
    for entry in merger:
        out.write(entry)
    out.close()


def format_sample(sample, format):
    return ':'.join(sample[key] for key in format)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Merge sets of variants'


def define_parser(parser):
    add_arg = parser.add_argument
    add_arg('inputs', nargs='+')
    add_arg('-b', '--bams', nargs='+',
            help='Include read counts from bam files')
    add_arg('-o', '--output',
            help='Name of the merged vcf (default: stdout).')
    add_arg('-f', '--variants-fields', nargs='+',
            help='All fields that are variants specific')
    parser.set_defaults(func=init_merge)
    return parser


def init_merge(args):
    non_existent = [filename for filename in args.inputs if not os.path.exists(filename)]
    if len(non_existent) > 0:
        raise FileNotFoundError('The following files were not found:\n{}'.format('\n'.join(non_existent)))

    inputs = [open_variant_file(filename) for filename in args.inputs]
    names = trim_names(args.inputs)
    for name, input in zip(names, inputs):
        if len(input.samples) == 0:
            input.samples.append(name)
    with open_variant_file(args.output, 'w') as output:
        merge(inputs, output, args.bams, variant_fields=args.variant_fields)


def trim_names(inputs):
    inputs = [os.path.basename(input) for input in inputs]
    smallest_name_length = min(len(input) for input in inputs)
    i = 1
    while i < smallest_name_length:
        if len(set(input[-i] for input in inputs)) > 1:
            break
        i += 1
    return [input[:-i + 1] for input in inputs]


if __name__ == '__main__':
    sys.exit(main())
