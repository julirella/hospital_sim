import csv

from src import Simulator


class LogExporter:
    def __init__(self, simulator: Simulator, nurse_log_path: str, event_log_path: str):
        self.simulator = simulator
        self.nurse_log_path = nurse_log_path
        self.event_log_path = event_log_path
        print("---------------------------UPDATED EXPORTER-----------------------------")


    def export_dicts(self, to_export: list[dict], out_file_path: str, fields) -> None:
        # source: https://www.geeksforgeeks.org/working-csv-files-python
        csvfile = open(out_file_path, "w")
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(to_export)

    def export_nurse_log(self, nurse_log: list[dict]):
        fields = ["time", "nurse", "x", "y", "event", "action", "patient"]
        self.export_dicts(nurse_log, self.nurse_log_path, fields)

    def export_event_log(self, event_log: list[dict]):
        fields = ["time", "event", "action", "patient", "type", "request_level"]
        self.export_dicts(event_log,  self.event_log_path, fields)
        
    def export_data(self):
        nurse_log = self.simulator.nurse_log()
        event_log = self.simulator.event_log()

        self.export_nurse_log(nurse_log)
        self.export_event_log(event_log)