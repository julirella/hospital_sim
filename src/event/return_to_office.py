from src import Patient, Nurse, Graph, SimTime
from src.event import PatientEvent


class ReturnToOffice(PatientEvent):

    def __init__(self, patient: Patient, assigned_nurse: Nurse | None,
                 graph: Graph, sim_time: SimTime) -> None:
        super().__init__(100, sim_time.sim_time, 0, patient, assigned_nurse, graph, sim_time)
        #TODO sort out event id

    @property
    def type(self) -> str:
        return 'return_to_office'

    def __create_steps__(self) -> None:
        self.__create_movement_steps__()

    def pause(self) -> None:
        #pause cancels the event, it will never be resumed
        next_step = self.get_next_step()
        next_step.pause(self._sim_time.sim_time)
        self.__log_action_now__("stop")
        self._assigned_nurse.unassign_event()
