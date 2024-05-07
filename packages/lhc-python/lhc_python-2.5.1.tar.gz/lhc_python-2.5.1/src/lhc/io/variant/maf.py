from lhc.entities.variant import Variant
from lhc.io.variant import VariantFile


class MafFile(VariantFile):

    EXTENSION = ('.maf',)
    FORMAT = 'maf'

    COLUMNS = ('hugo_symbol', 'entrez_gene_id', 'center', 'ncbi_build', 'chromosome', 'start_position',
               'end_position', 'strand', 'variant_classification', 'variant_type', 'reference_allele',
               'tumour_seq_allele1', 'tumour_seq_allele2', 'dnsnp_rs', 'dbsnp_val_status',
               'tumour_sample_barcode', 'matched_norm_sample_barcode', 'match_norm_seq_allele1',
               'match_norm_seq_allele2', 'tumour_validation_allele1', 'tumour_validation_allele2',
               'match_norm_validation_allele1', 'match_norm_validation_allele2',
               'verification_status', 'validation_status', 'mutation_status', 'sequencing_phase',
               'sequence_source', 'validation_method', 'score', 'bam_file', 'sequencer',
               'tumour_sample_uuid', 'matched_norm_sample_uuid', 'cosmic_codon', 'cosmic_gene',
               'transcript_id', 'exon', 'chrom_change', 'aa_change', 'genome_plus_minus_10_bp',
               'drug_target', 'ttot_cov', 'tvar_cov', 'ntot_cov', 'nvar_cov', 'dbSNPPopFreq')

    FORMAT_STRING = '\t'.join('{{{}}}'.format(column) for column in COLUMNS)

    def parse(self, line: str, index=1) -> Variant:
        parts = line.rstrip('\r\n').split('\t')
        return Variant(parts[4], int(parts[5]), parts[10], parts[11], info=dict(zip(self.COLUMNS, parts)))

    def format(self, variant: Variant, index=1):
        return ''.format(**variant.info)
