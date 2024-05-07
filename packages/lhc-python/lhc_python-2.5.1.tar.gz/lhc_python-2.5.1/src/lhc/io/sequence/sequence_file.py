import sys

from typing import ClassVar, Dict, Iterator, Optional
from lhc.cli.sequences import Sequence
from lhc.io import open_file


class SequenceFile:

    REGISTERED_EXTENSIONS = {}
    REGISTERED_FORMATS = {}  # type: Dict[str, ClassVar['SequenceFile']]

    def __init__(self, filename: Optional[str] = None, mode: str = 'r', encoding: str = 'utf-8', *, fr: float = 0, to: float = 1):
        if fr < 0 or fr > 1 or to < 0 or to > 1:
            raise ValueError('fr and to must be between 0 and 1.')
        elif fr >= to:
            raise ValueError('fr must be less than to.')

        if 'r' in mode or 'w' in mode:
            import os
            self.generator = open_file(filename, mode, encoding)
            self.file = self.generator.__enter__()

            if filename:
                statinfo = os.stat(filename)
                self.pos = self.seek(int(fr * statinfo.st_size))
                self.to = int(to * statinfo.st_size)
            else:
                self.pos = 0
                self.to = sys.maxsize
        elif mode == 'q':
            import pysam
            self.file = pysam.FastaFile(filename)
            self.fr = None
            self.to = None
        else:
            raise ValueError('Unrecognised open mode: {}'.format(mode))
        self.mode = mode
        self.encoding = encoding

    def __del__(self):
        self.generator.__exit__(None, None, None)

    def __iter__(self) -> Iterator[Sequence]:
        if self.mode == 'w':
            raise ValueError('Sequence file opened for writing not reading.')

        return self.iter()

    def write(self, sequence: Sequence):
        if self.mode in 'rq':
            raise ValueError('Sequence file opened for reading or querying, not writing.')
        self.file.write(self.format(sequence))
        self.file.write('\n')

    def iter(self) -> Iterator[Sequence]:
        raise NotImplementedError('This function must be implemented by the subclass.')

    def format(self, sequence: Sequence) -> str:
        raise NotImplementedError('This function must be implemented by the subclass.')

    def fetch(self, chromosome, start=None, end=None):
        if self.mode != 'q':
            raise ValueError('sequences file not opened for querying')
        return self.file.fetch(chromosome, start, end)

    def seek(self, pos: int):
        raise NotImplementedError('This function must be implemented by the subclass')

    @classmethod
    def register_sequence_file(cls, loci_file: ClassVar['SequenceFile']):
        for extension in loci_file.EXTENSION:
            cls.REGISTERED_EXTENSIONS[extension] = loci_file.FORMAT
        cls.REGISTERED_FORMATS[loci_file.FORMAT] = loci_file

    @classmethod
    def open_sequence_file(
        cls,
        filename: Optional[str] = None,
        mode='r',
        *,
        encoding='utf-8',
        format: Optional[str] = None,
        fr: float = 0,
        to: float = 1,
    ) -> 'SequenceFile':
        if filename is None and format is None:
            raise ValueError('When reading from stdin or writing to stdout, the file format must be specified.'
                             ' Valid formats are {}'.format(', '.join(cls.REGISTERED_FORMATS)))
        if not format:
            for extension, format in cls.REGISTERED_EXTENSIONS.items():
                if filename.endswith(extension):
                    break
        if format not in cls.REGISTERED_FORMATS:
            raise ValueError('Unknown loci file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding, fr=fr, to=to)
