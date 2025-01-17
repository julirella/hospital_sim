from abc import abstractmethod

from src.nurse import Nurse
from src.patient import Patient


class Event:
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, assigned_nurse: Nurse | None) -> None:
        self.event_id = event_id
        self.time = time
        self.duration = duration
        self.patient = patient
        self.assigned_nurse = assigned_nurse

    @abstractmethod
    def create_steps(self) -> None:
        pass