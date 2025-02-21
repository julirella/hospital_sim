from abc import abstractmethod

from src.event import Request
from src.queue import NurseList


class RequestAssigner:
    def __init__(self, nurse_queues: list[NurseList]):
        self.nurse_queues = nurse_queues

    @abstractmethod
    def assign_request(self, request: Request):
        pass