import argparse
import sys

from lhc.io.variant import open_variant_file, VariantFile
from lhc.entities.variant import Variant


def split_alt(variants: VariantFile):
    # TODO: figure out what to do with GT
    for variant in variants:
        for split_variant in _split_variant(variant):
            yield split_variant


def _split_variant(variant):
    res = []
    alts = variant.alt
    infos = _split_dict(variant.info, len(alts))
    sampless = _split_samples(variant.samples, len(alts))
    tmp = list(variant)
    for alt, info, samples in zip(alts, infos, sampless):
        tmp[3] = alt
        tmp[6] = info
        if len(tmp) > 8:
            tmp[8] = samples
        res.append(Variant(*tmp))
    return res


def _split_samples(samples, n):
    if len(samples) == 0:
        return n * [{}]
    split = []
    for sample in samples.values():
        split.append(_split_dict(sample, n))
    res = []
    for sample_data in zip(*split):
        res.append(dict(list(zip(samples, sample_data))))
    return res


def _split_dict(info, n):
    res = [info.copy() for i in range(n)]
    for key, value in info.items():
        if ',' not in value:
            continue
        for r, v in zip(res, value.split(',')):
            r[key] = v
    return res


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Split variants into multiple variants for each alternate allele.'


def define_parser(parser):
    add_arg = parser.add_argument

    add_arg('input', default=None, nargs='?',
            help='The input file (default: stdin).')
    add_arg('output', default=None, nargs='?',
            help='The output file (default: stdout')

    parser.set_defaults(func=init_split_alt)
    return parser


def init_split_alt(args):
    with open_variant_file(args.input) as input_, open_variant_file(args.output, 'w') as output:
        for variant in split_alt(input_):
            output.write(variant)


if __name__ == '__main__':
    sys.exit(main())
