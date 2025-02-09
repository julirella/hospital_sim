import unittest

from src.importer.viz_importer import VizImporter


class TestVisualiser(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/toScaleLayout.json"
        # self.graph_path = "input/layouts/testLayout.json"
        self.people_path = "input/people/testPeople2.json"
        self.nurse_log_path = "output/nurseLog.csv"

    def test_vis(self):
        importer = VizImporter(self.graph_path, self.people_path, self.nurse_log_path)
        visualiser = importer.import_data()
        visualiser.run()

if __name__ == '__main__':
    unittest.main()
