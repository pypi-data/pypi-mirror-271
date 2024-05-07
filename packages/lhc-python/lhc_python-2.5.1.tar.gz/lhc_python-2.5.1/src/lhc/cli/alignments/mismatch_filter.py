import argparse
import sys

from lhc.misc.tokeniser import Tokeniser
from collections import namedtuple


SamEntry = namedtuple('SamEntry', ('query_name', 'flag', 'rname', 'pos', 'mapq', 'cigar', 'rnext', 'pnext', 'tlen', 'seq', 'qual', 'tags', 'original'))
Variant = namedtuple('Variant', ('type', 'value'))


def mismatch_filter(alignments, *, percent=0.01, count=100):
    for alignment in alignments:
        if 'cs' in alignment.tags:
            mismatches = 0
            length = 0
            for variant in alignment.tags['cs']:
                if variant.type == 'match':
                    length += variant.value
                elif variant.type == 'mismatch':
                    mismatches += 1
                    length += 1
                elif variant.type == 'insertion':
                    length += len(variant.value)
            if mismatches / length < percent and mismatches < count:
                yield alignment


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Filter aligned reads based on the number of mismatches.'


def define_parser(parser):
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    parser.add_argument('-p', '--percent', default=0.01, type=float)
    parser.add_argument('-c', '--count', default=100, type=int)
    parser.set_defaults(func=init_filter)
    return parser


def init_filter(args):
    input = open(args.input) if args.input else sys.stdin
    output = open(args.output, 'w') if args.output else sys.stdout
    for alignment in mismatch_filter(iter_sam(input), percent=args.percent, count=args.count):
        output.write(alignment.original)


def iter_sam(stream):
    for line in stream:
        if line.startswith('@'):
            yield SamEntry(None, None, None, None, None, None, None, None, None, None, None, {'cs': parse_cs_tag(':1')}, original=line)
        else:
            parts = line.strip().split('\t', 11)
            parts[1] = int(parts[1])
            parts[3] = int(parts[3])
            parts[4] = int(parts[4])
            parts[11] = dict(parse_tag(definition) for definition in parts[11].split('\t'))
            if 'cs' in parts[11]:
                parts[11]['cs'] = parse_cs_tag(parts[11]['cs'])
            parts.append(line)
            yield SamEntry(*parts)


def parse_tag(definition):
    key, type, value = definition.split(':', 2)
    if type == 'i':
        value = int(value)
    elif type == 'f':
        value = float(value)
    elif type not in 'AZ':
        raise ValueError('Unknown tag type "{}". Tag: "{}", value: "{}"'.format(type, key, value))
    return key, value


def parse_cs_tag(definition):
    tokeniser = Tokeniser({
        'sequences': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_',
        'number': '0123456789',
        'variants': ':*+-'
    })
    tokens = tokeniser.tokenise(definition)
    variants = []
    for variant, value in zip(tokens, tokens):
        if variant.value == ':':
            variants.append(Variant('match', int(value.value)))
        elif variant.value == '*':
            variants.append(Variant('mismatch', value.value))
        elif variant.value == '+':
            variants.append(Variant('insertion', value.value))
        elif variant.value == '-':
            variants.append(Variant('deletion', value.value))
        else:
            raise ValueError('Unknown variants type: "{}"'.format(variant.value))
    return variants


if __name__ == '__main__':
    main()
