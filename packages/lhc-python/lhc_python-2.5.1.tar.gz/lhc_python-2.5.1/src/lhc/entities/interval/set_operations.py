import itertools

from typing import Iterable, Iterator, List, Optional, Sequence, Tuple
from lhc.entities.interval import Interval, IntervalPair


def intersect(a: Interval, b: Interval) -> Interval:
    """ Find the overlap between `a` and `b`. """
    return a.intersect(b)


def difference(a: Interval, b: Interval) -> IntervalPair:
    """ Remove the part of `a` that overlaps with `b`. """
    return a.difference(b)


def multi_difference(a: Interval, bs: Iterable[Interval]) -> List[Interval]:
    """ Return non overlapping intervals between interval `a` and sorted intervals `b`."""
    result = []
    right = a
    for b in bs:
        left, right = right.difference(b)
        result.append(left)
    if right is not None:
        result.append(right)
    return result


def union(a: Interval, b: Interval) -> Optional[Interval]:
    """ Return a single interval that covers `a` and `b` if they overlap or touch. """
    return a.union(b)


def set_intersect(a: Iterator[Interval], b: Iterator[Interval], intersect_intervals=False) -> Iterable[Interval]:
    """ Find all interals from the ordered set `b` that intersect with intervals in the ordered set `a`."""
    def get_b(_: Interval, b_: Interval):
        return b_

    intersect_fn = intersect if intersect_intervals else get_b
    for a_ in a:
        hits = itertools.takewhile(lambda b_: a_.stop > b_.start, b)
        hits = [intersect_fn(a_, b_) for b_ in hits if a_.start < b_.stop]
        yield from hits


def set_query(a: Iterator[Interval], b: Iterator[Interval]) -> Iterable[Tuple[Interval, List[Interval]]]:
    """ For each interval in the ordered set `a` find the intersecting intervals from the ordered set `b`."""
    hits = []
    for a_ in a:
        hits.extend(itertools.takewhile(lambda b_: a_.stop > b_.start, b))
        hits = [b_ for b_ in hits if a_.start < b_.stop]
        yield a_, hits


def set_difference(a: Iterator[Interval], b: Iterator[Interval], difference_intervals=False) -> Iterable[Interval]:
    """ For each interval in the ordered set `a` remove overlaps with intervals from the ordered set `b`. """
    def whole_interval_difference(a__: Interval, hits_: Sequence[Interval]):
        return [] if hits_ else [a__]

    difference_fn = multi_difference if difference_intervals else whole_interval_difference
    for a_ in a:
        hits = itertools.takewhile(lambda b_: a_.stop > b_.start, b)
        hits = [b_ for b_ in hits if a_.start < b_.stop]
        diffs = difference_fn(a_, hits)
        yield from diffs
