from abc import abstractmethod

from src.simulation.timed_object import TimedObject
from src.simulation.people.nurse import Nurse


class Step(TimedObject):
    """
    class representing one step of an event
    """
    def __init__(self, time: float, nurse: Nurse):
        """
        :param time: time of the step end
        :param nurse: nurse making the step
        """
        super().__init__(time)
        self._nurse = nurse

    @abstractmethod
    def run(self):
        """
        run the step
        """
        pass

    @abstractmethod
    def pause(self, pause_time: float) -> float:
        """
        pause the step
        :param pause_time: time at which the step is paused
        :return: remaining time of step if it is a time at patient step, else 0
        """
        pass