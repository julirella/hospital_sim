from .event import Event
from ..nurse import Nurse


class Step(Event):
    def __init__(self, event_id: int, nurse: Nurse):
        super().__init__(event_id, nurse)