import unittest

from src.importer.viz_importer import VizImporter


class TestVisualiser(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        # self.graph_path = "input/layouts/testLayout.json"

    def test_vis(self):
        importer = VizImporter(self.graph_path)
        visualiser = importer.import_data()
        visualiser.run()

if __name__ == '__main__':
    unittest.main()
