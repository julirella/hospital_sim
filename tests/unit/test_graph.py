import math
import unittest
from unittest.mock import Mock
from src import Graph, Node, NurseOffice, Junction, PatientRoom
from src.simulation.node.temp_node import TempNode


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
            Junction(2,2, 0),
            Node(3,0, 1),
            Node(4,1, 1),
            Node(5,2, 1),
            Node(6,0, 2),
            Node(7,1, 2),
            Node(8,2, 2),
            NurseOffice(9, 0.5, 0),
            PatientRoom(10, 1.5, 0, 0)
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
        self.graph.add_edge(8, 5)
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

    def test_find_path_temp_node(self):
        tmp_node = TempNode(1.5, 1.5, (4, math.sqrt(2) / 2), (8, math.sqrt(2) / 2))
        path = self.graph.find_path(tmp_node, self.nodes[5])
        expected = [(self.nodes[4], math.sqrt(2) / 2), (self.nodes[5], 1.0)]
        self.assertEqual(expected, path)

    def test_find_path_temp_node2(self):
        tmp_node = TempNode(1.5, 1.5, (4, math.sqrt(2) / 2 + 0.1), (8, math.sqrt(2) / 2 - 0.1))
        path = self.graph.find_path(tmp_node, self.nodes[5])
        expected = [(self.nodes[8], math.sqrt(2) / 2 - 0.1), (self.nodes[5], 1.0)]
        self.assertEqual(expected, path)

    def test_max_distance(self):
        max_dst = self.graph.max_distance()
        self.assertEqual(3 + math.sqrt(2), max_dst)


if __name__ == "__main__":
    unittest.main()