from enum import IntEnum

from src import Graph, SimTime
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
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, assigned_nurse: Nurse | None,
                 graph: Graph, sim_time: SimTime) -> None:
        super().__init__(time)
        self.__event_id = event_id
        self.__duration = duration
        self.__patient = patient
        self._assigned_nurse = assigned_nurse
        self.__graph = graph
        self.__sim_time = sim_time
        self.__status = EventStatus.NOT_STARTED
        self.__steps: list[Step] = []

    def __create_steps__(self) -> None:
        #nurse has to be assigned at this point
        #each step needs to happen at the end of it, but also it has to be obvious that the event is in progress
        #so maybe some start event step??
        nurse_pos = self._assigned_nurse.get_pos()
        patient_pos = self.__patient.get_room()
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
        self._time = time

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
        if self.__status == EventStatus.NOT_STARTED or self.__status == EventStatus.PAUSED:
            self.__start__() #at this point start and resume is the same
        else:
            step: Step = self.__pop_next_step__()
            step.run()

        if self.__is_finished__():
            self._assigned_nurse.finish_event()

        return self.__is_finished__()

    def pause(self) -> None:
        self.__status = EventStatus.PAUSED
        self._assigned_nurse.unassign_event()
        self._time = self.__sim_time.get_sim_time() #so that it can be pushed back correctly. Not amazing relying on this
        next_step = self.get_next_step()
        #if the next step was movement, sort out nurse position
        if type(next_step) == Movement: #is this too ugly?
            #TODO
            #calculate nurse position based on time remaining to get to next node
            #create a phantom node for them to be on, somehow sort out how to move them from there
            ...
        #if it's caring for patient, sort out duration
        elif type(next_step) == TimeAtPatient:
            self.__duration = next_step.get_time() - self.__sim_time.get_sim_time()

    def resume(self) -> None:
        ...
