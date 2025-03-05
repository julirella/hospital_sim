from src.simulation.event import Step
from src.simulation.nurse import Nurse


class TimeAtPatient(Step):

    def __init__(self, time: float, nurse: Nurse, duration: float) -> None:
        super().__init__(time, nurse)
        self._duration = duration

    def run(self) -> None:
        self._nurse.time_at_patient()

    def pause(self, pause_time: float) -> float:
        return self._duration - (self._time - pause_time) #TODO sort out this weird method