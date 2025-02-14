import unittest

from src.importer import SimImporter


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        self.people_path = "input/people/testPeople2.json"

    def run_sim(self, event_path, graph_path=None, people_path=None):
        if graph_path is None:
            graph_path = self.graph_path
        if people_path is None:
            people_path = self.people_path
        importer = SimImporter(graph_path, people_path, event_path)
        sim = importer.import_data()
        sim.simulate()

    def test_sim_plans_only(self):
        event_path = "input/events/testEvents2.json"
        self.run_sim(event_path=event_path)
        # importer = SimImporter(self.graph_path, self.people_path, event_path)
        # sim = importer.import_data()
        # sim.simulate()

    def test_sim_plans_and_requests(self):
        event_path = "input/events/testEventsRequests.json"
        self.run_sim(event_path=event_path)
        # importer = SimImporter(self.graph_path, self.people_path, event_path)
        # sim = importer.import_data()
        # sim.simulate()

    def test_sim_many_people(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/testEventsRequests.json"

        self.run_sim(event_path=event_path, graph_path=graph_path, people_path=people_path)


if __name__ == '__main__':
    unittest.main()
