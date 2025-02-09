import csv

from src import Simulator


class LogExporter:
    def __init__(self, simulator: Simulator, nurse_log_path: str, event_log_path: str):
        self.simulator = simulator
        self.nurse_log_path = nurse_log_path
        self.event_log_path = event_log_path


    def export_dicts(self, to_export: list[dict], out_file_path: str ) -> None:
        # source: https://www.geeksforgeeks.org/working-csv-files-python
        fields = to_export[0].keys()
        csvfile = open(out_file_path, "w")
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(to_export)

    def export_data(self):
        nurse_log = self.simulator.nurse_log()
        event_log = self.simulator.event_log()

        self.export_dicts(nurse_log, self.nurse_log_path)
        self.export_dicts(event_log, self.event_log_path)