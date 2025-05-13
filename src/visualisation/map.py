import pygame
import numpy as np
import pandas as pd

from src.visualisation.corridor import Corridor
from src.constants import *
from .vis_nurse import VisNurse
from .vis_room import VisRoom
from src.visualisation.vis_patient import VisPatient


class Map:
    """
    class representing the department map for visualisation
    """
    def __init__(self, rooms: list[VisRoom], nurse_office: VisRoom, corridors: list[Corridor], nurses: list[VisNurse],
                 patients: list[VisPatient], width: float, height: float, pixels_per_meter: int) -> None:
        """
        :param rooms: list of visualisation rooms in the department
        :param nurse_office: the nurse office VisRoom object
        :param corridors: list of corridors in the department
        :param nurses: list of nurses in the department
        :param patients: list of patients in the department
        :param width: width of the department map
        :param height: height of the department map
        :param pixels_per_meter: how many pixels does it take to draw a meter in the visualisation
        """
        self.rooms = rooms
        self.nurse_office = nurse_office
        self.corridors = corridors
        self.nurses = nurses
        self.patients = patients
        self.width = width
        self.height = height
        self.pixels_per_meter = pixels_per_meter

        # prepare the map surface
        self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))

        self.nurses_in_corridors = []

    def __point_on_line__(self, start: tuple[float, float], end: tuple[float, float], time_since_start: float,
                          speed: float) -> tuple[float, float]:
        # calculate current location of a point on a line based on its speed and time moving since start (yep, the point is a nurse)

        dst_covered = time_since_start * speed
        start = np.array(start)
        end = np.array(end)
        direction = end - start
        unit_direction = direction / np.linalg.norm(direction)
        point = start + unit_direction * dst_covered
        return point.tolist()

    def __reset__(self) -> None:
        # remove all info of nurse positions
        self.nurses_in_corridors = []
        for room in self.rooms + [self.nurse_office]:
            room.remove_nurses()

    def __nurse_by_id__(self, nurse_id: int) -> VisNurse:
        return self.nurses[nurse_id]

    def __put_nurse_in_corridor__(self, time: float, nurse_id: int, prev_row, row_after_time) -> None:
        # calculate where in the corridors the nurse is at the given time based on two consecutive dataframe rows from
        # their log (prev_row and row_after_time), save the position and add nurse to list of nurses currently in corridors
        # positions in df rows are in meters

        start = prev_row['x'].item(), prev_row['y'].item()
        end = row_after_time['x'].item(), row_after_time['y'].item()
        time_since_start = time - prev_row['time'].item()
        speed = self.__nurse_by_id__(nurse_id).speed
        nurse_pos = self.__point_on_line__(start, end, time_since_start, speed)
        self.nurses_in_corridors.append(self.nurses[nurse_id])
        self.nurses[nurse_id].set_pos(self.__scale_point__(nurse_pos))

    def __put_nurse_in_room__(self, nurse_id: int, row) -> None:
        # figure out which room the nurse is in based on a dataframe row from their log, add the nurse to the room
        patient_id = row['patient']
        if pd.isna(patient_id):
            self.__put_nurse_in_office__(nurse_id)
        else:
            room_number = self.patients[patient_id].room_number
            self.rooms[room_number].add_nurse(self.nurses[nurse_id])

    def __put_nurse_in_office__(self, nurse_id: int) -> None:
        self.nurse_office.add_nurse(self.nurses[nurse_id])

    def __scale_point__(self, point: tuple[float, float]) -> tuple[float, float]:
        # transform a point in meter coordinates into pixel coordinates
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def __update_nurses__(self, time):
        # figure out position of each nurse from their log at the given time, then save the position
        # if nurse is moving through a corridor, just calculate exact position in the corridor
        # otherwise figure out what room they're in and put them in the room to be displayed there

        for nurse_id, nurse in enumerate(self.nurses):
            nurse_log = nurse.nurse_log
            if nurse_log.size == 0 or time <= nurse_log.iloc[0]['time']:
                # put nurse in nurse office - assuming nurses always start in office
                # also if nurse has no log, they were in the office the whole time
                self.__put_nurse_in_office__(nurse_id)
            elif time > nurse_log.iloc[-1]['time']:
                # assuming nurse always ends in room because all events end in room - this will fail if there's a time cut off
                self.__put_nurse_in_room__(nurse_id, nurse_log.iloc[-1])

            else:
                row_after_time = nurse_log[nurse_log['time'] >= time].iloc[0]
                action = row_after_time['action']

                if action == 'time at patient':
                    self.__put_nurse_in_room__(nurse_id, row_after_time)
                elif action == 'move to':
                    index_after_time = row_after_time.name.item()
                    prev_row = nurse_log.iloc[index_after_time - 1]
                    self.__put_nurse_in_corridor__(time, nurse_id, prev_row, row_after_time)
                elif action == 'unassign event' or action == 'assign event':
                    index_after_time = row_after_time.name.item()
                    prev_row = nurse_log.iloc[index_after_time - 1]
                    prev_pos = prev_row['x'].item(), prev_row['y'].item()
                    next_pos = row_after_time['x'].item(), row_after_time['y'].item()
                    if prev_pos == next_pos:
                        # nurse is in room
                        self.__put_nurse_in_room__(nurse_id, prev_row)
                    else:
                        # nurse is walking in corridor
                        self.__put_nurse_in_corridor__(time, nurse_id, prev_row, row_after_time)
                else:
                    raise Exception('unknown action')  # finish action should probably not come up

    def update_surface(self, time: float) -> pygame.surface.Surface:
        """
        draw department state at the given time onto the map surface
        :param time: the given time
        :return: the prepared map surface
        """

        # figure out nurse positions at time
        self.__reset__()
        self.__update_nurses__(time)

        # draw map background
        self.map_surf.fill('white')

        # draw corridors
        for corridor in self.corridors:
            pygame.draw.line(self.map_surf, 'black', self.__scale_point__(corridor.one_end),
                             self.__scale_point__(corridor.other_end), 5)

        # draw rooms (and patients and nurses in them)
        for room in self.rooms + [self.nurse_office]:
            room_surf = room.surface(time)
            self.map_surf.blit(room_surf, self.__scale_point__((room.x - ROOM_SIDE_METERS / 2, room.y - ROOM_SIDE_METERS / 2)))

        # draw nurses in corridors
        for nurse in self.nurses_in_corridors:
            nurse.draw(self.map_surf, nurse.pos, self.pixels_per_meter)

        return self.map_surf