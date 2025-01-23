from sortedcontainers import SortedDict

from src.event import Step
from src.nurse import Nurse
from src.graph import Graph
from src.patient import Patient
from src.queue import StepQueue, TimeQueue
from src.queue.event_queue import EventQueue
from src.queue.nurse_queue import NurseQueue


class Simulator:
    def __init__(self, graph: Graph, nurses: list[Nurse], patients: list[Patient], request_queue: EventQueue, nurse_queues: list[NurseQueue]) -> None:
        self.graph = graph
        self.nurses = nurses
        self.patients = patients
        self.request_queue = request_queue
        self.nurse_queues = nurse_queues
        self.global_queue = TimeQueue()
        # self.global_queue = SortedDict() #maybe wrap this in some queue
        #put next step from each nurse queue into global queue
        for nurse_id, nurse_queue in enumerate(self.nurse_queues):
            self.global_queue.add_by_time(nurse_queue.next_time(), nurse_id)

    def run_next_step(self):
        next_step_nurse_id: int = self.global_queue.pop() #this should work anyway because python, but is it bad practice?
        self.nurse_queues[next_step_nurse_id].run_next_step()
        self.global_queue.add_by_time(self.nurse_queues[next_step_nurse_id].next_time(), next_step_nurse_id)

    def simulate(self) -> None:
        #while any queue is not empty:
        #take next planned or waiting thing - request or step
        #if step, run it, replace it with that nurses next step
        #if request, decide which queue to put it in
        #log whatever happens

        #TODO: add waiting requests
        while not self.request_queue.is_empty() or not self.request_queue.is_empty():
            if self.request_queue.is_empty():
                #run step
                ...
            elif not self.request_queue.is_empty():
                #assign request
                ...
            elif self.request_queue.next_time() <= self.global_queue.next_time():
                #run step
                ...
            else:
                #assign request
                ...