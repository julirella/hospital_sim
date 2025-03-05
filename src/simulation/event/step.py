from abc import abstractmethod

from . import TimedOccurrence
from src.simulation.nurse import Nurse


class Step(TimedOccurrence):
    def __init__(self, time: float, nurse: Nurse):
        super().__init__(time)
        self._nurse = nurse

    def run(self):
        pass

    @abstractmethod
    def pause(self, pause_time: float) -> float:
        pass