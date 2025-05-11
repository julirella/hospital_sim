from src.simulation.timed_object import Step
from src.simulation.people.nurse import Nurse


class TimeAtPatient(Step):
    """
    step representing the part of an event that is time spent caring for the patient
    """

    def __init__(self, time: float, nurse: Nurse, duration: float) -> None:
        super().__init__(time, nurse)
        self._duration = duration

    def run(self) -> None:
        self._nurse.time_at_patient()

    def pause(self, pause_time: float) -> float:
        """
        pause the time at patient by calculating remaining time to be spent at the patient
        :param pause_time: the time at which the pause happens
        :return: remaining time at patient
        """
        return self._duration - (self._time - pause_time)