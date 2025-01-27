from abc import abstractmethod
from enum import IntEnum
from operator import truediv

from src import Graph
from src.event import Step, Movement
from src.event.time_at_patient import TimeAtPatient
from src.event.timed_occurrence import TimedOccurrence
from src.nurse import Nurse
from src.patient import Patient

NURSE_KPH = 4
NURSE_PPS = 30 #pixels per second

class EventStatus(IntEnum):
    NOT_STARTED = 1
    ACTIVE = 2
    PAUSED = 3

class Event(TimedOccurrence):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, assigned_nurse: Nurse | None, graph: Graph) -> None:
        super().__init__(time)
        self.__event_id = event_id
        self.__duration = duration
        self.__patient = patient
        self._assigned_nurse = assigned_nurse
        self.__graph = graph
        self.__status = EventStatus.NOT_STARTED
        self.__steps: list[Step] = []

    def __create_steps__(self) -> None:
        #nurse has to be assigned at this point
        #each step needs to happen at the end of it, but also it has to be obvious that the event is in progress
        #so maybe some start event step??
        nurse_pos = self._assigned_nurse.get_pos()
        patient_pos = self.__patient.__room
        path_there = self.__graph.find_path(nurse_pos, patient_pos)
        prev_step_time = self._time

        #getting there
        from_node = nurse_pos
        for i in range(len(path_there)):
            to_node, dst = path_there[i]
            step_duration = dst / NURSE_PPS #TODO: sort out this conversion
            step_time = prev_step_time + step_duration
            step = Movement(step_time, self._assigned_nurse, from_node, to_node)
            self.__steps.append(step)
            prev_step_time = step_time
            from_node = to_node

        #time there
        self.__steps.append(TimeAtPatient(prev_step_time + self.__duration, self._assigned_nurse, self.__duration))

        #getting back? Is it a separate plan? Is it gonna be sorted out in simulator?
    def __start__(self):
        self.__create_steps__()
        self._assigned_nurse.assign_event(self.__event_id)
        self.__status = EventStatus.ACTIVE

    def __pop_next_step__(self) -> Step:
        step: Step = self.__steps.pop(0)
        return step

    def __is_finished__(self) -> bool:
        if len(self.__steps) == 0:
            return True
        else:
             return False

    def get_patient(self) -> Patient:
        return self.__patient

    def get_status(self) -> EventStatus:
        return self.__status

    def get_duration(self) -> float:
        return self.__duration

    def set_time(self, time: float) -> None:
        self.__time = time

    def end_time(self) -> float:
        return self.__steps[-1].get_time()

    def next_time(self) -> float:
        if len(self.__steps) == 0:
            return self.get_time()
        else:
            return self.__steps[0].get_time()

    def get_next_step(self) -> Step:
        #assumes only future __steps are in this list
        return self.__steps[0]

    def run_next_step(self) -> bool:
        #runs next step, returns true if it finishes the event
        if self.__status == EventStatus.NOT_STARTED:
            self.__start__()
        else:
            step: Step = self.__pop_next_step__()
            step.run()

        if self.__is_finished__():
            self._assigned_nurse.finish_event()

        return self.__is_finished__()

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...
