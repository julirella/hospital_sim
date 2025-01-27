from . import Event
from src.patient import Patient
from src.nurse import Nurse
from .. import Graph


class Request(Event):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, level: int, graph: Graph) -> None:
        super().__init__(event_id, time, duration, patient, None, graph)
        self.__level = level

    def assign_nurse(self, nurse: Nurse):
        self._assigned_nurse = nurse

    def get_level(self) -> int:
        return self.__level