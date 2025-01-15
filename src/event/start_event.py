from abc import abstractmethod

from .event import Event
from src.patient import Patient
from src.nurse import Nurse

class StartEvent(Event):
    def __init__(self, event_id: int, patient: Patient, duration: float, nurse: Nurse | None) -> None:
        Event.__init__(self, event_id, nurse)
        self.patient = patient
        self.duration = duration

    @abstractmethod
    def create_steps(self) -> None:
        pass