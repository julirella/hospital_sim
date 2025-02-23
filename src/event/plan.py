from . import PatientEvent
from src.patient import Patient
from src.nurse import Nurse
from src import Graph, SimTime


class Plan(PatientEvent):
    def __init__(self, time: float, duration: float, patient: Patient, nurse: Nurse, graph: Graph, sim_time: SimTime) -> None:
        super().__init__(time, duration, patient, nurse, graph, sim_time)

    @property
    def type(self) -> str:
        return "plan"
