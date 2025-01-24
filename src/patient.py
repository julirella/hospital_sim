from .nurse import Nurse
from .node import PatientRoom
from .sim_time import SimTime


class Patient:
    def __init__(self, nurse: Nurse, room: PatientRoom, sim_time: SimTime) -> None:
        self.nurse = nurse
        self.room = room
        self.sim_time = sim_time