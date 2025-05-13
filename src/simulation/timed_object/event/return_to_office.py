from src import Nurse, Graph, SimTime
from src.simulation.timed_object import Event, EventStatus


class ReturnToOffice(Event):
    """
    class representing an event in which a nurse returns to the nurses' office
    """

    def __init__(self, assigned_nurse: Nurse,
                 graph: Graph, sim_time: SimTime) -> None:
        """
        :param assigned_nurse: nurse that is returning to the nurses' office
        :param graph: department graph
        :param sim_time: SimTime object to track simulation time
        """
        super().__init__(sim_time.sim_time, 0, assigned_nurse, graph, sim_time)

    @property
    def type(self) -> str:
        return 'return_to_office'

    def __create_steps__(self) -> None:
        # calculate movement steps to get to the office
        self.__create_movement_steps__(self._assigned_nurse.pos, self._graph.nurse_office)

    def pause(self) -> None:
        """
        pause the event, effectively cancelling it since it will never be resumed
        :return:
        """
        if self.status == EventStatus.ACTIVE:
            next_step = self.get_next_step()
            next_step.pause(self._sim_time.sim_time)
            self._assigned_nurse.unassign_event()
        self.__log_action_now__("stop")
