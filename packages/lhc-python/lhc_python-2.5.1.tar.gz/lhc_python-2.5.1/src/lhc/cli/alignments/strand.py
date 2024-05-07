import pysam

from collections import Counter
from argparse import ArgumentParser
from lhc.io.locus import open_locus_file


def strand(alignments: pysam.AlignmentFile):
    counter = Counter()
    i = 0
    try:
        for alignment in alignments:
            if i > 500000:
                break
            if alignment.is_read2:
                continue
            key = 'FR'[alignment.is_reverse]
            if alignment.is_paired:
                key += 'FR'[alignment.mate_is_reverse]
            counter[key] += 1
            i += 1
    except KeyboardInterrupt:
        pass
    return counter


def strand_loci(loci, alignments: pysam.AlignmentFile):
    counter = Counter()
    i = 0
    try:
        for locus in loci:
            if locus.data['feature'] != 'exon':
                continue
            for alignment in alignments.fetch(str(locus.chromosome), locus.start.position, locus.stop.position):
                if i > 500000:
                    return counter
                if alignment.is_read2:
                    continue
                key = 'FR'[(locus.strand == '-') != alignment.is_reverse]
                if alignment.is_paired:
                    key += 'FR'[(locus.strand == '-') != alignment.mate_is_reverse]
                counter[key] += 1
                i += 1
    except KeyboardInterrupt:
        pass
    return counter


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Calculate strand statistics from aligned reads.'


def define_parser(parser):
    parser.add_argument('input')
    parser.add_argument('-l', '--loci')
    parser.set_defaults(func=init_strand)
    return parser


def init_strand(args):
    alignments = pysam.AlignmentFile(args.input)
    if args.loci:
        with open_locus_file(args.loci) as loci:
            print(strand_loci(loci, alignments))
    else:
        print(strand(alignments))


if __name__ == '__main__':
    main()
