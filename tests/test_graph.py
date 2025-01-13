# import pytest
import sys
import os
sys.path.insert(1, str(os.getcwd()) + '/src') #https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
from graph import Graph
from node import Node

class TestGraph:
    def test_find_path(self):
        nodes = [Node(0, 0, 0), Node(1, 0, 0), Node(2, 0, 0), Node(3, 0, 0), Node(4, 0, 0)]
        edges = [
            [(nodes[1], 1), (nodes[2], 2)],
            [(nodes[0], 1), (nodes[2], 1), (nodes[3], 1)],
            [(nodes[0], 2), (nodes[1], 1), (nodes[3], 2), (nodes[4], 1)],
            [(nodes[1], 1), (nodes[2], 2), (nodes[4], 1)],
            [(nodes[2], 1), (nodes[3], 1)]
        ]
        graph = Graph(nodes, edges)
        path = graph.find_path(nodes[0], nodes[4])
        print(path)
        assert path == [nodes[0], nodes[1], nodes[3], nodes[4]] or path == [nodes[0], nodes[2], nodes[4]] or path == [nodes[0], nodes[1], nodes[2], nodes[4]]


test = TestGraph()
test.test_find_path()