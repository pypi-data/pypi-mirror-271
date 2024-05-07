from contextlib import contextmanager
from typing import Optional
from .sequence_file import Sequence, SequenceFile
from .embl import EmblFile
from .fasta import FastaFile
from .fastq import FastqFile


def iter_sequences(filename, *, encoding='utf-8', format: Optional[str] = None):
    with open_sequence_file(filename, encoding=encoding, format=format) as sequences:
        yield from sequences


@contextmanager
def open_sequence_file(filename: Optional[str] = None, mode='r', *, encoding='utf-8', format: Optional[str] = None, fr: float = 0, to: float = 1):
    file = SequenceFile.open_sequence_file(filename, mode, encoding=encoding, format=format, fr=fr, to=to)
    yield file


SequenceFile.register_sequence_file(EmblFile)
SequenceFile.register_sequence_file(FastaFile)
SequenceFile.register_sequence_file(FastqFile)
