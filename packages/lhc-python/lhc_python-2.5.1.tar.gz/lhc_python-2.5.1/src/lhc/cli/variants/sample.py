import argparse
import random
import sys

from lhc.io.variant import open_variant_file


def sample(input, proportion):
    for variant in input:
        if random.random() < proportion:
            yield variant


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Subsample a set of variants'


def define_parser(parser):
    add_arg = parser.add_argument
    add_arg('input', nargs='?')
    add_arg('output', nargs='?')
    add_arg('-p', '--proportion', default=0.01, type=float)
    add_arg('-s', '--seed', type=int)
    parser.set_defaults(func=sample_init)
    return parser


def sample_init(args):
    with open_variant_file(args.input) as input_, open_variant_file(args.output, 'w') as output:
        output.set_header(input_.header, input_.samples)
        if args.seed is not None:
            random.seed(args.seed)
        for variant in sample(input_, args.proportion):
            output.write(variant)


if __name__ == '__main__':
    sys.exit(main())
