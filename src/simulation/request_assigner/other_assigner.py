import numpy as np

from src.simulation.timed_object import Request
from src.simulation.queue import NurseList
from .request_assigner import RequestAssigner


class OtherAssigner(RequestAssigner):
    """
    other way of assigning requests to nurse (what a creative name right)
    """
    def init(self, nurse_queues: list[NurseList]):
        super().__init__(nurse_queues)

    def assign_request(self, request: Request) -> int | None:
        """
        attempt to assign request to a nurse based on the other method, add to their queue on success
        :param request: the request to assign
        :return: ID of chosen nurse on success, None otherwise
        """
        patient = request.patient
        patients_nurse = patient.nurse
        patients_nurse_queue = self.nurse_queues[patients_nurse.nurse_id]

        chosen_nurse_id = None

        request_level = request.level
        if request_level == 1:
            patients_nurse_queue.add_to_gap(request)
            chosen_nurse_id = patients_nurse.nurse_id

        elif request_level == 2:
            if patients_nurse_queue.has_time_now(request):
                patients_nurse_queue.add_to_start(request)
                chosen_nurse_id = patients_nurse.nurse_id
            else:
                for nurse_id, nurse_queue in enumerate(self.nurse_queues):
                    if nurse_queue.has_time_now(request):
                        nurse_queue.add_to_start(request)
                        chosen_nurse_id = nurse_id
                        break
                # return None

        elif request_level == 3:
            if patients_nurse_queue.has_time_now(request):
                patients_nurse_queue.add_to_start(request)
                chosen_nurse_id = patients_nurse.nurse_id
            else:
                active_event_levels = []
                for nurse_id, nurse_queue in enumerate(self.nurse_queues):
                    if nurse_queue.has_time_now(request):
                        active_event_levels.append(-1)
                    else:
                        active_event_levels.append(nurse_queue.current_event_level())

                min_level = min(active_event_levels)
                min_nurse_id = int(np.argmin(active_event_levels))
                if min_level == 3:
                    chosen_nurse_id = None #all nurses dealing with emergency
                elif active_event_levels[patients_nurse.nurse_id] == min_level:
                    # if patient's nurse is among those with lowest request level, choose them
                    self.nurse_queues[patients_nurse.nurse_id].add_to_start(request)
                    chosen_nurse_id = patients_nurse.nurse_id
                else:
                    self.nurse_queues[min_nurse_id].add_to_start(request)
                    chosen_nurse_id = min_nurse_id

        if chosen_nurse_id is not None:
            nurse = self.nurse_queues[chosen_nurse_id].nurse
            request.assign_nurse(nurse)

        return chosen_nurse_id