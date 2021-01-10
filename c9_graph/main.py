import copy
import heapq
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
        self.curr_non_ins = [v for v in vertexes if v not in set(e[1] for e in edges)]

    def _top_sort(self) -> List[int]:
        vertexes = copy.deepcopy(self.vertexes)
        indegree = copy.deepcopy(self.indegree)
        ret = []
        while vertexes:
            v_non_in = self.curr_non_ins.pop()
            vertexes.remove(v_non_in)
            ret.append(v_non_in)
            for w in self.adjacency_list[v_non_in].keys():
                indegree[w] -= 1
                if indegree[w] == 0:
                    self.curr_non_ins.append(w)
        return ret

    @property
    def top_list(self):
        assert self.acyclic, 'top_list not available in cyclic graph.'
        if not hasattr(self, '_top_list'):
            self._top_list = self._top_sort()
        return self._top_list

    def breadth_first_search(self, start: int, end: int) -> Tuple[int, List[int]]:
        known_vertexes = {start: [0, start]}  # dv, parent_v
        head_verts = [start]
        found_end = (end in known_vertexes)
        while not found_end:
            for v in head_verts:
                new_head_verts = []
                for w in self.adjacency_list[v].keys():
                    if w in known_vertexes:
                        continue
                    known_vertexes[w] = [known_vertexes[v][0] + 1, v]
                    new_head_verts.append(w)
                    if w == end:
                        found_end = True
                        break
                if found_end:
                    break
                head_verts = new_head_verts
        cost = known_vertexes[end][0]
        path = [end]
        while path[0] != start:
            path.insert(0, known_vertexes[path[0]][1])
        return cost, path

    def dijkstra(self, start: int, end: int) -> Tuple[int, List[int]]:
        scanned_vertexes = {start: [True, 0, start]}  # known, dv, parent_v
        head_v = start
        head_d = 0
        found_end = False
        select_q = []
        while not found_end:
            for w, cost in self.adjacency_list[head_v].items():
                w_d = head_d + cost
                scanned_vertexes.setdefault(w, [False, w_d, head_v])
                if scanned_vertexes[w][0]:
                    continue
                if w_d < scanned_vertexes[w][1]:
                    scanned_vertexes[w][1:] = w_d, head_v
                heapq.heappush(select_q, (w_d, w))
            while not found_end:
                head_d, head_v = heapq.heappop(select_q)
                if not scanned_vertexes[head_v][0]:
                    scanned_vertexes[head_v][0] = True
                    if head_v == end:
                        found_end = True
                    break
        cost = scanned_vertexes[end][1]
        path = [end]
        while path[0] != start:
            path.insert(0, scanned_vertexes[path[0]][2])
        return cost, path
