# $ pytest -sv
import pytest
from .main import Graph


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


class TestGraph(object):

    def test_top_sort(self, acyclic_graph):
        vertexes, edges = acyclic_graph
        graph = Graph(vertexes, edges)
        top_list = graph.top_list
        for v, w in edges.keys():
            assert top_list.index(v) < top_list.index(w)
