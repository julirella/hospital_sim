import csv

from src.event import Request
from src.event.timed_nurse_id import TimedNurseId
from src.nurse import Nurse
from src.graph import Graph
from src.patient import Patient
from src.queue import TimeQueue, EventList, NurseList
from src.sim_time import SimTime


class Simulator:
    def __init__(self, graph: Graph, nurses: list[Nurse], patients: list[Patient], request_queue: EventList,
                 nurse_queues: list[NurseList], sim_time: SimTime) -> None:
        self.graph = graph
        self.nurses = nurses
        self.patients = patients
        self.sim_time = sim_time
        self.request_queue = request_queue
        self.nurse_queues = nurse_queues
        self.global_queue = TimeQueue()

        #put next step from each nurse queue into global queue
        for nurse_id, nurse_queue in enumerate(self.nurse_queues):
            if not nurse_queue.empty():
                next_nurse_id = nurse_queue.create_timed_nurse_id()
                self.global_queue.add(next_nurse_id)

    def run_next_step(self):
        step_time = self.global_queue.next_time()
        self.sim_time.set_sim_time(step_time)
        next_step_nurse_id: TimedNurseId = self.global_queue.pop() #this should work anyway because python, but is it bad practice?
        nurse_queue = self.nurse_queues[next_step_nurse_id.nurse_id]
        nurse_queue.run_next_step()
        if not nurse_queue.empty():
            self.global_queue.add(nurse_queue.create_timed_nurse_id())

    def assign_next_request(self):
        self.sim_time.set_sim_time(self.request_queue.next_time())
        request: Request = self.request_queue.pop_front()
        #choose nurse
        patient = request.patient
        patients_nurse = patient.get_nurse()
        #TODO: add option for choosing other nurse if patients is unavailable/too far away based on request severity
        chosen_nurse = patients_nurse
        #put request in nurse queue
        chosen_nurse_id = chosen_nurse.nurse_id
        request.assign_nurse(chosen_nurse)
        nurse_queue = self.nurse_queues[chosen_nurse_id]

        request_level = request.get_level()
        if request_level == 1:
            nurse_queue.add_to_gap(request)
        elif request_level == 2:
            nurse_queue.add_after_current(request)
        elif request_level == 3:
            #add to start of nurse queue (and pause current if necessary)
            nurse_queue.add_to_start(request)
            #take next nurse step out of global queue
            self.global_queue.remove(nurse_queue.current_timed_nurse_id())
            #put new next nurse step into global queue
            self.global_queue.add(nurse_queue.create_timed_nurse_id())

    # def custom_print(*args, decimal_places=2):
    #     formatted_args = [
    #         f"{arg:.{decimal_places}f}" if isinstance(arg, float) else arg
    #         for arg in args
    #     ]
    #     print(*formatted_args)

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
        #TODO: add waiting requests
        while not self.request_queue.empty() or not self.global_queue.is_empty():
            if self.request_queue.empty():
                self.run_next_step()
            elif self.global_queue.is_empty():
                self.assign_next_request()
            elif self.global_queue.next_time() < self.request_queue.next_time():
                self.run_next_step()
            else:
                self.assign_next_request()

        self.__print_logs__()