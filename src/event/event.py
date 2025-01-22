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
        self.steps = []

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
    def pop_next_step(self) -> tuple[Step, bool]:
        step: Step = self.steps.pop(0)
        if len(self.steps) == 0:
            last_step = True
        else:
            last_step = False
        return step, last_step

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...
