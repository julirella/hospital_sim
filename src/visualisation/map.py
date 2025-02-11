import pygame

from src.visualisation.corridor import Corridor
from src.constants import *
from .vis_nurse import VisNurse
from .vis_room import VisRoom
from src.visualisation.vis_patient import VisPatient


class Map:
    def __init__(self, rooms: list[VisRoom], nurse_office: VisRoom, corridors: list[Corridor], nurses: list[VisNurse],
                 patients: list[VisPatient], width: float, height: float, pixels_per_meter: float):
        self.rooms = rooms
        self.nurse_office = nurse_office
        self.corridors = corridors
        self.nurses = nurses
        self.patients = patients
        self.width = width
        self.height = height
        self.pixels_per_meter = pixels_per_meter
        self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))

        self.nurses_in_corridors = []
        #tmp to check nurses print:
        self.nurse_office.add_nurse(self.nurses[0])
        self.nurse_office.add_nurse(self.nurses[1])


        #assuming there will be no weird corridor sticking out further than a room
        # self.width = max(self.rooms + [nurse_office], key=lambda r: r.x).x + ROOM_SIDE_METERS / 2
        # self.height = max(self.rooms + [nurse_office], key=lambda r: r.y).y + ROOM_SIDE_METERS / 2

    def reset(self) -> None:
        #remove all info of nurse positions
        self.nurses_in_corridors = []
        for room in self.rooms + [self.nurse_office]:
            room.remove_nurses()


    def nurse_by_id(self, nurse_id: int) -> VisNurse:
        return self.nurses[nurse_id]

    # def set_nurse_pos_meters(self, nurse_id: int, pos: tuple[float, float]) -> None:
    #     #accepts nurse pos as meters, recalculates to pixels
    #     self.nurses[nurse_id].set_pos(self.scale_point(pos))

    def put_nurse_in_corridor(self, nurse_id: int, pos: tuple[float, float]) -> None:
        #accepts nurse pos in meters
        self.nurses_in_corridors.append(self.nurses[nurse_id])
        self.nurses[nurse_id].set_pos(self.scale_point(pos))

    def put_nurse_in_room(self, nurse_id: int, patient_id: int) -> None:
        room_number = self.patients[patient_id].room_number
        self.rooms[room_number].add_nurse(self.nurses[nurse_id])

    def put_nurse_in_office(self, nurse_id: int) -> None:
        self.nurse_office.add_nurse(self.nurses[nurse_id])

    def scale_point(self, point):
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def surface(self, time: float) -> pygame.surface.Surface:
        self.map_surf.fill('white')

        for corridor in self.corridors:
            pygame.draw.line(self.map_surf, 'black', self.scale_point(corridor.one_end),
                             self.scale_point(corridor.other_end), 5)

        for room in self.rooms + [self.nurse_office]:
            room_surf = room.surface(time)
            self.map_surf.blit(room_surf, self.scale_point((room.x - ROOM_SIDE_METERS / 2, room.y - ROOM_SIDE_METERS / 2)))

        for nurse in self.nurses_in_corridors:
            pygame.draw.circle(self.map_surf, nurse.colour, nurse.pos, 5) #TODO: sort out radius (and corridor width)
        return self.map_surf