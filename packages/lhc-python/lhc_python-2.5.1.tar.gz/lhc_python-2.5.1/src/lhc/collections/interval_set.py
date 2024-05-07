import collections
from typing import Sequence

from lhc.entities.interval import Interval, IntervalBinner


class IntervalSet:
    def __init__(self, intervals: Sequence[Interval] = ()):
        self._len = 0

        self._binner = IntervalBinner()
        self._bins = collections.defaultdict(list)

        for interval in intervals:
            self.add(interval)

    def __iter__(self):
        for bin_ in self._bins.values():
            yield from bin_

    def __len__(self) -> int:
        return self._len

    def __contains__(self, item: Interval):
        return item in self.fetch(item)

    def __getitem__(self, item: Interval):
        return self.fetch(item)

    def add(self, item: Interval):
        self._bins[self._binner.get_bin(item)].append(item)
        self._len += 1

    def fetch(self, item: Interval):
        bins = self._binner.get_overlapping_bins(item)
        for fr, to in bins:
            for bin_ in range(fr, to):
                for interval in self._bins[bin_]:
                    if interval.overlaps(item):
                        yield interval
