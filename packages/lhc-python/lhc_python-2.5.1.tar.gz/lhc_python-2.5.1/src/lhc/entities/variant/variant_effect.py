def call_variant_effects(amino_acid_variants):
    variant_effects = []
    for variant in amino_acid_variants:
        # intron_variant is still missing
        if variant is None:
            variant_effects.append('intergenic_variant')
        elif variant.fs == 0:
            if variant.ref == variant.alt:
                if variant.pos == 0:
                    variant_effects.append('start_retained_variant')
                elif variant.ref == '*':
                    variant_effects.append('stop_retained_variant')
                else:
                    variant_effects.append('synonymous_variant')
            else:
                if variant.pos == 0:
                    variant_effects.append('start_lost')
                elif variant.ref == '*':
                    variant_effects.append('stop_lost')
                elif variant.alt == '*':
                    variant_effects.append('stop_gained')
                else:
                    variant_effects.append('missense_variant')
        elif len(variant.ref) > len(variant.alt):
            if variant.ref.endswith(variant.alt):
                variant_effects.append('inframe_deletion')
            else:
                variant_effects.append('frameshift_truncation')
        else:
            if variant.alt.endswith(variant.ref):
                variant_effects.append('inframe_insertion')
            else:
                variant_effects.append('frameshift_elongation')
    return variant_effects
