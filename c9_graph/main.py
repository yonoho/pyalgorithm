import copy
import heapq
import math
from typing import Set, Dict, Tuple, List
from disjoint_set import DisjointSet


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
        self.has_nagtive_edge = False
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
            if c < 0:
                self.has_nagtive_edge = True
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

    def acyclic_dijkstra(self, start: int, end: int) -> Tuple[int, List[int]]:
        raise NotImplementedError()


class UndirectedGraph(object):
    def __init__(self, vertexes: Set[int], edges: Dict[Tuple[int], int]):
        self.vertexes = vertexes
        self.edges = edges
        self.acyclic = True
        self.has_nagtive_edge = False
        self.adjacency_list = {}
        for v in vertexes:
            self.adjacency_list.setdefault(v, {})
        for (v, w), c in edges.items():
            self.adjacency_list[v][w] = c
            self.adjacency_list[w][v] = c
            if self.acyclic and (v in self.adjacency_list[w] or w in self.adjacency_list[v]):
                self.acyclic = False
            if c < 0:
                self.has_nagtive_edge = True
        # spanning tree related
        self.visited = dict.fromkeys(vertexes, False)
        self.num = dict.fromkeys(vertexes, None)
        self.low = dict.fromkeys(vertexes, None)
        self.parent = dict.fromkeys(vertexes, None)

    def prim(self) -> Set[Tuple[int]]:
        """返回所有的边, 为了方便测试，返回的边的两个顶点是有序的"""
        vertex_records = {v: [False, 0, 0] for v in self.vertexes}  # known, dv, parent_v
        start = list(self.vertexes)[0]
        vertex_records[start][0] = True
        head_v = start
        select_q = []
        while not all([r[0] for r in vertex_records.values()]):
            # feed queue
            for w, cost in self.adjacency_list[head_v].items():
                w_record = vertex_records[w]
                if not w_record[0] and (not w_record[1] or w_record[1] > cost):
                    w_record[1] = cost
                    w_record[2] = head_v
                    heapq.heappush(select_q, (cost, w))
            # pop queue
            while True:
                head_d, head_v = heapq.heappop(select_q)
                if not vertex_records[head_v][0]:
                    vertex_records[head_v][0] = True
                    break
        return {tuple(sorted([v_record[2], v])) for v, v_record in vertex_records.items() if v_record[2]}

    def kruskal(self) -> Set[Tuple[int]]:
        edge_queue = []
        for e, cost in self.edges.items():
            heapq.heappush(edge_queue, (cost, e))
        vertex_set = DisjointSet()
        for v in self.vertexes:
            vertex_set.find(v)
        known_edges = set()
        while len(list(vertex_set.itersets())) > 1:
            cost, edge = heapq.heappop(edge_queue)
            if not vertex_set.connected(*edge):
                known_edges.add(tuple(sorted(list(edge))))
                vertex_set.union(*edge)
        return known_edges

    def depth_first_spanning_tree(self, v: int = None, counter: int = 1):
        if v is None:
            v = min(self.vertexes)
        self.visited[v] = True
        self.num[v] = counter
        counter += 1
        for w in self.adjacency_list[v].keys():
            if not self.visited[w]:
                self.parent[w] = v
                counter = self.depth_first_spanning_tree(w, counter)
        return counter

    def _cal_low(self, v: int):
        sub_low = math.inf
        for w, p in self.parent.items():
            if p == v:
                sub_low = min([sub_low, self._cal_low(w)])
        num_v = self.num[v]
        back_num = math.inf
        for w in self.adjacency_list[v]:
            if w != self.parent[v]:  # back edge
                back_num = min([back_num, self.num[w]])
        low_v = min([num_v, back_num, sub_low])
        self.low[v] = low_v
        return low_v

    def find_articulation_points(self):
        if not all(self.visited.values()):
            self.depth_first_spanning_tree()
        root = [v for v, p in self.parent.items() if not p][0]
        self._cal_low(root)
        points = []
        if len([v for v, p in self.parent.items() if p == root]) > 1:
            points.append(root)
        for v in (self.vertexes - {root}):
            sub_vs = [w for w, p in self.parent.items() if p == v]
            if any([self.low[w] >= self.num[v] for w in sub_vs]):
                points.append(v)
        return set(points)

    @classmethod
    def find_one_circuit(cls, start: int, available_adjacency_vs: Dict[int, List[int]]) -> List[Tuple[int]]:
        edges = [(start, available_adjacency_vs[start].pop())]
        available_adjacency_vs[edges[0][1]].remove(start)
        while edges[-1][1] != edges[0][0]:
            edges.append((edges[-1][1], available_adjacency_vs[edges[-1][1]].pop()))
            available_adjacency_vs[edges[-1][1]].remove(edges[-1][0])
        return edges

    def find_euler_circuit(self, start: int) -> List[int]:
        available_adjacency_vs = {}
        for v, w in self.edges.keys():
            available_adjacency_vs.setdefault(v, []).append(w)
            available_adjacency_vs.setdefault(w, []).append(v)
        euler_path = []
        while any(available_adjacency_vs.values()):
            # 找到一个尚未使用的边
            for v in euler_path:
                if available_adjacency_vs[v]:
                    start = v
                    break
            new_edges = self.find_one_circuit(start, available_adjacency_vs)
            # 拼接
            new_circuit = [e[0] for e in new_edges]
            insert_idx = euler_path.index(start) if euler_path else 0
            euler_path = euler_path[:insert_idx] + new_circuit + euler_path[insert_idx:]
        euler_path.append(euler_path[0])
        return euler_path
