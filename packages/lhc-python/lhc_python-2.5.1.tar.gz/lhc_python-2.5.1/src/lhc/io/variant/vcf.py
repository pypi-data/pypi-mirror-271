from collections import OrderedDict
from typing import Any, Dict
from lhc.entities.variant import Variant
from .variant_file import VariantFile


class VcfFile(VariantFile):

    EXTENSION = ('.vcf', '.vcf.gz')
    FORMAT = 'vcf'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.mode == 'r':
            self.header, self.samples = self.get_header()
        elif self.mode == 'w':
            self.header, self.samples = None, None

    def set_header(self, header, samples):
        self.header = header
        self.samples = samples
        self.write_header()

    def get_header(self):
        header = OrderedDict()
        line = next(self.file)
        while line.startswith('##'):
            key, value = line[2:].strip().split('=', 1)
            if key not in header:
                header[key] = set()
            header[key].add(value)
            line = next(self.file)
        samples = line.rstrip('\r\n').split('\t')[9:]
        return header, samples

    def write_header(self):
        for key, value in self.header.items():
            self.file.write('##{}={}\n'.format(key, value))
        self.file.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO')
        if len(self.samples) > 0:
            self.file.write('FORMAT\t{}'.format('\t'.join(self.samples)))
        self.file.write('\n')

    def parse(self, line: str, index=1) -> Variant:
        parts = line.rstrip('\r\n').split('\t')
        info = dict(i.split('=', 1) if '=' in i else (i, i) for i in parts[7].split(';'))
        format_ = None if len(parts) < 9 else parts[8].split(':')
        return Variant(
            parts[0],
            int(parts[1]) - 1,
            parts[3],
            parts[4].split(',')[0],
            parts[2],
            self.get_float(parts[5]),
            parts[6].split(',')[0],
            info,
            format_,
            self.get_samples(parts[9:], format_))

    def format(self, variant: Variant, index=1) -> str:
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            str(variant.chr),
            variant.pos + index,
            variant.id,
            variant.ref,
            ','.join(variant.alt),
            '.' if variant.qual is None else variant.qual,
            ','.join(variant.filter),
            ':'.join('{}={}'.format(k, v) for k, v in variant.info.items()),
            ':'.join(variant.format),
            '\t'.join(self.format_sample(variant.samples[sample], variant.format)
                      if sample in variant.samples
                      else '.' for sample in variant.samples)
        )

    def get_samples(self, parts, format_) -> Dict[str, Any]:
        samples = {}
        for name, part in zip(self.samples, parts):
            samples[name] = {} if part == '.' else dict(zip(format_, part.split(':')))
        return samples

    @staticmethod
    def format_sample(sample, format_):
        return ':'.join(sample[key] for key in format_)

    @staticmethod
    def get_float(string):
        try:
            return float(string)
        except ValueError:
            pass
        return None
