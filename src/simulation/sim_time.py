
class SimTime:
    """
    Class for keeping track of simulation time, used as a singleton
    """
    def __init__(self):
        self._sim_time: float = 0.0

    @property
    def sim_time(self) -> float:
        return self._sim_time

    @sim_time.setter
    def sim_time(self, sim_time: float) -> None:
        self._sim_time = sim_time