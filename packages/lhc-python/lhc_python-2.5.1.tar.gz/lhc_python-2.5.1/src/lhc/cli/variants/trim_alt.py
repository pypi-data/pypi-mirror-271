import argparse

from lhc.io.variant import open_variant_file, VariantFile


def trim_alt(variants: VariantFile, output: VariantFile):
    output.set_header(variants.header, variants.samples)
    for variant in variants:
        poss, refs, alts = _trim_alt(variant.pos, variant.ref, variant.alt)
        for pos, ref, alt in zip(poss, refs, alts):
            variant.pos = pos
            variant.ref = ref
            variant.alt = alt
            output.write(variant)


def _trim_alt(pos, ref, alt):
    poss = []
    refs = []
    alts = []
    for alt in alt.split(','):
        j = 0
        while j < len(ref) and j < len(alt) and ref[-j - 1] == alt[-j - 1]:
            j += 1
        i = 0
        while i < len(ref) - j - 1 and i < len(alt) - j - 1 and ref[i] == alt[i]:
            i += 1
        poss.append(pos + i)
        refs.append(ref[i:len(ref) - j])
        alts.append(alt[i:len(alt) - j])
    return poss, refs, alts


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Trim overlapping nucleotides in the alternative allele'


def define_parser(parser):
    add_arg = parser.add_argument

    add_arg('input', default=None, nargs='?',
            help='The input file (default: stdin).')
    add_arg('output', default=None, nargs='?',
            help='The output file (default: stdout')

    parser.set_defaults(func=init_trim_alt)
    return parser


def init_trim_alt(args):
    with open_variant_file(args.input) as input_, open_variant_file(args.output, 'w') as output:
        trim_alt(input_, output)


if __name__ == '__main__':
    import sys
    sys.exit(main())
