from abc import abstractmethod

from src.simulation.timed_object import Request
from src.simulation.queue import NurseList


class RequestAssigner:
    """
    abstract class for assigning requests
    """
    def __init__(self, nurse_queues: list[NurseList]):
        """
        :param nurse_queues: list of all nurse queues (ordered by nurse ID)
        """
        self.nurse_queues = nurse_queues

    @abstractmethod
    def assign_request(self, request: Request) -> int | None:
        """
        attempt to assign request to a nurse, add to their queue on success
        :param request: the request to assign
        :return: ID of chosen nurse on success, None otherwise
        """
        pass