from itertools import chain, islice
from typing import Iterator
from .sequence_file import Sequence, SequenceFile


class FastqFile(SequenceFile):

    EXTENSION = ('.fastq', '.fq', '.fastq.gz', '.fq.gz')
    FORMAT = 'fastq'

    def iter(self) -> Iterator[Sequence]:
        pos = self.pos
        try:
            while pos < self.to:
                hdr, seq, qual_hdr, qual = islice(self.file, 4)
                pos += len(hdr) + len(seq) + len(qual_hdr) + len(qual)
                yield Sequence(hdr.strip()[1:], seq.strip(), data=qual.strip())
        except ValueError:
            raise StopIteration

    def format(self, sequence: Sequence) -> str:
        return '{}\n{}\n{}\n{}'.format(sequence.identifier, sequence, sequence.identifier, sequence.data)

    def seek(self, pos: int):
        self.file.seek(pos)
        for line in self.file:
            if line[0] == '@':
                self.file = chain([line], self.file)
                break
            pos += len(line)
        return pos
