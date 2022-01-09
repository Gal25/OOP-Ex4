
from unittest import TestCase

from src.API.DiGraph import DiGraph
from src.API.GraphAlgo import GraphAlgo


class GraphAlgo_test(TestCase):

    def setUp(self) -> None:
        self.graph = None
        self.g_algo = GraphAlgo()


    def test_shortest_path(self):
        """
            Test for the shortest paths
        """
        g = DiGraph()
        for i in range(5):
            g.add_node(i)
        g.add_edge(0, 1, 1)
        g.add_edge(3, 0, 2)
        g.add_edge(0, 2, 1)
        g.add_edge(1, 3, 3)
        g.add_edge(2, 3, 4)
        g.add_edge(4, 1, 2)
        g.add_edge(3, 4, 1)
        self.g_algo.graph = g

        self.assertEqual("(4, [0, 1, 3])", str(self.g_algo.shortest_path(0, 3)))
        self.assertEqual("(1, [0, 2])", str(self.g_algo.shortest_path(0, 2)))
        self.assertEqual("(6, [1, 3, 0, 2])", str(self.g_algo.shortest_path(1, 2)))
        self.assertEqual("(4, [2, 3])", str(self.g_algo.shortest_path(2, 3)))
        self.assertEqual("(5, [0, 1, 3, 4])", str(self.g_algo.shortest_path(0, 4)))

    def test_centerPoint(self):
        """
            Check for the centers of the graphs given in the json files
        """
        g = DiGraph()  # creates a undirected graph
        for n in range(5):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 5)
        g.add_edge(2, 3, 1.1)
        gAlgo0 = GraphAlgo(g)
        self.assertEqual((None, float('inf')), gAlgo0.centerPoint())




    def test_tsp(self):
        """
            Test for the tsp
        """
        g = DiGraph()
        for i in range(3):
            g.add_node(i)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 0, 6)
        self.g_algo.graph = g


        l = [0, 1, 2]

        self.assertEqual("([0, 1, 2], 3)", str(self.g_algo.TSP(l)))