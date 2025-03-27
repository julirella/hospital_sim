from src import Graph
from src.importer import Importer


class GenImporter(Importer):
    def __init__(self, graph_file_name: str, entity_file_name: str):
        super().__init__(graph_file_name, entity_file_name)

    def import_people(self):
        entities_json = self.load_json(self.entity_file_name)
        nurse_cnt = entities_json["nurses"]
        patient_lst = entities_json["patients"]


    def import_data(self):
        self.graph: Graph = self._import_graph()

    def max_graph_dst(self):
        return self.graph.max_distance()