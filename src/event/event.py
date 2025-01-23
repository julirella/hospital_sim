from abc import abstractmethod
from enum import IntEnum
from operator import truediv

from src import Graph
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
        for i in range(len(path_there)):
            step_time = prev_step_time #+ time it takes to get between the nodes
            self.steps.append(Movement(nurse=self.assigned_nurse, start=path_there[i], end=path_there[i+1]))
            prev_step_time = step_time

        #time there
        self.steps.append(TimeAtPatient(prev_step_time + self.duration, self.assigned_nurse, self.duration))

        #getting back? Is it a separate plan? Is it gonna be sorted out in simulator?
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
        step: Step = self.pop_next_step()
        step.run()
        return self.is_finished()

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...
