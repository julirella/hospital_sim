from src.event import Step
from src.nurse import Nurse


class TimeAtPatient(Step):

    def __init__(self, time: float, nurse: Nurse, duration: float) -> None:
        super().__init__(time, nurse)
        self.duration = duration

    def run(self) -> None:
        self._nurse.time_at_patient()

    def pause(self, pause_time: float) -> float:
        return self.duration - (self._time - pause_time) #TODO sort out this weird method