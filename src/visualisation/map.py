from src.visualisation.corridor import Corridor
from .constants import *
from .vis_room import VisRoom


class Map:
    def __init__(self, rooms: list[VisRoom], nurse_office: VisRoom, corridors: list[Corridor]):
        self.rooms = rooms
        self.nurse_office = nurse_office
        self.corridors = corridors

        #assuming there will be no weird corridor sticking out further than a room
        self.width = max(self.rooms + [nurse_office], key=lambda r: r.x).x + ROOM_SIDE_METERS / 2
        self.height = max(self.rooms + [nurse_office], key=lambda r: r.y).y + ROOM_SIDE_METERS / 2
