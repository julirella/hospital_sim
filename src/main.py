# from src.exporter.log_exporter import LogExporter
import sys
print(sys.path)
from src.exporter import LogExporter
from src.importer import SimImporter
from src.importer.viz_importer import VizImporter


class App:
    def __init__(self, graph_path, people_path, event_path, nurse_output_path, event_output_path):
        self.graph_path = graph_path
        self.people_path = people_path
        self.event_path = event_path
        self.nurse_output_path = nurse_output_path
        self.event_output_path = event_output_path

    def run_simulation(self, visualise=False):
        importer = SimImporter(self.graph_path, self.people_path, self.event_path)
        sim = importer.import_data()
        sim.simulate()
        log_exporter = LogExporter(sim, self.nurse_output_path, self.event_output_path)
        log_exporter.export_data()

        if visualise:
            self.run_visualisation()

    def run_visualisation(self):
        importer = VizImporter(self.graph_path, self.people_path, self.nurse_output_path, self.event_output_path)
        visualiser = importer.import_data()
        visualiser.run()


def main():
    graph_path = "input/layouts/toScaleLayout.json"
    people_path = "input/people/manyPeople.json"
    event_path = "input/events/testEventsRequests.json"
    event_output = "output/eventLog.csv"
    nurse_output = "output/nurseLog.csv"
    app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
              nurse_output_path=nurse_output, event_output_path=event_output)

    app.run_simulation(visualise=True)


if __name__ == "__main__":
    main()