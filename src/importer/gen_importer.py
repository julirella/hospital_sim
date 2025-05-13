from src import Graph
from src.importer import Importer


class GenImporter(Importer):
    """
    class for importing data for event generation
    """
    def __init__(self, graph_file_name: str, entity_file_name: str):
        """
        :param graph_file_name: path to file with department layout graph
        :param entity_file_name: path to file specifying people
        """
        super().__init__(graph_file_name, entity_file_name)

    def import_people(self):
        """
        import people data from files
        """
        entities_json = self.__load_json__(self.entity_file_name)
        nurse_cnt = entities_json["nurses"]
        patient_lst = entities_json["patients"]
        self.nurse_patients = [[] for _ in range(nurse_cnt)] #list containing a list of patient ids for each nurse
        self.patient_cnt = len(patient_lst)
        for patient_id, patient in enumerate(patient_lst):
            nurse_id: int = patient["nurse_id"]
            self.nurse_patients[nurse_id].append(patient_id)

    def import_data(self):
        """
        import graph and people data from files for event generation
        """
        self.graph: Graph = self.__import_graph__()
        self.import_people()

    def max_graph_dst(self):
        return self.graph.max_distance()