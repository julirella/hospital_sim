from src.nurse import Nurse
from src.graph import Graph
from src.patient import Patient
from src.queue import StepQueue
from src.queue.event_queue import EventQueue
from src.queue.nurse_queue import NurseQueue


class Simulator:
    def __init__(self, graph: Graph, nurses: list[Nurse], patients: list[Patient], request_queue: EventQueue, nurse_queues: list[NurseQueue]) -> None:
        self.graph = graph
        self.nurses = nurses
        self.patients = patients
        self.request_queue = request_queue
        self.nurse_queues = nurse_queues
        self.global_queue = StepQueue()
        #put next step from each nurse queue into global queue
        for nurse_queue in self.nurse_queues:
            self.global_queue.add(nurse_queue.next_step())

    def simulate(self) -> None:
        #while any queue is not empty:
        #take next planned or waiting thing - request or step
        #if step, run it, replace it with that nurses next step
        #if request, decide which queue to put it in
        #log whatever happens
        ...