from .locus_file import GenomicInterval, LocusFile


class BedFile(LocusFile):

    EXTENSION = ('.bed', '.bed.gz')
    FORMAT = 'bed'

    def parse(self, line: str, index=1) -> GenomicInterval:
        parts = line.rstrip('\r\n').split('\t')
        name = parts[3] if len(parts) > 3 else ''
        score = parts[4] if len(parts) > 4 else ''
        strand = parts[5] if len(parts) > 5 else '+'
        data = {'gene_id': name, 'score': score}
        for col in parts[6:]:
            data[col] = None
        return GenomicInterval(int(parts[1]) - index, int(parts[2]),
                               chromosome=parts[0],
                               strand=strand,
                               data=data)

    def format(self, interval: GenomicInterval, index=1) -> str:
        return '{chr}\t{start}\t{stop}\t{data[gene_id]}\t{score}\t{strand}{cols}'.format(
            chr=interval.chromosome,
            start=interval.start.position + index,
            stop=interval.stop.position,
            score=interval.data.get('score', '.'),
            data=interval.data,
            strand=interval.strand,
            cols='\t' + '\t'.join(interval.data['cols']) if 'cols' in interval.data else '')
