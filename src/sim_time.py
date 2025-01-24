
class SimTime:
    def __init__(self):
        self.sim_time: float = 0.0

    def get_sim_time(self) -> float:
        return self.sim_time

    def set_sim_time(self, sim_time: float) -> None:
        self.sim_time = sim_time