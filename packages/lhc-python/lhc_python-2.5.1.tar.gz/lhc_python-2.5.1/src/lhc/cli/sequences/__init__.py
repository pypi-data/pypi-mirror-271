class Sequence:
    def __init__(self, identifier, sequence, *, data=None):
        self.identifier = identifier
        self.sequence = sequence
        self.data = {} if data is None else data

    def __str__(self):
        return self.sequence

    def __iter__(self):
        return iter(self.sequence)

    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, item):
        return self.sequence[item]


def translate(sequence: str) -> str:
    from lhc.misc.genetic_code import GeneticCodes
    codes = GeneticCodes()
    return codes.translate(sequence)
