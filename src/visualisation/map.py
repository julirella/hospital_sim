import pygame
import numpy as np
import pandas as pd

from src.visualisation.corridor import Corridor
from src.constants import *
from .vis_nurse import VisNurse
from .vis_room import VisRoom
from src.visualisation.vis_patient import VisPatient


class Map:
    def __init__(self, rooms: list[VisRoom], nurse_office: VisRoom, corridors: list[Corridor], nurses: list[VisNurse],
                 patients: list[VisPatient], nurse_logs: list[pd.DataFrame], width: float, height: float, pixels_per_meter: int):
        self.rooms = rooms
        self.nurse_office = nurse_office
        self.corridors = corridors
        self.nurses = nurses
        self.patients = patients
        self.nurse_logs = nurse_logs
        self.width = width
        self.height = height
        self.pixels_per_meter = pixels_per_meter
        self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))

        self.nurses_in_corridors = []

    def point_on_line(self, start: tuple[float, float], end: tuple[float, float], time_since_start: float, speed: float):
        dst_covered = time_since_start * speed
        start = np.array(start)
        end = np.array(end)
        direction = end - start
        unit_direction = direction / np.linalg.norm(direction)
        point = start + unit_direction * dst_covered
        return point.tolist()

    def reset(self) -> None:
        #remove all info of nurse positions
        self.nurses_in_corridors = []
        for room in self.rooms + [self.nurse_office]:
            room.remove_nurses()

    def nurse_by_id(self, nurse_id: int) -> VisNurse:
        return self.nurses[nurse_id]

    def put_nurse_in_corridor(self, time, nurse_id: int, prev_row, row_after_time) -> None:
        #accepts nurse pos in meters
        start = prev_row['x'].item(), prev_row['y'].item()
        end = row_after_time['x'].item(), row_after_time['y'].item()
        time_since_start = time - prev_row['time'].item()
        speed = self.nurse_by_id(nurse_id).speed
        nurse_pos = self.point_on_line(start, end, time_since_start, speed)
        self.nurses_in_corridors.append(self.nurses[nurse_id])
        self.nurses[nurse_id].set_pos(self.scale_point(nurse_pos))

    def put_nurse_in_room(self, nurse_id: int, row) -> None:
        patient_id = row['patient']
        room_number = self.patients[patient_id].room_number
        self.rooms[room_number].add_nurse(self.nurses[nurse_id])

    def put_nurse_in_office(self, nurse_id: int) -> None:
        self.nurse_office.add_nurse(self.nurses[nurse_id])

    def scale_point(self, point):
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def update_nurses(self, time):
        # nurses:
        # if nurse is moving, just calculate exact position
        # otherwise figure out what room they're in and put them in the room to be displayed there

        for nurse_id, nurse_log in enumerate(self.nurse_logs):
            if time <= nurse_log.iloc[0]['time']:
                # put nurse in nurse office - assuming nurses always start in office
                self.put_nurse_in_office(nurse_id)
            elif time > nurse_log.iloc[-1]['time']:
                # assuming nurse always ends in room because all events end in room - this will fail if there's a time cut off
                self.put_nurse_in_room(nurse_id, nurse_log.iloc[-1])

            else:
                row_after_time = nurse_log[nurse_log['time'] >= time].iloc[0]
                action = row_after_time['action']

                if action == 'time at patient':
                    self.put_nurse_in_room(nurse_id, row_after_time)
                elif action == 'move to':
                    index_after_time = row_after_time.name.item()
                    prev_row = nurse_log.iloc[index_after_time - 1]
                    self.put_nurse_in_corridor(time, nurse_id, prev_row, row_after_time)
                elif action == 'unassign event' or action == 'assign event':
                    index_after_time = row_after_time.name.item()
                    prev_row = nurse_log.iloc[index_after_time - 1]
                    prev_pos = prev_row['x'].item(), prev_row['y'].item()
                    next_pos = row_after_time['x'].item(), row_after_time['y'].item()
                    if prev_pos == next_pos:  # TODO: check for float problems
                        # nurse is in room
                        self.put_nurse_in_room(nurse_id, prev_row)
                    else:
                        # nurse is walking in corridor
                        self.put_nurse_in_corridor(time, nurse_id, prev_row, row_after_time)
                else:
                    raise Exception('unknown action')  # finish action should probably not come up

    def update(self, time):
        self.reset()
        self.update_nurses(time)

    def surface(self, time: float) -> pygame.surface.Surface:
        self.map_surf.fill('white')

        for corridor in self.corridors:
            pygame.draw.line(self.map_surf, 'black', self.scale_point(corridor.one_end),
                             self.scale_point(corridor.other_end), 5)

        for room in self.rooms + [self.nurse_office]:
            room_surf = room.surface(time)
            self.map_surf.blit(room_surf, self.scale_point((room.x - ROOM_SIDE_METERS / 2, room.y - ROOM_SIDE_METERS / 2)))

        for nurse in self.nurses_in_corridors:
            # pygame.draw.circle(self.map_surf, nurse.colour, nurse.pos, 5)
            nurse.draw(self.map_surf, nurse.pos, self.pixels_per_meter)
        return self.map_surf