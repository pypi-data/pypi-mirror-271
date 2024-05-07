import argparse
import os

from lhc.io.locus import open_locus_file
from lhc.collections import OnePassIntervalSet, TabixFileWrapper


def intersect(as_, bs, target_set='b'):
    previous_hits = set()
    for a in as_:
        hits = bs[a]
        if target_set == 'a':
            yield a
        elif target_set == 'b':
            next_previous_hits = set()
            for hit in hits:
                if hit in previous_hits:
                    next_previous_hits.add(hit)
                else:
                    yield hit
            previous_hits = next_previous_hits
        elif target_set == 'ab':
            yield from (a.intersect(hit) for hit in hits)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'get the intersecting loci between two sets'


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('a', nargs='?',
                        help='input loci to intersect (default: stdin).')
    parser.add_argument('b',
                        help='input loci to intersect.')
    parser.add_argument('-t', '--target', default='b', choices=('a', 'b', 'ab'),
                        help='a - return loci from set a. b - return loci from set b. ab - intersection of the loci')
    parser.add_argument('-i', '--input-format',
                        help='file format of set a loci (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='bed',
                        help='file format of output file (useful for writing to stdout).')
    parser.set_defaults(func=init_intersect)
    return parser


def init_intersect(args):
    with open_locus_file(args.a, format=args.input_format) as as_,\
        open_locus_file(args.b) as bs,\
        open_locus_file(mode='w', format=args.output_format) as output\
    :
        bs = TabixFileWrapper(args.b) if os.path.exists(f'{args.b}.tbi') else OnePassIntervalSet(bs)
        for locus in intersect(as_, bs, args.target):
            output.write(locus)


if __name__ == '__main__':
    main()
