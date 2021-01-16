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
def min_spanning_tree():
    return {
        (1, 2),
        (1, 4),
        (3, 4),
        (4, 7),
        (5, 7),
        (6, 7),
    }


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
