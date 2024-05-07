![Build Status](https://github.com/childsish/lhc-python/actions/workflows/python-package.yml/badge.svg)

# lhc-python

This is my personal library of python classes and functions, many of them have bioinformatics applications.
The library changes constantly and at a whim.
If you want to use it, approach with caution.

## cli

Tools with a command line interface.
These can be used from the command line after the library has been installed using `python -m lhc.cli.<package_name>`.

### alignments

`python -m lhc.cli.alignments cs_to_table`

`python -m lhc.cli.alignments mismatch_filter`

`python -m lhc.cli.alignments strand`

### loci

`python -m lhc.cli.loci closest`

`python -m lhc.cli.loci deduplicate`

`python -m lhc.cli.loci strand`

`python -m lhc.cli.loci filter`

`python -m lhc.cli.loci flank`

`python -m lhc.cli.loci generate`

`python -m lhc.cli.loci kmer_filter`

`python -m lhc.cli.loci query`

`python -m lhc.cli.loci shear`

`python -m lhc.cli.loci stats`

`python -m lhc.cli.loci view`

### multiple_alignments

`python -m lhc.cli.multiple_alignments align_pairwise`

`python -m lhc.cli.multiple_alignments call_variants`

`python -m lhc.cli.multiple_alignments extract`

`python -m lhc.cli.multiple_alignments get_consensus`

`python -m lhc.cli.multiple_alignments trim_gaps`

### sequences

`python -m lhc.cli.sequences barcode_filter`

`python -m lhc.cli.sequences barcode_split`

`python -m lhc.cli.sequences extract`

`python -m lhc.cli.sequences filter`

`python -m lhc.cli.sequences interleave`

`python -m lhc.cli.sequences rmdup`

`python -m lhc.cli.sequences split`

`python -m lhc.cli.sequences stat`

`python -m lhc.cli.sequences unique`

`python -m lhc.cli.sequences view`

### variants

`python -m lhc.cli.variants annotate`

`python -m lhc.cli.variants compare`

`python -m lhc.cli.variants diff`

`python -m lhc.cli.variants filter`

`python -m lhc.cli.variants merge`

`python -m lhc.cli.variants sample`

`python -m lhc.cli.variants shift`

`python -m lhc.cli.variants split_alt`

`python -m lhc.cli.variants trim_alt`
