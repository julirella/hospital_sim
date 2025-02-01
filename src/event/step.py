from . import TimedOccurrence
from ..nurse import Nurse


class Step(TimedOccurrence):
    def __init__(self, time: float, nurse: Nurse):
        super().__init__(time)
        self._nurse = nurse

    def run(self):
        pass

    def pause(self, pause_time: float) -> None:
        #TODO should this even exist? Maybe log here?
        pass