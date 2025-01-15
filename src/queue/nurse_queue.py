from .event_queue import EventQueue
from src.nurse import Nurse
from src.event import Event

class NurseQueue(EventQueue):
    def __init__(self, nurse: Nurse) -> None:
        super().__init__()
        self.nurse = nurse

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        pass