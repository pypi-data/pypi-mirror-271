from itertools import repeat
from .graph import Graph


class NPartiteGraph:
    def __init__(self, n=2):
        self.graph = Graph()
        self.partitions = [set_constructor() for set_constructor in repeat(set, n)]

    def __len__(self):
        return len(self.graph.vs)

    def add_vertex(self, v, partition):
        """ Add a vertex to the graph

        :param v: vertex name
        :param partition: partition to add to
        """
        self.graph.add_vertex(v)
        self.partitions[partition].add(v)

    def add_edge(self, fr, to):
        """ Add an outward edge to a vertex

        :param fr: The source vertex.
        :param to: The name of the outward edge.
        """
        if fr not in set(self.graph.vs):  # ToDo: find out why item can be in set but not dict
            raise ValueError('can not connect unknown vertices in n-partite graphs, {!r} missing'.format(fr))
        elif to not in set(self.graph.vs):
            raise ValueError('can not connect unknown vertices in n-partite graphs, {!r} missing'.format(to))
        self.graph.add_edge(fr, to)

    def get_parents(self, n):
        """ Get the parents of a vertex or edge.

        :param n: A vertex or edge.
        :return: The children of the given vertex or edge.
        """
        return self.graph.get_parents(n)

    def get_children(self, n):
        """ Get the children of a vertex or edge.

        :param n: A vertex or edge.
        :return: The children of the given vertex or edge.
        """
        return self.graph.get_children(n)

    def update(self, other):
        for self_partition, other_partition in zip(self.partitions, other.partitions):
            self_partition.update(other_partition)
        self.graph.update(other.graph)
