from src import Graph
from src.importer import Importer


class GenImporter(Importer):
    def __init__(self, graph_file_name: str, entity_file_name: str):
        super().__init__(graph_file_name, entity_file_name)

    def import_people(self):
        entities_json = self.load_json(self.entity_file_name)
        nurse_cnt = entities_json["nurses"]
        patient_lst = entities_json["patients"]
        self.nurse_patients = [[] for _ in range(nurse_cnt)] #list containing a list of patient ids for each nurse

        for patient_id, patient in enumerate(patient_lst):
            nurse_id: int = patient["nurse_id"]
            self.nurse_patients[nurse_id].append(patient_id)

    def import_data(self):
        self.graph: Graph = self._import_graph()
        self.import_people()

    def max_graph_dst(self):
        return self.graph.max_distance()