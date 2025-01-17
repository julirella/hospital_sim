from . import Event
from src.patient import Patient
from src.nurse import Nurse


class Plan(Event):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, nurse: Nurse) -> None:
        super().__init__(event_id, time, duration, patient, nurse)

    def create_steps(self) -> None:
        pass

