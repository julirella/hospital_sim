from . import TimedOccurrence
from ..nurse import Nurse


class Step(TimedOccurrence):
    def __init__(self, time: float, nurse: Nurse):
        super().__init__(time)
        self.nurse = nurse