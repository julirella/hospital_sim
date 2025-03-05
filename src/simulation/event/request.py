from . import PatientEvent
from src.simulation.patient import Patient
from src.simulation.nurse import Nurse
from src import Graph, SimTime


class Request(PatientEvent):
    def __init__(self, time: float, duration: float, patient: Patient, level: int, graph: Graph, sim_time: SimTime) -> None:
        super().__init__(time, duration, patient, None, graph, sim_time)
        self._level = level

    def assign_nurse(self, nurse: Nurse):
        self._assigned_nurse = nurse

    @property
    def level(self) -> int:
        return self._level

    @property
    def type(self) -> str:
        return "request"

