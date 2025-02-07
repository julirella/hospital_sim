from src import PatientRoom, NurseOffice
from src.visualisation.corridor import Corridor
from .constants import *


class Map:
    def __init__(self, rooms: list[PatientRoom], nurse_office: NurseOffice, corridors: list[Corridor]):
        self.rooms = rooms
        self.nurse_office = nurse_office
        self.corridors = corridors

        #assuming there will be no weird corridor sticking out further than a room
        self.width = max(self.rooms + [nurse_office], key=lambda r: r.x).x + ROOM_SIDE_METERS / 2
        self.height = max(self.rooms + [nurse_office], key=lambda r: r.y).y + ROOM_SIDE_METERS / 2
