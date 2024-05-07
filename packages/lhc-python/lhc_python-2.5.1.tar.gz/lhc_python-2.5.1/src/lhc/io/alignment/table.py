import collections

from typing import Iterator
from .alignment_file import Alignment, AlignmentFile


class TableFile(AlignmentFile):

    EXTENSION = ('.tsv', '.tsv.gz')
    FORMAT = 'table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alignments = collections.defaultdict(list)

    def __del__(self):
        for key, values in self.alignments.items():
            value_columns = '\t'.join(values)
            self.file.write(f'{key}\t{value_columns}\n')
        super().__del__()

    def iter(self) -> Iterator[Alignment]:
        raise NotImplementedError()

    def write(self, alignment: Alignment):
        for key, value in alignment.sequences.items():
            self.alignments[key].append(value)
