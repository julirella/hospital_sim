from src.event import Request
from src.queue import NurseList
from .request_assigner import RequestAssigner


class BasicAssigner(RequestAssigner):
    def init(self, nurse_queues: list[NurseList]):
        super().__init__(nurse_queues)

    def assign_request(self, request: Request) -> int | None:
        patient = request.patient
        patients_nurse = patient.nurse
        chosen_nurse = patients_nurse

        # put request in nurse queue
        chosen_nurse_id = chosen_nurse.nurse_id
        request.assign_nurse(chosen_nurse)
        nurse_queue = self.nurse_queues[chosen_nurse_id]

        request_level = request.get_level()
        if request_level == 1:
            nurse_queue.add_to_gap(request)
        elif request_level == 2:
            nurse_queue.add_after_current(request)
        elif request_level == 3:
            # add to start of nurse queue (and pause current if necessary)
            nurse_queue.add_to_start(request)

        return chosen_nurse_id
