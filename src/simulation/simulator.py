from sortedcontainers import SortedList

from src.simulation.timed_object import Request
from src.simulation.timed_object.timed_nurse_id import TimedNurseId
from src.simulation.people.nurse import Nurse
from src.simulation.graph import Graph
from src.simulation.people.patient import Patient
from src.simulation.queue import TimeQueue, EventList, NurseList
from src.simulation.request_assigner import RequestAssigner
from src.simulation.sim_time import SimTime


class Simulator:
    def __init__(self, graph: Graph, nurses: list[Nurse], patients: list[Patient], request_queue: EventList[Request],
                 nurse_queues: list[NurseList], sim_time: SimTime, request_assigner: RequestAssigner) -> None:
        self.graph = graph
        self.nurses = nurses
        self.patients = patients
        self.sim_time = sim_time
        self.request_assigner = request_assigner
        self.request_queue = request_queue
        self.nurse_queues = nurse_queues
        self.global_queue = TimeQueue[TimedNurseId]()
        self.waiting_requests = SortedList(key=lambda request: (request.level, request.time))

        #put next step from each nurse queue into global queue
        # for nurse_id, nurse_queue in enumerate(self.nurse_queues):
        #     if not nurse_queue.empty():
        #         next_nurse_id = nurse_queue.create_timed_nurse_id()
        #         self.global_queue.add(next_nurse_id)

        for nurse_id in range(len(self.nurses)):
            self.add_to_global_queue(nurse_id)

    def add_to_global_queue(self, nurse_id):
        nurse_queue = self.nurse_queues[nurse_id]
        if nurse_queue.in_global_queue: #for debugging
            raise RuntimeError(f"Nurse {nurse_id} already has event in global queue")
        if not nurse_queue.empty():
            next_nurse_id = nurse_queue.create_timed_nurse_id()
            self.global_queue.add(next_nurse_id)
            nurse_queue.in_global_queue = True

    def remove_from_global_queue(self, nurse_id):
        nurse_queue = self.nurse_queues[nurse_id]
        if nurse_queue.in_global_queue:
            self.global_queue.remove(nurse_queue.current_timed_nurse_id())
            nurse_queue.in_global_queue = False

    def pop_from_global_queue(self) -> int:
        nurse_id: int = self.global_queue.pop().nurse_id #this should work anyway because python, but is it bad practice?
        nurse_queue = self.nurse_queues[nurse_id]
        nurse_queue.in_global_queue = False
        return nurse_id

    def run_next_step(self):
        step_time = self.global_queue.next_time()
        self.sim_time.sim_time = step_time
        # next_step_nurse_id: int = self.global_queue.pop().nurse_id #this should work anyway because python, but is it bad practice?
        next_step_nurse_id = self.pop_from_global_queue()
        nurse_queue = self.nurse_queues[next_step_nurse_id]
        finished = nurse_queue.run_next_step()
        if finished and len(self.waiting_requests) > 0: #assuming request will definitely be assigned
            success = self.assign_request(self.waiting_requests.pop(0))
            if not success:
                self.add_to_global_queue(next_step_nurse_id)
        # elif not nurse_queue.empty():
        #     self.global_queue.add(nurse_queue.create_timed_nurse_id())
        else:
            self.add_to_global_queue(next_step_nurse_id)

    def assign_request(self, request: Request) -> bool:
        #choose nurse
        chosen_nurse_id = self.request_assigner.assign_request(request)

        if chosen_nurse_id is not None:
            # nurse_queue = self.nurse_queues[chosen_nurse_id]
            #take next nurse step out of global queue
            # if not nurse_queue.empty():
            #     self.global_queue.remove(nurse_queue.current_timed_nurse_id())
            self.remove_from_global_queue(chosen_nurse_id)
            #put new next nurse step into global queue
            # self.global_queue.add(nurse_queue.create_timed_nurse_id())
            self.add_to_global_queue(chosen_nurse_id)
            return True
        else:
            #put in waiting requests
            self.waiting_requests.add(request)
            return False

    def assign_next_request(self):
        self.sim_time.sim_time = self.request_queue.next_time()
        request: Request = self.request_queue.pop_front()
        self.assign_request(request)

    def __print_logs__(self):
        print("------------------nurse logs--------------------")
        for nurse_id, nurse in enumerate(self.nurses):
            print("nurse", nurse_id)
            log = nurse.log
            for line in log:
                print(line)
                # self.custom_print(line)

            # print(nurse.log)
        print("\n")
        print("------------------event logs--------------------")
        logs = []
        for nurse_queue in self.nurse_queues:
            logs += nurse_queue.event_logs

        for log in logs:
            print(log)

    def nurse_log(self) -> list[dict]:
        nurse_logs = []
        for nurse in self.nurses:
            nurse_logs += nurse.log

        return nurse_logs

    def event_log(self) -> list[dict]:
        event_logs = []
        for nurse_queue in self.nurse_queues:
            event_logs += nurse_queue.event_logs

        return event_logs

    def simulate(self) -> None:
        #while any queue is not empty:
        #take next planned or waiting thing - request or step
        #if step, run it, replace it with that nurses next step
        #if request, decide which queue to put it in
        #log whatever happens
        print("Simulating...")
        while not self.request_queue.empty() or not self.global_queue.empty():
            if self.request_queue.empty():
                self.run_next_step()
            elif self.global_queue.empty():
                self.assign_next_request()
            elif self.global_queue.next_time() < self.request_queue.next_time():
                self.run_next_step()
            else:
                self.assign_next_request()

        # self.__print_logs__()