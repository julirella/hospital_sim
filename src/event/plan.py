from . import Event
from src.patient import Patient
from src.nurse import Nurse
from .. import Graph


class Plan(Event):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, nurse: Nurse, graph: Graph) -> None:
        super().__init__(event_id, time, duration, patient, nurse, graph)

