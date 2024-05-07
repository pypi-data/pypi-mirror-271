import argparse

from lhc.entities.variant import call_coding_variants, call_codon_variants, call_amino_acid_variants, call_variant_effects
from lhc.collections import IntervalSet
from lhc.io import open_file
from lhc.io.locus import open_locus_file, LocusFile
from lhc.io.sequence import open_sequence_file, SequenceFile
from lhc.io.variant import open_variant_file, VariantFile


def annotate(variants: VariantFile, reference: SequenceFile, loci: LocusFile):
    variants = list(variants)
    locus_set = IntervalSet(locus for locus in loci if locus.data['type'] == 'CDS')
    locus_sequences = {locus.data['gene']: reference.file.fetch(
            str(locus.chromosome),
            locus.start.position,
            locus.stop.position + 3
        ) for locus in locus_set}
    coding_variantss = call_coding_variants(variants, locus_set)
    codon_variantss = []
    for coding_variants in coding_variantss:
        codon_variantss.append(call_codon_variants(coding_variants, locus_sequences))
    amino_acid_variantss = []
    for codon_variants in codon_variantss:
        amino_acid_variantss.append(call_amino_acid_variants(codon_variants))
    variant_effectss = []
    for amino_acid_variants in amino_acid_variantss:
        variant_effectss.append(call_variant_effects(amino_acid_variants))
    yield from zip(variants, coding_variantss, codon_variantss, amino_acid_variantss, variant_effectss)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(get_description()))


def get_description() -> str:
    return 'Annotate the given set of genomic variants'


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    parser.add_argument('-i', '--input-format')
    parser.add_argument('-r', '--reference', required=True)
    parser.add_argument('-l', '--loci', required=True)
    parser.set_defaults(func=init_annotate)
    return parser


def init_annotate(args: argparse.Namespace):
    with open_variant_file(args.input, format=args.input_format) as variants,\
            open_file(args.output, 'w') as output_file,\
            open_sequence_file(args.reference, 'q') as reference,\
            open_locus_file(args.loci) as loci:
        output_file.write('sample\tallele_frequency\tgenomic_variant\tgene\tamino_acid_variant\tvariant_effect\n')
        for variant, coding_variants, codon_variants, amino_acid_variants, variant_effects in annotate(variants, reference, loci):
            for coding_variant, codon_variant, amino_acid_variant, variant_effect in zip(coding_variants, codon_variants, amino_acid_variants, variant_effects):
                for sample in variant.samples:
                    if 'AF' not in variant.samples[sample]:
                        continue
                    output_file.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(sample, variant.samples[sample]['AF'], variant, coding_variant.gene, amino_acid_variant, variant_effect))


if __name__ == '__main__':
    import sys
    sys.exit(main())
