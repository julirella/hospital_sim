from abc import abstractmethod

from src.simulation.timed_object import TimedObject
from src.simulation.people.nurse import Nurse


class Step(TimedObject):
    def __init__(self, time: float, nurse: Nurse):
        super().__init__(time)
        self._nurse = nurse

    def run(self):
        pass

    @abstractmethod
    def pause(self, pause_time: float) -> float:
        pass