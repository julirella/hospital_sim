from abc import abstractmethod
from enum import IntEnum

from src import Graph, SimTime
from src.event import Step, Movement
from src.event.time_at_patient import TimeAtPatient
from src.event.timed_occurrence import TimedOccurrence
from src.nurse import Nurse
from src.patient import Patient



class EventStatus(IntEnum):
    NOT_STARTED = 1
    ACTIVE = 2
    PAUSED = 3

class Event(TimedOccurrence):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, assigned_nurse: Nurse | None,
                 graph: Graph, sim_time: SimTime) -> None:
        super().__init__(time)
        self._event_id = event_id
        self._duration = duration
        self._patient = patient
        self._assigned_nurse = assigned_nurse
        self._graph = graph
        self._sim_time = sim_time
        self._status = EventStatus.NOT_STARTED
        self._steps: list[Step] = []
        self._log: list[dict] = []
        self.__log_action__("planned start", self._time)

    @property
    @abstractmethod
    def type(self) -> str:
        # https://stackoverflow.com/questions/2736255/abstract-attributes-in-python
        pass

    def __create_steps__(self) -> None:
        #nurse has to be assigned at this point
        #each step needs to happen at the end of it, but also it has to be obvious that the event is in progress
        #so maybe some start event step??
        nurse_pos = self._assigned_nurse.pos
        patient_pos = self._patient.get_room()
        path_there = self._graph.find_path(nurse_pos, patient_pos)
        prev_step_time = self._time

        #getting there
        from_node = nurse_pos
        for i in range(len(path_there)):
            to_node, dst = path_there[i]
            step_duration = dst / self._assigned_nurse.speed
            step_time = prev_step_time + step_duration
            step = Movement(step_time, self._assigned_nurse, from_node, to_node)
            self._steps.append(step)
            prev_step_time = step_time
            from_node = to_node

        #time there
        self._steps.append(TimeAtPatient(prev_step_time + self._duration, self._assigned_nurse, self._duration))

        #getting back? Is it a separate plan? Is it gonna be sorted out in simulator?
    def __start__(self) -> None:
        self.__create_steps__()
        self._assigned_nurse.assign_event(self._event_id, self._patient.patient_id)
        self._status = EventStatus.ACTIVE

    def __pop_next_step__(self) -> Step:
        step: Step = self._steps.pop(0)
        return step

    def __is_finished__(self) -> bool:
        if len(self._steps) == 0:
            return True
        else:
             return False

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def status(self) -> EventStatus:
        return self._status

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def log(self) -> list[dict]:
        return self._log

    #time of next step, or of event itself if steps have not yet been created
    def next_time(self) -> float:
        if len(self._steps) == 0:
            return self.time
        else:
            return self._steps[0].time

    def get_next_step(self) -> Step:
        #assumes only future steps are in this list
        if self._status == EventStatus.ACTIVE:
            return self._steps[0]
        else:
            raise Exception("get next step can only be called on active event")

    def run_next_step(self) -> bool:
        #runs next step, returns true if it finishes the event
        if self._status == EventStatus.NOT_STARTED:
            self.__start__() #at this point start and resume is the same
            self.__log_action_now__("actual start")
        elif self._status == EventStatus.PAUSED:
            self.__start__()
            self.__log_action_now__("resume")
        else:
            step: Step = self.__pop_next_step__()
            step.run()

        if self.__is_finished__():
            self._assigned_nurse.finish_event()
            self.__log_action_now__("end")

        return self.__is_finished__()

    def pause(self) -> None:
        next_step = self.get_next_step()
        self._duration -= next_step.pause(self._sim_time.get_sim_time())
        self._status = EventStatus.PAUSED
        self.__log_action_now__("pause")
        self._assigned_nurse.unassign_event()

        self._steps = [] #empty steps so that they can be recalculated when resuming

    def __log_action__(self, action: str, time: float) -> None:
        self._log.append({"time": time, "event": self._event_id, "action": action,
                          "patient": self._patient.patient_id, "type": self.type})

    def __log_action_now__(self, action: str) -> None:
        self.__log_action__(action, self._sim_time.get_sim_time())