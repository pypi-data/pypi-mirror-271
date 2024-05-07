from dataclasses import dataclass


@dataclass
class CodonVariant:
    pos: int
    ref: str
    alt: str
    fs: int = 0

    def __str__(self):
        if self.fs == 0:
            return 'c.{}{}>{}'.format(self.pos + 1, self.ref, self.alt)
        else:
            return 'c.{}{}{}fs{}'.format(self.ref[:3], self.pos + 1, self.alt[:3], 'Ter' + str(self.fs) if self.alt[-3:].upper() in {'TAA', 'TAG', 'TGA'} else '*?')


def call_codon_variants(coding_variants, reference_sequences):
    codon_variants = []
    for variant in coding_variants:
        if variant is None:
            codon_variants.append(None)
            continue

        reference_sequence = reference_sequences[variant.id]
        assert reference_sequence[variant.pos:variant.pos + len(variant.ref)] == variant.ref

        sequence = list(reference_sequence)
        sequence[variant.pos:variant.pos + len(variant.ref)] = list(variant.alt)

        fr = variant.pos - variant.pos % 3
        if (len(variant.ref) - len(variant.alt)) % 3 == 0:
            ref_to = variant.pos + len(variant.ref)
            ref_to += [0, 2, 1][ref_to % 3]
            alt_to = variant.pos + len(variant.alt)
            alt_to += [0, 2, 1][alt_to % 3]
            fs_pos = 0
        else:
            while fr + 3 < len(reference_sequence) and fr + 3 < len(sequence) and reference_sequence[fr:fr+3] == ''.join(sequence[fr:fr+3]):
                fr += 3

            ref_to = fr + 3
            while ref_to <= len(reference_sequence) and reference_sequence[ref_to - 3:ref_to].upper() not in {'TAA', 'TAG', 'TGA'}:
                ref_to += 3

            alt_to = fr + 3
            while alt_to <= len(sequence) and ''.join(sequence[alt_to - 3:alt_to]).upper() not in {'TAA', 'TAG', 'TGA'}:
                alt_to += 3
            fs_pos = alt_to - fr - (3 if ''.join(sequence[alt_to - 3:alt_to]).upper() in {'TAA', 'TAG', 'TGA'} else 0)
            if fs_pos == 0:
                ref_to = fr + 3
        ref_codon = reference_sequence[fr:ref_to]
        alt_codon = ''.join(sequence[fr:alt_to])
        codon_variants.append(CodonVariant(fr, ref_codon, alt_codon, fs_pos))
    return codon_variants
