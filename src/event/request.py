from .start_event import StartEvent
from src.patient import Patient
from src.nurse import Nurse


class Request(StartEvent):
    def __init__(self, event_id: int, patient: Patient, level: int, duration: float, nurse: Nurse | None=None) -> None:
        super().__init__(event_id, patient, duration, nurse)
        self.level = level
        self.duration = duration
        self.nurse: Nurse | None = None

    def assign_nurse(self, nurse: Nurse):
        self.nurse = nurse

    def create_steps(self) -> None:
        pass

