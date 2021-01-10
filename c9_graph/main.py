import copy
from typing import Set, Dict, Tuple, List


class Graph(object):
    def __init__(self, vertexes: Set[int], edges: Dict[Tuple[int], int]):
        """
        example:
            - vertexes: {1, 2, 3}
            - edges: {
                (1, 2): 1,
                (2, 3): 2,
                (1, 3): 5,
            }
            - adjacency_list: {
                1: {2: 1, 3: 5},
                2: {3: 2},
                3: {},
            }
        """
        self.vertexes = vertexes
        self.edges = edges
        self.acyclic = True
        self.adjacency_list = {}
        for v in vertexes:
            self.adjacency_list.setdefault(v, {})
        for (v, w), c in edges.items():
            self.adjacency_list[v][w] = c
            if self.acyclic and v in self.adjacency_list[w]:
                self.acyclic = False

    def _top_sort(self) -> List[int]:
        edges = set(self.edges.keys())
        vertexes = copy.deepcopy(self.vertexes)
        ret = []
        while vertexes:
            v_ins = {e[1] for e in edges}
            v_non_ins = [v for v in vertexes if v not in v_ins]
            assert v_non_ins, 'cycle found in top sort.'
            ret.extend(v_non_ins)
            for v in v_non_ins:
                vertexes.remove(v)
            edges = [e for e in edges if e[0] not in v_non_ins]
        return ret

    @property
    def top_list(self):
        assert self.acyclic, 'top_list not available in cyclic graph.'
        if not hasattr(self, '_top_list'):
            self._top_list = self._top_sort()
        return self._top_list
