from abc import abstractmethod
from enum import IntEnum
from operator import truediv

from src import Graph
from src.event import Step, Movement
from src.event.time_at_patient import TimeAtPatient
from src.event.timed_occurrence import TimedOccurrence
from src.nurse import Nurse
from src.patient import Patient

NURSE_SPEED = 4

class EventStatus(IntEnum):
    NOT_STARTED = 1
    ACTIVE = 2
    PAUSED = 3

class Event(TimedOccurrence):
    def __init__(self, event_id: int, time: float, duration: float, patient: Patient, assigned_nurse: Nurse | None, graph: Graph) -> None:
        super().__init__(time)
        self.event_id = event_id
        self.duration = duration
        self.patient = patient
        self.assigned_nurse = assigned_nurse
        self.graph = graph #is this dependency injection?
        self.status = EventStatus.NOT_STARTED
        self.steps: list[Step] = []

    def create_steps(self) -> None:
        #nurse has to be assigned at this point
        #each step needs to happen at the end of it, but also it has to be obvious that the event is in progress
        #so maybe some start event step??
        nurse_pos = self.assigned_nurse.get_pos()
        patient_pos = self.patient.room
        path_there = self.graph.find_path(nurse_pos, patient_pos)
        prev_step_time = self.time

        #getting there
        from_node = nurse_pos
        for i in range(len(path_there)):
            to_node, dst = path_there[i]
            step_duration = dst / NURSE_SPEED #TODO: sort out this conversion
            step_time = prev_step_time + step_duration
            step = Movement(step_time, self.assigned_nurse, from_node, to_node)
            self.steps.append(step)
            prev_step_time = step_time
            from_node = to_node

        #time there
        self.steps.append(TimeAtPatient(prev_step_time + self.duration, self.assigned_nurse, self.duration))

        #getting back? Is it a separate plan? Is it gonna be sorted out in simulator?
    def start(self):
        self.create_steps()
        self.assigned_nurse.assign_event(self.event_id)
        self.status = EventStatus.ACTIVE

    def pop_next_step(self) -> Step:
        step: Step = self.steps.pop(0)
        return step

    def is_finished(self) -> bool:
        if len(self.steps) == 0:
            return True
        else:
             return False

    def get_next_step(self) -> Step:
        #assumes only future steps are in this list
        return self.steps[0]

    def run_next_step(self) -> bool:
        #runs next step, returns true if it finishes the event
        if self.status == EventStatus.NOT_STARTED:
            self.start()
        step: Step = self.pop_next_step()
        step.run()

        if self.is_finished():
            self.assigned_nurse.finish_event()

        return self.is_finished()

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...
