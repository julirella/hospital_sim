import argparse

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
    parser = argparse.ArgumentParser(description="Run the simulation app.")
    parser.add_argument("--graph", type=str, default="input/layouts/toScaleLayout.json",
                        help="Path to the graph layout JSON file.")
    parser.add_argument("--people", type=str, default="input/people/manyPeople.json",
                        help="Path to the people JSON file.")
    parser.add_argument("--events", type=str, default="input/events/testEventsRequests.json",
                        help="Path to the events JSON file.")
    parser.add_argument("--event_output", type=str, default="output/eventLog.csv",
                        help="Path to the event log output CSV file.")
    parser.add_argument("--nurse_output", type=str, default="output/nurseLog.csv",
                        help="Path to the nurse log output CSV file.")
    parser.add_argument("--visualise", action="store_true",
                        help="Run with visualisation.")

    args = parser.parse_args()

    app = App(
        graph_path=args.graph,
        people_path=args.people,
        event_path=args.events,
        nurse_output_path=args.nurse_output,
        event_output_path=args.event_output
    )

    app.run_simulation(visualise=args.visualise)


if __name__ == "__main__":
    main()