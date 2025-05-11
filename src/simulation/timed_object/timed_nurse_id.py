from src.simulation.timed_object import TimedObject


class TimedNurseId(TimedObject):
    """
    nurse id wrapped up with time of next step/event for global queue
    """
    def __init__(self, time: float, nurse_id: int):
        """
        :param time: time
        :param nurse_id: nurse ID
        """
        super().__init__(time)
        self._nurse_id = nurse_id

    @property
    def nurse_id(self) -> int:
        return self._nurse_id