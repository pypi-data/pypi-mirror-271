from typing import Iterator
from .sequence_file import Sequence, SequenceFile


class EmblFile(SequenceFile):

    EXTENSION = ('.embl', '.embl.gz')
    FORMAT = 'embl'

    def iter(self) -> Iterator[Sequence]:
        line = next(self.file)
        while line.startswith(';'):
            line = next(self.file)
        yield Sequence(line.strip(), ''.join(line.strip() for line in self.file))

    def format(self, sequence: Sequence) -> str:
        raise NotImplementedError()
