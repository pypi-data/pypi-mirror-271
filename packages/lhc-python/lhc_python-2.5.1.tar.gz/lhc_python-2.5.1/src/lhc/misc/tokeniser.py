from collections import namedtuple

Token = namedtuple('Token', ('type', 'value'))


class Tokeniser(object):
    def __init__(self, types, individual=None):
        self._type_map = {}
        for type, characters in types.items():
            for character in characters:
                self._type_map[character] = type
        self.individual = set() if individual is None else individual

    def tokenise(self, string):
        type_map = self._type_map
        individual = self.individual

        fr = 0
        while fr < len(string):
            type = type_map[string[fr]]
            to = fr + 1
            while to < len(string) and type == type_map[string[to]] and string[to] not in individual:
                to += 1
            yield Token(type=type, value=string[fr:to])
            fr = to
