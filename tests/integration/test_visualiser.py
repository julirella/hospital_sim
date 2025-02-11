import unittest

from src.exporter.log_exporter import LogExporter
from src.importer import SimImporter
from src.importer.viz_importer import VizImporter


class TestVisualiser(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/toScaleLayout.json"
        # self.graph_path = "input/layouts/testLayout.json"
        self.people_path = "input/people/testPeople2.json"
        self.nurse_log_path = "output/nurseLog.csv"
        self.event_log_path = "output/eventLog.csv"

    def test_vis(self):
        importer = VizImporter(self.graph_path, self.people_path, self.nurse_log_path, self.event_log_path)
        visualiser = importer.import_data()
        visualiser.run()

    def test_vis_with_sim(self):
        event_path = "input/events/testEventsRequests.json"
        importer = SimImporter(self.graph_path, self.people_path, event_path)
        sim = importer.import_data()
        sim.simulate()
        event_log_path = "output/eventLog.csv"
        exporter = LogExporter(sim, self.nurse_log_path, event_log_path)
        exporter.export_data()
        importer = VizImporter(self.graph_path, self.people_path, self.nurse_log_path, self.event_log_path)
        visualiser = importer.import_data()
        visualiser.run()

if __name__ == '__main__':
    unittest.main()
