import unittest

from src import Simulator
from src.importer import SimImporter


class SimulatorTest(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        self.people_path = "input/people/testPeople2.json"
        self.event_path = "input/events/testEvents2.json"
    def test_sim(self):
        importer = SimImporter(self.graph_path, self.people_path, self.event_path)
        sim = importer.import_data()
        sim.simulate()
if __name__ == '__main__':
    unittest.main()
