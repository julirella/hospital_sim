# import pytest
import math
import sys
import os
import unittest
from unittest.mock import Mock

# sys.path.insert(1, str(os.getcwd()) + '/src') #https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
# sys.path.insert(1, str(os.getcwd())) #https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
# from __graph import Graph
# from node import Node
from src import Graph, Node

class TestGraph(unittest.TestCase):

    def setUp(self):
        """
        Creates a test graph with the following structure (almost)

                N1 ---- N2 ---- N3
                |       |       |
                |       |       |
                N4 ---- N5 ---- N6
                |       |       |
                |       |       |
                N7 ---- N8 ---- N9
        """
        # Create nodes with specific coordinates
        self.nodes = [
            Node(0,0, 0),
            Node(1,1, 0),
            Node(2,2, 0),
            Node(3,0, 1),
            Node(4,1, 1),
            Node(5,2, 1),
            Node(6,0, 2),
            Node(7,1, 2),
            Node(8,2, 2),
            Node(9, 0.5, 0),
            Node(10, 1.5, 0)
        ]
        self.nurse_office = Mock()
        self.patient_rooms = Mock()

        # Create the graph
        self.graph = Graph(self.nodes, self.nurse_office, self.patient_rooms)

        self.graph.add_edge(0, 9)
        self.graph.add_edge(9, 1)
        self.graph.add_edge(1, 10)
        self.graph.add_edge(10, 2)
        self.graph.add_edge(0, 9)
        self.graph.add_edge(0, 4)
        self.graph.add_edge(2, 4)


        self.graph.add_edge(3, 4)
        self.graph.add_edge(4, 5)
        self.graph.add_edge(6, 7)
        self.graph.add_edge(7, 8)

        self.graph.add_edge(3, 6)
        self.graph.add_edge(4, 7)
        self.graph.add_edge(4, 8)

    def test_find_path_basic(self):
        path = self.graph.find_path(self.nodes[0], self.nodes[7])
        expected = [(self.nodes[4], math.sqrt(2)), (self.nodes[7], 1)]
        self.assertEqual(expected, path)

    def test_find_path_more_nodes(self):
        path = self.graph.find_path(self.nodes[2], self.nodes[0])
        expected = [(self.nodes[10], 0.5), (self.nodes[1], 0.5), (self.nodes[9], 0.5), (self.nodes[0], 0.5)]
        self.assertEqual(expected, path)

if __name__ == "__main__":
    unittest.main()