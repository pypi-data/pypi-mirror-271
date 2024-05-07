from .alignment import Alignment
from typing import ClassVar, Dict, Iterator, Optional
from lhc.cli.sequences import Sequence
from lhc.io import open_file


class AlignmentFile:

    REGISTERED_EXTENSIONS = {}
    REGISTERED_FORMATS = {}  # type: Dict[str, ClassVar['AlignmentFile']]

    def __init__(self, filename: Optional[str] = None, mode: str = 'r', encoding: str = 'utf-8'):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.generator = open_file(filename, 'w', encoding) if mode == 'w' else None
        self.file = self.generator.__enter__() if mode == 'w' else None

    def __del__(self):
        if self.mode == 'w':
            self.generator.__exit__(None, None, None)

    def __iter__(self) -> Iterator[Sequence]:
        if self.mode == 'w':
            raise ValueError('Alignment file opened for writing not reading.')
        return self.iter()

    def write(self, alignment: Alignment):
        raise NotImplementedError('This function must be implemented by the subclass.')

    def iter(self) -> Iterator[Sequence]:
        raise NotImplementedError('This function must be implemented by the subclass.')

    @classmethod
    def register_alignment_file(cls, loci_file: ClassVar['AlignmentFile']):
        for extension in loci_file.EXTENSION:
            cls.REGISTERED_EXTENSIONS[extension] = loci_file.FORMAT
        cls.REGISTERED_FORMATS[loci_file.FORMAT] = loci_file

    @classmethod
    def open_alignment_file(
            cls,
            filename: Optional[str],
            mode='r',
            *,
            encoding='utf-8',
            format: Optional[str] = None,
    ) -> 'AlignmentFile':
        if filename is None and format is None:
            raise ValueError('When reading from stdin or writing to stdout, the file format must be specified.'
                             ' Valid formats are {}'.format(', '.join(cls.REGISTERED_FORMATS)))
        if not format:
            for extension, format in cls.REGISTERED_EXTENSIONS.items():
                if filename.endswith(extension):
                    break
        if format not in cls.REGISTERED_FORMATS:
            raise ValueError('Unknown loci file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding)
