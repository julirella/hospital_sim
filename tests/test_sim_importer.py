import unittest

from src.importer import SimImporter
from src.simulator import Simulator


class TestSimImporter(unittest.TestCase):
    def test_import_data(self):
        #currently just tests that it doesn't crash
        graph_file_path = "input/layouts/testLayout.json"
        people_file_path = "input/people/testPeople.json"
        events_file_path = "input/events/testEvents.json"
        sim_importer = SimImporter(graph_file_path, people_file_path, events_file_path)
        simulator: Simulator = sim_importer.import_data()
        assert(len(simulator.nurses) == 2)
        assert(len(simulator.patients) == 2)

