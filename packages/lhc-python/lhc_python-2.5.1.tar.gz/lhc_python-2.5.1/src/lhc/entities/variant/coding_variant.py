from dataclasses import dataclass
from lhc.entities.interval import Interval
from lhc.collections import IntervalSet
from typing import Optional


@dataclass
class CodingVariant:
    id: str
    pos: int
    ref: str
    alt: str
    gene: Optional[str] = None

    def __str__(self):
        res = []
        pos = self.pos
        ref = self.ref
        alt = self.alt
        if len(ref) > len(alt):
            d = len(ref) - len(alt)
            rng = str(pos + len(ref) - 1,) if d == 1 else '{}_{}'.format(pos + len(ref) - d, pos + len(ref) - 1)
            res.append('{}:c.{}del'.format(self.id, rng))
        elif len(alt) > len(ref):
            d = len(alt) - len(ref)
            rng = str(pos + len(alt) - 1) if d == 1 else '{}_{}'.format(pos + len(alt) - d, pos + len(alt) - 1)
            res.append('{}:c.{}ins{}'.format(self.id, rng, alt))
        else:
            if len(ref) > 1 and ref == alt[::-1]:
                res.append('{}:c.{}_{}inv'.format(self.id, pos + 1, pos + len(ref)))
            else:
                res.append('{}:c.{}{}>{}'.format(self.id, pos + 1, ref, alt))
        return ','.join(res)


def call_coding_variants(nucleotide_variants, loci: IntervalSet):
    coding_variants = []
    for nucleotide_variant in nucleotide_variants:
        matching_loci = list(loci.fetch(Interval(nucleotide_variant.pos, nucleotide_variant.pos + 1)))
        coding_variants.append([
            CodingVariant(
                locus.data['gene'] if 'gene' in locus.data else locus.data['product'],
                locus.get_rel_pos(nucleotide_variant.pos),
                nucleotide_variant.ref,
                nucleotide_variant.alt,
                get_gene_name(locus.data),
            ) for locus in matching_loci])
    return coding_variants


def get_gene_name(data):
    name = data.get('gene', None)
    if not name:
        name = data['product']
    return name
