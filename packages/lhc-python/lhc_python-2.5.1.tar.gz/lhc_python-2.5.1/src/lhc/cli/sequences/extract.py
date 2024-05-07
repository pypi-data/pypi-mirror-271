import argparse
import sys

from typing import Generator, Iterable, Set
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.entities.locus import make_loci
from lhc.entities.sequence.reverse_complement import reverse_complement
from lhc.io.locus import open_locus_file
from lhc.io.sequence import open_sequence_file, Sequence, SequenceFile


def extract_by_coordinate(loci: Iterable[GenomicInterval], sequences: SequenceFile, stranded=True, header_template='{gene_id}') -> Generator[str, None, Set[str]]:
    missing_chromosomes = set()
    for locus in loci:
        if str(locus.chromosome) not in sequences.file.references:
            missing_chromosomes.add(str(locus.chromosome))
            continue
        sequence = sequences.fetch(str(locus.chromosome), locus.start.position, locus.stop.position)
        header = header_template.format(chr=locus.chromosome, start=locus.start, stop=locus.stop, **locus.data)
        yield Sequence(header, reverse_complement(sequence) if locus.strand == '-' and stranded else sequence)
    sys.stderr.write('\n'.join(sorted(missing_chromosomes)))
    return missing_chromosomes


def extract_by_name(loci: Iterable[GenomicInterval], sequences: SequenceFile, stranded=True, header_template='{gene_id}') -> Generator[Sequence, None, None]:
    for locus in loci:
        if locus.data['gene_id'] in sequences.file.references:
            sequence = sequences.fetch(locus.data['gene_id'])
            header = header_template.format(chr=locus.chromosome, start=locus.start, stop=locus.stop, **locus.data)
            yield Sequence(header, reverse_complement(sequence) if locus.strand == '-' and stranded else sequence)


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
    return 'Extract subsequences using the given set of loci.'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='loci to extract (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequences file to extract sequences to (default: stdout).')
    parser.add_argument('-a', '--assemble', action='store_true',
                        help='assemble loci models before extracting sequences')
    parser.add_argument('-f', '--format', default='{gene_id}',
                        help='format string to use as the header of the fasta entry.')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='fasta',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-n', '--extract_by_name', default=False, action='store_true',
                        help='extract sequences by entry rather than coordinate.')
    parser.add_argument('-s', '--sequences', required=True,
                        help='sequences file to extract loci from')
    parser.add_argument('-u', '--unstranded', action='store_false',
                        help='whether to keep the strand of the loci (default: true)')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args):
    extract = extract_by_name if args.extract_by_name else extract_by_coordinate
    with open_locus_file(args.input, format=args.input_format) as loci,\
        open_sequence_file(args.output, 'w', format=args.output_format) as output,\
        open_sequence_file(args.sequence, 'q') as sequences\
    :
        if args.assemble:
            loci = make_loci(loci)
        for entry in extract(loci, sequences, args.unstranded, args.format):
            output.write(entry)


if __name__ == '__main__':
    sys.exit(main())
