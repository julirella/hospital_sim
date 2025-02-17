import unittest

from src.exporter.log_exporter import LogExporter
from src.importer import SimImporter
from src.importer.viz_importer import VizImporter


class TestVisualiser(unittest.TestCase):
    def setUp(self):
    #     self.graph_path = "input/layouts/toScaleLayout.json"
    #     # self.graph_path = "input/layouts/testLayout.json"
    #     self.people_path = "input/people/testPeople2.json"
        self.nurse_log_path = "output/nurseLog.csv"
        self.event_log_path = "output/eventLog.csv"

    def run_vis(self, graph_path, people_path, nurse_log_path, event_log_path):
        importer = VizImporter(graph_path, people_path, nurse_log_path, event_log_path)
        visualiser = importer.import_data()
        visualiser.run()

    def run_vis_with_sim(self, graph_path, people_path, event_path, nurse_log_path, event_log_path):
        importer = SimImporter(graph_path, people_path, event_path)
        sim = importer.import_data()
        sim.simulate()
        exporter = LogExporter(sim, nurse_log_path, event_log_path)
        exporter.export_data()
        importer = VizImporter(graph_path, people_path, nurse_log_path, event_log_path)
        visualiser = importer.import_data()
        visualiser.run()

    def run_test(self, graph_path, people_path, nurse_log_path = None, event_log_path = None, sim = False, event_path = None):
        if nurse_log_path is None:
            nurse_log_path = self.nurse_log_path
        if event_log_path is None:
            event_log_path = self.event_log_path

        if sim:
            self.run_vis_with_sim(graph_path=graph_path, people_path=people_path, event_path=event_path,
                                  nurse_log_path=nurse_log_path, event_log_path=event_log_path)
        else:
            self.run_vis(graph_path, people_path, nurse_log_path, event_log_path)

    def test_vis(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/testPeople2.json"
        event_path = "input/events/testEventsRequests.json"

        # self.run_test(graph_path, people_path)
        self.run_test(graph_path, people_path, event_path=event_path, sim=True)

    def test_vis_many_people(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/testEventsRequests.json"

        self.run_test(graph_path=graph_path, people_path=people_path, event_path=event_path, sim=True)





if __name__ == '__main__':
    unittest.main()
