import copy
from functools import reduce
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
        self.indegree = {}
        for v in vertexes:
            self.adjacency_list.setdefault(v, {})
            self.indegree[v] = 0
        for (v, w), c in edges.items():
            self.adjacency_list[v][w] = c
            self.indegree[w] += 1
            if self.acyclic and v in self.adjacency_list[w]:
                self.acyclic = False
        self.cur_non_ins = [v for v in vertexes if v not in set(e[1] for e in edges)]

    def _top_sort(self) -> List[int]:
        vertexes = copy.deepcopy(self.vertexes)
        indegree = copy.deepcopy(self.indegree)
        ret = []
        while vertexes:
            v_non_in = self.cur_non_ins.pop()
            vertexes.remove(v_non_in)
            ret.append(v_non_in)
            for w in self.adjacency_list[v_non_in].keys():
                indegree[w] -= 1
                if indegree[w] == 0:
                    self.cur_non_ins.append(w)
        return ret

    @property
    def top_list(self):
        assert self.acyclic, 'top_list not available in cyclic graph.'
        if not hasattr(self, '_top_list'):
            self._top_list = self._top_sort()
        return self._top_list

    def breadth_first_search(self, start: int, end: int) -> Tuple[int, List[int]]:
        cost = 0,
        path = []

        return cost, path
