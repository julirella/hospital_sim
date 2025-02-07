from src.importer import Importer
from src.visualisation import Map, Corridor, Visualiser


class VizImporter(Importer):

    def __init__(self, graph_file_name: str) -> None:
        super().__init__(graph_file_name)

    def import_graphit_graph(self) -> Map:
        self.parse_graphit_graph()

        corridors = []
        for edge in self.edges:
            start = self.nodes[edge[0]].x, self.nodes[edge[0]].y
            end = self.nodes[edge[1]].x, self.nodes[edge[1]].y
            corridors.append(Corridor(start, end))

        return Map(self.patient_rooms, self.nurse_office, corridors)

    def import_data(self) -> Visualiser:
        dept_map = self.import_graphit_graph()
        visualiser = Visualiser(dept_map)
        return visualiser
