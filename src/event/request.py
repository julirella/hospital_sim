from . import Event
from src.patient import Patient
from src.nurse import Nurse


class Request(Event):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, level: int) -> None:
        super().__init__(event_id, time, duration, patient, None)
        self.level = level

    def assign_nurse(self, nurse: Nurse):
        super().nurse = nurse #?? does accessing variables from parent work like this?

    def create_steps(self) -> None:
        pass

