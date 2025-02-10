import pandas as pd
import pygame
from pandas.core.interchange.dataframe_protocol import DataFrame

from src.importer import Importer
from src.visualisation.vis_patient import VisPatient
from src.visualisation import Map, Corridor, Visualiser, VisRoom
from src.visualisation.vis_nurse import VisNurse
from src.constants import *


class VizImporter(Importer):

    def __init__(self, graph_filename: str, entity_file_name: str, nurse_log_filename: str) -> None:
        super().__init__(graph_filename, entity_file_name)
        self.nurse_log_filename = nurse_log_filename
        self.corridors = []
        self.patients_in_rooms = []

    def import_graphit_graph(self) -> None:
        self.parse_graphit_graph()

        for edge in self.edges:
            start = self.nodes[edge[0]].x, self.nodes[edge[0]].y
            end = self.nodes[edge[1]].x, self.nodes[edge[1]].y
            self.corridors.append(Corridor(start, end))


    def int_to_colour(self, num: int, total_colours: int) -> pygame.Color:
        step = 360 // total_colours
        colour = pygame.Color(0, 0, 0, 0)
        colour.hsva = (step * num, 100, 100, 50)
        return colour

    def import_entities(self) -> tuple[list[VisNurse], list[VisPatient]]:
        entities_json = self.load_json(self.entity_file_name)

        nurse_cnt = entities_json["nurses"]
        nurses: list[VisNurse] = []
        for i in range(nurse_cnt):
            nurses.append(VisNurse(self.int_to_colour(i, nurse_cnt)))

        patient_lst = entities_json["patients"]
        patients: list[VisPatient] = []
        self.patients_in_rooms: list[list[VisPatient]] = [[] for _ in range(len(self.patient_rooms))]
        for i, patient_info in enumerate(patient_lst):
            nurse = patient_info["nurse_id"]
            room = patient_info["room"]
            patient = VisPatient(self.int_to_colour(nurse, nurse_cnt), room)
            self.patients_in_rooms[room].append(patient)
            patients.append(patient)

        return nurses, patients

    def import_nurse_log(self) -> list[DataFrame]:
        df = pd.read_csv(self.nurse_log_filename)
        nurse_ids = df['nurse'].unique().tolist()

        nurse_dfs = []
        for nurse_id in nurse_ids:
            # https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe
            # reset index to start from 0 for each nurse df
            nurse_dfs.append(df[df['nurse'] == nurse_id].reset_index(drop=True))

        return nurse_dfs

    def import_data(self) -> Visualiser:
        self.import_graphit_graph()
        nurses, patients = self.import_entities()

        map_width = max(self.patient_rooms + [self.nurse_office], key=lambda r: r.x).x + ROOM_SIDE_METERS / 2
        map_height = max(self.patient_rooms + [self.nurse_office], key=lambda r: r.y).y + ROOM_SIDE_METERS / 2
        width_ratio = MAP_SURF_WIDTH / map_width
        height_ratio = MAP_SURF_HEIGHT / map_height
        pixels_per_meter = min(width_ratio, height_ratio)

        vis_rooms = []
        for i, room in enumerate(self.patient_rooms):
            vis_rooms.append(VisRoom(room, pixels_per_meter, self.patients_in_rooms[i]))

        nurse_office = VisRoom(self.nurse_office, pixels_per_meter, [])

        dept_map = Map(vis_rooms, nurse_office, self.corridors, nurses, patients, map_width, map_height, pixels_per_meter)
        nurse_dfs = self.import_nurse_log()
        visualiser = Visualiser(dept_map, nurse_dfs)
        return visualiser
