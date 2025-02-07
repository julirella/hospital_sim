from src import PatientRoom, NurseOffice
from src.visualisation.corridor import Corridor


class Map:
    def __init__(self, rooms: list[PatientRoom], nurse_office: NurseOffice, corridors: list[Corridor]):
        self.rooms = rooms
        self.nurse_office = nurse_office
        self.corridors = corridors
        self.width, self.height = self.__width_and_height__()

    def __width_and_height__(self) -> tuple[float, float]:
        pass