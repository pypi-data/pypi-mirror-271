import json
import sys

from argparse import  ArgumentParser


def extract_patterns(filename):
    with open(filename) as fileobj:
        for line in fileobj:
            if line.strip().startswith('amplicons = '):
                amplicons = json.loads(line.strip()[12:-1])

    known_sites = [2, 22, 38, 55, 61, 64, 73, 104, 125, 139, 155, 157, 162, 166, 168, 173, 183, 207]

    for name, amplicon in amplicons.items():
        chromosome = amplicon['amplicon'].split(':')[0]
        start = int(amplicon['amplicon'].split(':')[1].split('-')[0])
        strand = amplicon['amplicon'].split(':')[2]
        total = sum(pattern['count'] for pattern in amplicon['patterns'])

        relative_sites = align_sites(known_sites, amplicon['sites'], strand)
        for pattern_index, pattern in enumerate(amplicon['patterns']):
            if pattern['count'] / total < 0.05:
                continue
            for site, methylation in zip(relative_sites, pattern['methylation']):
                print(f'{chromosome}\t{start}\t{strand}\t{pattern_index}\t{site}\t{methylation}')


def align_sites(target_sites, query_sites, strand):
    assert strand in '+-'

    query_sites = [site - query_sites[0] for site in query_sites]
    if strand == '-':
        query_sites = [max(query_sites) - site for site in query_sites]

    match_scores = [(0, 0)]
    for start_site in target_sites:
        relative_sites = [site + start_site for site in query_sites]
        matches = [site in target_sites for site in relative_sites]
        if all(matches):
            return relative_sites
        match_scores.append((sum(matches), start_site))
    match_scores.sort(reverse=True)
    relative_sites = [site + match_scores[0][1] for site in query_sites]
    return relative_sites


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> ArgumentParser:
    return define_parser(ArgumentParser())


def define_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument('input_file')
    parser.set_defaults(func=init_extract_patterns)
    return parser


def init_extract_patterns(args):
    extract_patterns(args.input_file)


if __name__ == '__main__':
    main()
