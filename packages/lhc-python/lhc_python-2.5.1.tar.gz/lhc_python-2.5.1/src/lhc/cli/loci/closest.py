import argparse

from typing import Iterable, Iterator
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def closest(lefts: Iterable[GenomicInterval], rights: Iterable[GenomicInterval]) -> Iterator[GenomicInterval]:
    rights = iter(rights)
    lefts = iter(lefts)

    current_closest = [next(rights, None), next(rights, None)]
    for left in lefts:
        if current_closest[0] is None:
            yield left, None, None
        else:
            while left.chromosome != current_closest[0].chromosome or current_closest[1] is not None and current_closest[0].chromosome == current_closest[1].chromosome and abs(current_closest[0].start - left.start) >= abs(current_closest[1].start - left.start):
                current_closest.pop(0)
                current_closest.append(next(rights, None))
            yield left, current_closest[0], abs(current_closest[0].start - left.start)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Get the closest loci to the given loci.'


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?',
                        help='input loci to filter (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='loci file to extract loci to (default: stdout).')
    parser.add_argument('-m', '--missing',
                        help='file to write missing loci to')
    parser.add_argument('-d', '--direction', default='both', choices=('left', 'right', 'both'),
                        help='which loci to return')
    parser.add_argument('-l', '--loci', required=True,
                        help='loci to find intersections with')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='gtf',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-t', '--tolerance', type=int,
                        help='limit the farthest detected loci to tolerance.')
    parser.add_argument('--loci-format')
    parser.add_argument('--input-index', default=1, type=int)
    parser.add_argument('--output-index', default=1, type=int)
    parser.add_argument('--loci-index', default=1, type=int)
    parser.set_defaults(func=init_closest)
    return parser


def init_closest(args):
    import sys

    with open_locus_file(args.input, format=args.input_format, index=args.input_index) as input,\
            open_locus_file(args.output, 'w', format=args.output_format, index=args.output_index) as output, \
            open_locus_file(args.missing, 'we', format=None if args.missing else args.output_format, index=args.output_index) as missing, \
            open_locus_file(args.loci, index=args.loci_index) as loci:
        for left, right, distance in closest(input, loci):
            if args.direction == 'both':
                right_id = right.data['gene_id'] if right is not None else None
                if args.tolerance and distance > args.tolerance:
                    missing.write(left)
                else:
                    sys.stdout.write('\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(left.chromosome, left.start.position, left.stop.position, right.start.position, right.stop.position, distance))
            else:
                locus = left if args.direction == 'left' else right
                if args.tolerance and distance > args.tolerance:
                    missing.write(locus)
                else:
                    output.write(locus)


if __name__ == '__main__':
    main()
