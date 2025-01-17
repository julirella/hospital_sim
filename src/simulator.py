from nurse import Nurse
from src.graph import Graph
from src.patient import Patient
from src.queue.event_queue import EventQueue
from src.queue.nurse_queue import NurseQueue


class Simulator:
    def __init__(self, graph: Graph, nurses: list[Nurse], patients: list[Patient], request_queue: EventQueue, nurse_queues: list[NurseQueue]) -> None:
        self.graph = graph
        self.nurses = nurses
        self.patients = patients
        self.request_queue = request_queue
        self.nurse_queues = nurse_queues
        self.global_queue = EventQueue()

    def simulate(self) -> None:
        ...