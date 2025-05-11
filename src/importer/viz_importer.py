import pandas as pd
import pygame
from pandas.core.interchange.dataframe_protocol import DataFrame

from src.importer import Importer
from src.visualisation.vis_patient import VisPatient
from src.visualisation import Map, Corridor, Visualiser, VisRoom
from src.visualisation.vis_nurse import VisNurse
from src.constants import *


class VizImporter(Importer):
    """
    class for importing visualisation input and constructing the Visualiser object
    """

    def __init__(self, graph_filename: str, entity_file_name: str, nurse_log_filename: str, event_log_filename: str) -> None:
        """
        :param graph_filename: path to file with department layout graph
        :param entity_file_name: path to file specifying people
        :param nurse_log_filename: path to file with nurse logs from a simulation
        :param event_log_filename: path to file with event logs from a simulation
        """

        super().__init__(graph_filename, entity_file_name)
        self.nurse_log_filename = nurse_log_filename
        self.event_log_filename = event_log_filename

        self.corridors = []
        self.patients_in_rooms = []
        self.req_times = {} #dict because not all patients have requests
        self.nurse_logs = {}

    def __import_graphit_graph__(self) -> None:
        # import graphIT department graph and construct corridors
        self.__parse_graphit_graph__()

        for edge in self.edges:
            start = self.nodes[edge[0]].x, self.nodes[edge[0]].y
            end = self.nodes[edge[1]].x, self.nodes[edge[1]].y
            self.corridors.append(Corridor(start, end))


    def __int_to_colour__(self, num: int, total_colours: int) -> pygame.Color:
        # calculate hue value for given integer based on total amount of colors that will be used

        step = 360 // total_colours
        colour = pygame.Color(0, 0, 0, 0)
        colour.hsva = (step * num, 100, 100, 50)
        return colour

    def __import_entities__(self) -> tuple[list[VisNurse], list[VisPatient]]:
        # import nurses and patients from files and construct the corresponding visualisation objects

        entities_json = self.__load_json__(self.entity_file_name)

        nurse_cnt = entities_json["nurses"]
        nurses: list[VisNurse] = []
        for i in range(nurse_cnt):
            if i in self.nurse_logs:
                nurse_log = self.nurse_logs[i]
            else:
                nurse_log = pd.DataFrame()
            nurses.append(VisNurse(self.__int_to_colour__(i, nurse_cnt), nurse_log))

        patient_lst = entities_json["patients"]
        patients: list[VisPatient] = []
        self.patients_in_rooms: list[list[VisPatient]] = [[] for _ in range(len(self.patient_rooms))]
        for i, patient_info in enumerate(patient_lst):
            nurse = patient_info["nurse_id"]
            room = patient_info["room"]

            if i in self.req_times:
                start_times, end_times = self.req_times[i]
            else:
                start_times, end_times = [], []

            patient = VisPatient(self.__int_to_colour__(nurse, nurse_cnt), room, start_times, end_times)
            self.patients_in_rooms[room].append(patient)
            patients.append(patient)

        return nurses, patients

    def __import_nurse_log__(self) -> None:
        # import simulation nurse log from csv file and turn it into a list of dicts for each action
        df = pd.read_csv(self.nurse_log_filename, dtype={'patient': 'Int32'})
        nurse_ids = df['nurse'].unique().tolist()

        for nurse_id in nurse_ids:
            # https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe
            # reset index to start from 0 for each nurse df
            nurse_df = df[df['nurse'] == nurse_id].reset_index(drop=True)
            self.nurse_logs[nurse_id] = nurse_df

    def __import_event_log__(self) -> float:
        # import simulation event log from csv file and turn it into a list of dicts for each action
        # return simulation end time

        event_df = pd.read_csv(self.event_log_filename)
        req_df = event_df[event_df['type'] == "request"]
        patient_ids_float = req_df['patient'].unique().tolist() #ids may be floats because of NaNs
        patient_ids = list(map(lambda x: int(x), patient_ids_float))
        for patient_id in patient_ids:
            patient_reqs = req_df[req_df['patient'] == patient_id]
            start_times = sorted(patient_reqs[patient_reqs['action'] == "planned start"]["time"].tolist())
            end_times = sorted(patient_reqs[patient_reqs['action'] == "end"]["time"].tolist())
            self.req_times[patient_id] = start_times, end_times

        sim_end_time = max(event_df['time'].tolist())
        return sim_end_time

    def import_data(self) -> Visualiser:
        """
        import visualisation data and construct Visualiser
        :return: the constructed Visualiser
        """
        self.__import_graphit_graph__()
        sim_end_time = self.__import_event_log__()
        self.__import_nurse_log__()
        nurses, patients = self.__import_entities__()

        map_width = max(self.patient_rooms + [self.nurse_office], key=lambda r: r.x).x + ROOM_SIDE_METERS / 2
        map_height = max(self.patient_rooms + [self.nurse_office], key=lambda r: r.y).y + ROOM_SIDE_METERS / 2
        width_ratio = MAP_SURF_WIDTH / map_width
        height_ratio = MAP_SURF_HEIGHT / map_height
        pixels_per_meter = int(min(width_ratio, height_ratio))

        vis_rooms = []
        for i, room in enumerate(self.patient_rooms):
            vis_rooms.append(VisRoom(room, pixels_per_meter, self.patients_in_rooms[i]))

        nurse_office = VisRoom(self.nurse_office, pixels_per_meter, [])

        dept_map = Map(vis_rooms, nurse_office, self.corridors, nurses, patients, map_width, map_height,
                       pixels_per_meter)

        visualiser = Visualiser(dept_map, sim_end_time)
        return visualiser
