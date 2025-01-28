from . import Event
from src.patient import Patient
from src.nurse import Nurse
from src import Graph, SimTime


class Plan(Event):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, nurse: Nurse, graph: Graph, sim_time: SimTime) -> None:
        super().__init__(event_id, time, duration, patient, nurse, graph, sim_time)

