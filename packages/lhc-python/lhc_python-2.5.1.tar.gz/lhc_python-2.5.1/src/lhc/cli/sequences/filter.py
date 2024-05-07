import argparse

from typing import Callable, Iterator, Set
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file
from lhc.io.sequence import open_sequence_file, Sequence, SequenceFile


def filter_(sequences: SequenceFile, filters: Set[Callable], mode=all) -> Iterator[Sequence]:
    for sequence in sequences:
        if mode(filter_(sequence) for filter_ in filters):
            yield sequence


def filter_in_set(entry, entries):
    return entry.hdr in entries


def format_locus(format_string: str, locus: GenomicInterval) -> str:
    return format_string.format(chromosome=locus.chromosome,
                                start=locus.start.position,
                                end=locus.stop.position,
                                strand=locus.strand,
                                **locus.data)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Filter sequences using the given filter.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='sequences to filter (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequences file to filtered sequences to (default: stdout).')
    parser.add_argument('-l', '--loci',
                        help='filter using given loci')
    parser.add_argument('--loci-format', default='{gene_id}',
                        help='format string to convert loci into fasta header')
    parser.add_argument('-m', '--mode', default='all', choices=['all', 'any'],
                        help='whether entry has to match all or any filter')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args: argparse.Namespace):
    from functools import partial

    filters = set()

    if args.loci:
        with open_locus_file(args.loci) as loci:
            filters.add(partial(filter_in_set, entries={format_locus(args.loci_format, locus) for locus in loci}))

    with open_sequence_file(args.input) as sequences, open_sequence_file(args.output, 'w') as output:
        for sequence in filter_(sequences, filters, mode={'all': all, 'any': any}[args.mode]):
            output.write(sequence)


if __name__ == '__main__':
    import sys
    sys.exit(main())
