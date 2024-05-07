import collections

from typing import Iterator
from .alignment_file import Alignment, AlignmentFile
from lhc.io.sequence import iter_sequences


class FastaFile(AlignmentFile):

    EXTENSION = ('.fasta', '.fa', '.fasta.gz', '.fa.gz')
    FORMAT = 'fasta'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alignments = collections.defaultdict(list)

    def __del__(self):
        for key, values in self.alignments.items():
            self.file.write(f'>{key}\n{"".join(values)}\n')
        super().__del__()

    def iter(self) -> Iterator[Alignment]:
        yield Alignment({sequence.identifier: sequence.sequence for sequence in iter_sequences(self.filename, encoding=self.encoding)})

    def write(self, alignment: Alignment):
        for key, value in alignment.sequences.items():
            self.alignments[key].append(value)
