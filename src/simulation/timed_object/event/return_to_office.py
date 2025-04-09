from src import Nurse, Graph, SimTime
from src.simulation.timed_object import Event, EventStatus


class ReturnToOffice(Event):

    def __init__(self, assigned_nurse: Nurse,
                 graph: Graph, sim_time: SimTime) -> None:
        super().__init__(sim_time.sim_time, 0, assigned_nurse, graph, sim_time)

    @property
    def type(self) -> str:
        return 'return_to_office'

    def __create_steps__(self) -> None:
        self.__create_movement_steps__(self._assigned_nurse.pos, self._graph.nurse_office)

    def pause(self) -> None:
        #pause cancels the event, it will never be resumed
        if self.status == EventStatus.ACTIVE:
            next_step = self.get_next_step()
            next_step.pause(self._sim_time.sim_time)
            self._assigned_nurse.unassign_event()
        self.__log_action_now__("stop")
