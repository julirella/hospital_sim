import unittest

from src.exporter.log_exporter import LogExporter
from src.importer import SimImporter


class TestLogExporter(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        self.people_path = "input/people/testPeople2.json"
        self.event_path = "input/events/testEventsRequests.json"
        importer = SimImporter(self.graph_path, self.people_path, self.event_path)
        self.sim = importer.import_data()
        self.sim.simulate()
        self.nurse_log_path = "output/nurseLog.csv"
        self.event_log_path = "output/eventLog.csv"

    def test_something(self):
        exporter = LogExporter(self.sim, self.nurse_log_path, self.event_log_path)
        exporter.export_data()


if __name__ == '__main__':
    unittest.main()
