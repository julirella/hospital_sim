from .nurse import Nurse
from .node import PatientRoom
from .sim_time import SimTime


class Patient:
    def __init__(self, nurse: Nurse, room: PatientRoom, sim_time: SimTime) -> None:
        self.__nurse = nurse
        self.__room = room
        self.__sim_time = sim_time

    def get_nurse(self) -> Nurse:
        return self.__nurse

    def get_room(self) -> PatientRoom:
        return self.__room