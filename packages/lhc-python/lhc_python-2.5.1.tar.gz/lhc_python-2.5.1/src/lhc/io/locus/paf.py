from .locus_file import GenomicInterval, LocusFile


class PafFile(LocusFile):

    EXTENSION = ('.paf', '.paf.gz')
    FORMAT = 'paf'

    def parse(self, line: str, index=0) -> GenomicInterval:
        query_name, query_length, query_start, query_end, strand, target_name, target_length, target_start, target_end, matches, block_length, mapping_quality, *parts = line.rstrip('\r\n').split('\t')
        return GenomicInterval(int(target_start) - index, int(target_end),
                               chromosome=target_name,
                               strand=strand,
                               data={'query_name': query_name,
                                     'query_length': int(query_length),
                                     'query_start': int(query_start) - index,
                                     'query_end': int(query_end),
                                     'target_length': int(target_length),
                                     'matches': matches,
                                     'block_length': block_length,
                                     'mapping_quality': mapping_quality,
                                     'gene_id': '{}:{}-{}_{}:{}-{}'.format(query_name, query_start, query_end, target_name, target_start, target_end)})

    def format(self, interval: GenomicInterval, index=0) -> str:
        return '{query_name}\t{query_length}\t{query_start}\t{query_end}\t{strand}\t{target_name}\t{target_length}\t{target_start}\t{target_end}\t{matches}\t{block_length}\t{mapping_quality}'.format(
            query_name=interval.data['query_name'],
            query_length=interval.data['query_length'],
            query_start=interval.data['query_start'] + index,
            query_end=interval.data['query_end'],
            strand=interval.strand,
            target_name=interval.chromosome,
            target_length=interval.data['target_length'],
            target_start=interval.start + index,
            target_end=interval.stop,
            matches=interval.data['matches'],
            block_length=interval.data['block_length'],
            mapping_quality=interval.data['mapping_quality'])
