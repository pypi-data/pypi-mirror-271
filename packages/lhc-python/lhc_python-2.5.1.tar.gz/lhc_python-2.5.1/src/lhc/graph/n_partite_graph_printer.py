from itertools import repeat
from .graph import Graph


class NPartiteGraphPrinter:
	def print_graph(self, graph, name, shapes):
        res = ['digraph {} {{'.format(name)]
        for partition, shape in zip(graph.partitions, shapes):
            for vertex in partition:
                res.append('    "{}" [shape={},label="{}"];'.format(hash(vertex), shape, vertex))
        x = list(graph.es)
        for fr, to in sorted(graph.es):
            res.append('    "{}" -> "{}";'.format(hash(fr), hash(to)))
        res.append('}')
        return '\n'.join(res)
