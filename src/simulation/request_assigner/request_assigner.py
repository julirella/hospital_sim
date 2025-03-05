from abc import abstractmethod

from src.simulation.event import Request
from src.simulation.queue import NurseList


class RequestAssigner:
    def __init__(self, nurse_queues: list[NurseList]):
        self.nurse_queues = nurse_queues

    @abstractmethod
    def assign_request(self, request: Request):
        pass