import unittest

from src import Graph
from src.importer import Importer


class TestImporter(unittest.TestCase):
    def test_graphit_import(self):
        graph_file_path = "input/layouts/testLayout.json"
        importer = Importer(graph_file_path, "")
        graph: Graph = importer.import_graphit_graph()
        # assert len(graph._nodes) == 4
