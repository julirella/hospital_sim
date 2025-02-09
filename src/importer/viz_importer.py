import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from src.importer import Importer
from src.visualisation import Map, Corridor, Visualiser


class VizImporter(Importer):

    def __init__(self, graph_filename: str, nurse_log_filename: str) -> None:
        super().__init__(graph_filename)
        self.nurse_log_filename = nurse_log_filename

    def import_graphit_graph(self) -> Map:
        self.parse_graphit_graph()

        corridors = []
        for edge in self.edges:
            start = self.nodes[edge[0]].x, self.nodes[edge[0]].y
            end = self.nodes[edge[1]].x, self.nodes[edge[1]].y
            corridors.append(Corridor(start, end))

        return Map(self.patient_rooms, self.nurse_office, corridors)

    def import_nurse_log(self) -> list[DataFrame]:
        df = pd.read_csv(self.nurse_log_filename)
        nurse_ids = df['nurse'].unique().tolist()

        nurse_dfs = []
        for nurse_id in nurse_ids:
            nurse_dfs.append(df[df['nurse'] == nurse_id])

        return nurse_dfs

    def import_data(self) -> Visualiser:
        dept_map = self.import_graphit_graph()
        nurse_dfs = self.import_nurse_log()
        visualiser = Visualiser(dept_map, nurse_dfs)
        return visualiser
