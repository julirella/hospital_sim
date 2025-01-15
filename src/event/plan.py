from .start_event import StartEvent
from src.patient import Patient
from src.nurse import Nurse


class Plan(StartEvent):
    def __init__(self, event_id: int, patient: Patient, duration: float, nurse: Nurse) -> None:
        super().__init__(event_id, patient, duration, nurse)
        self.duration = duration

    def create_steps(self) -> None:
        pass

