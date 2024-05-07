from typing import ClassVar, Dict, Iterator, Optional
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io import open_file


class LocusFile:

    REGISTERED_EXTENSIONS = {}
    REGISTERED_FORMATS = {}  # type: Dict[str, ClassVar['LocusFile']]

    def __init__(self, filename: Optional[str] = None, mode: str = 'r', encoding: str = 'utf-8', index=1):
        self.generator = None
        if 'r' in mode or 'w' in mode:
            self.generator = open_file(filename, mode, encoding)
            self.file = self.generator.__enter__()
        elif mode == 'q':
            import pysam
            self.file = pysam.TabixFile(filename)
        else:
            raise ValueError('Unrecognised open mode: {}'.format(mode))
        self.mode = mode
        self.encoding = encoding
        self.index = index

    def __iter__(self) -> Iterator[GenomicInterval]:
        if self.mode == 'w':
            raise ValueError('Locus file opened for writing, not reading.')
        for raw_entry in self.iter():
            yield self.parse(raw_entry, self.index)

    def iter(self) -> Iterator[str]:
        for line in self.file:
            if line and not line.startswith('#'):
                yield line

    def fetch(self, locus: GenomicInterval) -> Iterator[GenomicInterval]:
        if self.mode in 'rw':
            raise ValueError('Loci file opened for reading or writing, not querying.')
        return (self.parse(raw_entry, self.index) for raw_entry in
                self.file.fetch(str(locus.chromosome), locus.start.position, locus.stop.position))

    def write(self, locus: GenomicInterval):
        if self.mode in 'rq':
            raise ValueError('Locus file opened for reading or querying, not writing.')
        self.file.write(self.format(locus, self.index))
        self.file.write('\n')

    def close(self):
        if self.mode in 'rw':
            self.file.close()

    def parse(self, raw_entry: str, index=1) -> GenomicInterval:
        raise NotImplementedError('This function must be implemented by the subclass.')

    def format(self, locus: GenomicInterval) -> str:
        raise NotImplementedError('This function must be implemented by the subclass.')

    @classmethod
    def register_locus_file(cls, loci_file: ClassVar['LocusFile']):
        for extension in loci_file.EXTENSION:
            cls.REGISTERED_EXTENSIONS[extension] = loci_file.FORMAT
        cls.REGISTERED_FORMATS[loci_file.FORMAT] = loci_file

    @classmethod
    def open_locus_file(
        cls,
        filename: Optional[str] = None,
        mode='r', *,
        encoding='utf-8',
        format: Optional[str] = None,
        index=1
    ) -> 'LocusFile':
        if filename is None and format is None:
            raise ValueError('When reading from stdin or writing to stdout, the file format must be specified.'
                             ' Valid formats are {}'.format(', '.join(cls.REGISTERED_FORMATS)))
        if not format:
            for extension, format in cls.REGISTERED_EXTENSIONS.items():
                if filename.endswith(extension):
                    break
        if format not in cls.REGISTERED_FORMATS:
            raise ValueError('Unknown loci file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding, index)
