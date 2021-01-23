# $ pytest -sv
import pytest
from .main import Graph, UndirectedGraph


@pytest.fixture
def acyclic_graph():
    vertexes = set(range(1, 8))
    edges = {
        (1, 2): 1,
        (1, 3): 1,
        (1, 4): 1,
        (2, 4): 1,
        (2, 5): 1,
        (3, 6): 1,
        (4, 3): 1,
        (4, 6): 1,
        (4, 7): 1,
        (5, 4): 1,
        (5, 7): 1,
        (7, 6): 1,
    }
    return vertexes, edges


@pytest.fixture
def weighted_acyclic_graph():
    vertexes = set(range(1, 8))
    edges = {
        (1, 2): 2,
        (1, 4): 1,
        (2, 4): 3,
        (2, 5): 10,
        (3, 1): 4,
        (3, 6): 5,
        (4, 3): 2,
        (4, 5): 2,
        (4, 6): 8,
        (4, 7): 4,
        (5, 7): 6,
        (7, 6): 1,
    }
    return vertexes, edges


@pytest.fixture
def weighted_undirected_graph():
    vertexes = set(range(1, 8))
    edges = {
        (1, 2): 2,
        (1, 3): 4,
        (1, 4): 1,
        (2, 4): 3,
        (2, 5): 10,
        (3, 4): 2,
        (3, 6): 5,
        (4, 5): 7,
        (4, 6): 8,
        (4, 7): 4,
        (5, 7): 6,
        (6, 7): 1,
    }
    return vertexes, edges


@pytest.fixture
def unweighted_undirected_graph():
    vertexes = set(range(1, 8))
    edges = {
        (1, 2): 1,
        (1, 4): 1,
        (2, 3): 1,
        (3, 4): 1,
        (3, 7): 1,
        (4, 5): 1,
        (4, 6): 1,
        (5, 6): 1,
    }
    return vertexes, edges


@pytest.fixture
def min_spanning_tree():
    return {
        (1, 2),
        (1, 4),
        (3, 4),
        (4, 7),
        (5, 7),
        (6, 7),
    }


@pytest.fixture
def depth_first_spanning_tree():
    return {
        (1, 2),
        (2, 3),
        (3, 4),
        (3, 7),
        (4, 5),
        (5, 6),
    }


@pytest.fixture
def euler_graph():
    vertexes = set(range(1, 13))
    edges = {
        (1, 3): 1,
        (1, 4): 1,
        (2, 3): 1,
        (2, 8): 1,
        (3, 4): 1,
        (3, 6): 1,
        (3, 7): 1,
        (3, 9): 1,
        (4, 5): 1,
        (4, 7): 1,
        (4, 10): 1,
        (4, 11): 1,
        (5, 10): 1,
        (6, 9): 1,
        (7, 9): 1,
        (7, 10): 1,
        (8, 9): 1,
        (9, 10): 1,
        (9, 12): 1,
        (10, 11): 1,
        (10, 12): 1,
    }
    return vertexes, edges


@pytest.fixture
def articulation_points():
    return {3, 4}


class TestGraph(object):

    def test_top_sort(self, acyclic_graph):
        vertexes, edges = acyclic_graph
        graph = Graph(vertexes, edges)
        top_list = graph.top_list
        for v, w in edges.keys():
            assert top_list.index(v) < top_list.index(w)

    def test_unweighted_shortest_path(self, acyclic_graph):
        vertexes, edges = acyclic_graph
        graph = Graph(vertexes, edges)
        assert graph.breadth_first_search(1, 7)[0] == 2
        assert graph.breadth_first_search(2, 6)[0] == 2
        assert graph.breadth_first_search(1, 4) == (1, [1, 4])
        assert graph.breadth_first_search(1, 1) == (0, [1])

    def test_weighted_shortest_path(self, weighted_acyclic_graph):
        vertexes, edges = weighted_acyclic_graph
        graph = Graph(vertexes, edges)
        assert graph.dijkstra(1, 4) == (1, [1, 4])
        assert graph.dijkstra(1, 2) == (2, [1, 2])
        assert graph.dijkstra(2, 6) == (8, [2, 4, 7, 6])

    def test_prim(self, weighted_undirected_graph, min_spanning_tree):
        vertexes, edges = weighted_undirected_graph
        graph = UndirectedGraph(vertexes, edges)
        assert graph.prim() == min_spanning_tree

    def test_kruskal(self, weighted_undirected_graph, min_spanning_tree):
        vertexes, edges = weighted_undirected_graph
        graph = UndirectedGraph(vertexes, edges)
        assert graph.kruskal() == min_spanning_tree

    def test_depth_first_spanning_tree(self, unweighted_undirected_graph, depth_first_spanning_tree):
        vertexes, edges = unweighted_undirected_graph
        graph = UndirectedGraph(vertexes, edges)
        graph.depth_first_spanning_tree()
        assert set([tuple(sorted([k, v])) for k, v in graph.parent.items() if k in vertexes and v in vertexes]) == depth_first_spanning_tree

    def test_find_articulation_points(self, unweighted_undirected_graph, articulation_points):
        vertexes, edges = unweighted_undirected_graph
        graph = UndirectedGraph(vertexes, edges)
        assert graph.find_articulation_points() == articulation_points

    def test_euler_circuit(self, euler_graph):
        vertexes, edges = euler_graph
        graph = UndirectedGraph(vertexes, edges)
        euler_path = graph.find_euler_circuit(7)
        assert len(euler_path) == len(edges) + 1
        for i in range(len(euler_path) - 1):
            assert tuple(sorted(euler_path[i: i + 2])) in edges
