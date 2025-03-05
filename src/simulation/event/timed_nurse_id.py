from src.simulation.event import TimedOccurrence


class TimedNurseId(TimedOccurrence):
    #nurse id wrapped up with time of next step/event for global queue
    def __init__(self, time: float, nurse_id: int):
        super().__init__(time)
        self._nurse_id = nurse_id

    @property
    def nurse_id(self) -> int:
        return self._nurse_id