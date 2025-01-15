from .nurse import Nurse
from .node import PatientRoom

class Patient:
    def __init__(self, nurse: Nurse, room: PatientRoom) -> None:
        self.nurse = nurse
        self.room = room