import unittest

from src.importer import SimImporter


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        self.people_path = "input/people/testPeople2.json"

    def test_sim_plans_only(self):
        event_path = "input/events/testEvents2.json"
        importer = SimImporter(self.graph_path, self.people_path, event_path)
        sim = importer.import_data()
        sim.simulate()

    def test_sim_plans_and_requests(self):
        event_path = "input/events/testEventsRequests.json"
        importer = SimImporter(self.graph_path, self.people_path, event_path)
        sim = importer.import_data()
        sim.simulate()

if __name__ == '__main__':
    unittest.main()
