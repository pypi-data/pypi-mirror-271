import itertools

from typing import Iterator
from .sequence_file import Sequence, SequenceFile


class FastaFile(SequenceFile):

    EXTENSION = ('.fasta', '.fa', '.fasta.gz', '.fa.gz', '.fna', '.fna.gz')
    FORMAT = 'fasta'

    def iter(self) -> Iterator[Sequence]:
        pos = self.pos
        line = next(self.file)
        while line and pos < self.to:
            pos += len(line)
            if line.startswith('#'):
                continue
            elif not line.startswith('>'):
                raise ValueError('Invalid fasta file format.')

            header = line.strip()[1:]
            sequence = []
            for line in self.file:
                if line == '' or line.startswith('>'):
                    identifier = header.split(maxsplit=1)[0]
                    yield Sequence(identifier, ''.join(sequence), data=header)
                    header = line.strip()[1:]
                    del sequence[:]
                else:
                    sequence.append(line.strip())
            if not (line == '' or line.startswith('>')):
                identifier = header.split(maxsplit=1)[0]
                yield Sequence(identifier, ''.join(sequence), data=header)
                del sequence[:]
                line = ''

    def format(self, sequence: Sequence) -> str:
        return '>{}\n{}'.format(sequence.identifier, sequence)

    def seek(self, pos: int):
        self.file.seek(pos)
        for line in self.file:
            if line[0] == '>':
                self.file = itertools.chain([line], self.file)
                break
            pos += len(line)
        return pos
