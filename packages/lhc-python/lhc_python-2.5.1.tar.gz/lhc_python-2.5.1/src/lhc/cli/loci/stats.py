import argparse
import itertools

from typing import Iterable
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def get_loci_sizes(loci: Iterable[GenomicInterval]):
    for locus in loci:
        yield locus.stop - locus.start


def get_insert_sizes(loci: Iterable[GenomicInterval]):
    ends = {}
    for locus in loci:
        gene_id = locus.data['transcript_id']
        if gene_id in ends:
            yield gene_id, locus.start - ends[gene_id]
        ends[gene_id] = locus.stop


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Get the minimum and maximum loci sizes in the given set of loci.'


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.set_defaults(func=init_stat)
    return parser


def init_stat(args: argparse.Namespace):
    #with open_loci_file(args.input) as loci:
    #    mn = 0
    #    mx = 0
    #    for k, v in get_insert_sizes(loci):
    #        if v < mn:
    #            mn = v
    #        elif v > mx:
    #            mx = v
    #    print('{}\t{}'.format(mn, mx))

    with open_locus_file(args.input) as loci:
        for_min, for_max = itertools.tee(get_loci_sizes(loci))
        print(min(for_min), max(for_max))


if __name__ == '__main__':
    main()
