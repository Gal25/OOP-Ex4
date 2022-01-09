import unittest
from unittest import TestCase

from src.API.DiGraph import DiGraph


class DiGraph_test(TestCase):

    def setUp(self):
        self.graph = DiGraph()
        for i in range(5):
            self.graph.add_node(i)
        self.graph.add_edge(0, 1, 1)
        self.graph.add_edge(3, 0, 2)
        self.graph.add_edge(0, 2, 1)
        self.graph.add_edge(1, 3, 3)
        self.graph.add_edge(2, 3, 4)
        self.graph.add_edge(4, 1, 2)
        self.graph.add_edge(3, 4, 1)

    def test_v_size(self):
        self.assertEqual(5, self.graph.v_size())
        self.assertTrue(self.graph.add_node(6))
        self.assertEqual(6, self.graph.v_size())

    def test_e_size(self):
        self.assertEqual(7, self.graph.e_size())
        self.assertTrue(self.graph.add_edge(4, 3, 1))
        self.assertEqual(8, self.graph.e_size())


    def test_all_in_edges_of_node(self):

        self.assertEqual({3: 2}, self.graph.all_in_edges_of_node(0))
        self.graph.add_node(6)
        self.assertEqual({}, self.graph.all_in_edges_of_node(6))


    def test_all_out_edges_of_node(self):
        self.assertEqual({1: 1, 2: 1}, self.graph.all_out_edges_of_node(0))
        self.assertEqual({3: 3}, self.graph.all_out_edges_of_node(1))


    def test_get_mc(self):
        self.assertEqual(12, self.graph.get_mc())

        self.assertTrue(self.graph.remove_node(0))

        self.assertEqual(16, self.graph.get_mc())

    def test_add_edge(self):
        self.assertEqual(7, self.graph.e_size())
        self.assertTrue(self.graph.add_edge(4, 3, 1))
        self.assertEqual(8, self.graph.e_size())
        self.assertEqual(13, self.graph.get_mc())

        self.assertFalse(self.graph.add_edge(0, 1, 1))

        self.assertFalse(self.graph.add_edge(0, 10, 1))
        self.assertEqual(8, self.graph.e_size())
        self.assertEqual(13, self.graph.get_mc())

    def test_add_node(self):
        self.assertEqual(5, self.graph.v_size())
        self.assertTrue(self.graph.add_node(5))
        self.assertEqual(6, self.graph.v_size())
        self.assertEqual(13, self.graph.get_mc())


    def test_remove_node(self):
        self.assertEqual(5, self.graph.v_size())

        self.assertTrue(self.graph.remove_node(4))
        self.assertEqual(4, self.graph.v_size())
        self.assertEqual(15, self.graph.get_mc())


    def test_remove_edge(self):
        self.assertEqual(7, self.graph.e_size())
        self.assertTrue(self.graph.remove_edge(0, 2))
        self.assertEqual(6, self.graph.e_size())
        self.assertEqual(13, self.graph.get_mc())
        self.assertFalse(self.graph.remove_edge(1, 2))
        self.assertEqual(6, self.graph.e_size())
        self.assertEqual(13, self.graph.get_mc())

