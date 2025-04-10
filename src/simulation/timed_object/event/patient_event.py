from abc import abstractmethod

from src import Graph, SimTime
from src.simulation.timed_object.event.event import Event, EventStatus
from src.simulation.timed_object.step.time_at_patient import TimeAtPatient
from src.simulation.people.nurse import Nurse
from src.simulation.people.patient import Patient


class PatientEvent(Event):
    def __init__(self, time: float, duration: float, patient: Patient, assigned_nurse: Nurse | None,
                 graph: Graph, sim_time: SimTime) -> None:
        self._patient = patient
        super().__init__(time, duration, assigned_nurse, graph, sim_time)

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    def __create_steps__(self) -> None:
        #nurse has to be assigned at this point
        #each step needs to happen at the end of it, but also it has to be obvious that the event is in progress
        #so maybe some start event step??
        prev_step_time = self.__create_movement_steps__(self._assigned_nurse.pos, self._patient.room)
        #time there
        self._steps.append(TimeAtPatient(prev_step_time + self._duration, self._assigned_nurse, self._duration))

    @property
    def patient(self) -> Patient:
        return self._patient

    def __start__(self) -> None:
        self.__create_steps__()
        self._assigned_nurse.assign_event(self._event_id, self.patient.patient_id)
        self._status = EventStatus.ACTIVE

    def pause(self) -> None:
        next_step = self.get_next_step()
        self._duration -= next_step.pause(self._sim_time.sim_time)
        self._status = EventStatus.PAUSED
        self.__log_action_now__("pause")
        self._assigned_nurse.unassign_event()

        self._steps = [] #empty steps so that they can be recalculated when resuming

    def __log_action__(self, action: str, time: float) -> None:
        action_dict = {"time": time, "event": self._event_id, "action": action,
                          "patient": self._patient.patient_id, "type": self.type}
        # print(action_dict)
        self._log.append({"time": time, "event": self._event_id, "action": action,
                          "patient": self._patient.patient_id, "type": self.type})