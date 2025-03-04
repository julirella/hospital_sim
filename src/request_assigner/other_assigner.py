import numpy as np

from src import RequestAssigner, NurseList, Request


class OtherAssigner(RequestAssigner):
    def init(self, nurse_queues: list[NurseList]):
        super().__init__(nurse_queues)

    def assign_request(self, request: Request) -> int | None:
        patient = request.patient
        patients_nurse = patient.nurse
        patients_nurse_queue = self.nurse_queues[patients_nurse.nurse_id]

        request_level = request.level
        if request_level == 1:
            patients_nurse_queue.add_to_gap(request)
            return patients_nurse.nurse_id

        elif request_level == 2:
            if patients_nurse_queue.has_time_now(request):
                patients_nurse_queue.add_to_start(request)
                return patients_nurse.nurse_id
            else:
                for nurse_id, nurse_queue in enumerate(self.nurse_queues):
                    if nurse_queue.has_time_now(request):
                        nurse_queue.add_to_start(request)
                        return nurse_id
                return None

        elif request_level == 3:
            if patients_nurse_queue.has_time_now(request):
                patients_nurse_queue.add_to_start(request)
                return patients_nurse.nurse_id
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
                    return None #all nurses dealing with emergency
                else:
                    self.nurse_queues[min_nurse_id].add_to_start(request)
                    return min_nurse_id