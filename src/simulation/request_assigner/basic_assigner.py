from src.simulation.timed_object import Request
from src.simulation.queue import NurseList
from .request_assigner import RequestAssigner


class BasicAssigner(RequestAssigner):
    """
    basic way of assigning requests to nurse
    """
    def init(self, nurse_queues: list[NurseList]):
        """
        :param nurse_queues: list of all nurse queues (ordered by nurse ID)
        """
        super().__init__(nurse_queues)

    def assign_request(self, request: Request) -> int | None:
        """
        attempt to assign request to a nurse based on the basic method, add to their queue on success
        :param request: the request to assign
        :return: ID of chosen nurse on success, None otherwise
        """
        patient = request.patient
        patients_nurse = patient.nurse
        chosen_nurse = patients_nurse

        # put request in nurse queue
        chosen_nurse_id = chosen_nurse.nurse_id
        request.assign_nurse(chosen_nurse)
        nurse_queue = self.nurse_queues[chosen_nurse_id]

        request_level = request.level
        if request_level == 1:
            nurse_queue.add_to_gap(request)
        elif request_level == 2:
            nurse_queue.add_after_current(request)
        elif request_level == 3:
            # add to start of nurse queue (and pause current if necessary)
            nurse_queue.add_to_start(request)

        return chosen_nurse_id
