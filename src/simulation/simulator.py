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
    """
    Class for running the simulation
    """
    def __init__(self, graph: Graph, nurses: list[Nurse], patients: list[Patient], request_queue: EventList[Request],
                 nurse_queues: list[NurseList], sim_time: SimTime, request_assigner: RequestAssigner) -> None:
        """
        :param graph: department graph
        :param nurses: list of nurses
        :param patients: list of patients
        :param request_queue: request queue
        :param nurse_queues: list of nurse queues
        :param sim_time: SimTime object to track simulation time
        :param request_assigner: chosen request assigner
        """
        self.graph = graph
        self.nurses = nurses
        self.patients = patients
        self.sim_time = sim_time
        self.request_assigner = request_assigner

        # prepare queues
        self.request_queue = request_queue
        self.nurse_queues = nurse_queues
        self.global_queue = TimeQueue[TimedNurseId]()
        self.waiting_requests = SortedList(key=lambda request: (request.level, request.time))

        # put next step from each nurse queue into global queue
        for nurse_id in range(len(self.nurses)):
            self.__add_to_global_queue__(nurse_id)

    def __add_to_global_queue__(self, nurse_id):
        # add timed_nurse_id of nurse to global queue if nurse has any event coming up
        nurse_queue = self.nurse_queues[nurse_id]
        if nurse_queue.in_global_queue: #for debugging
            raise RuntimeError(f"Nurse {nurse_id} already has event in global queue")
        if not nurse_queue.empty():
            next_nurse_id = nurse_queue.create_timed_nurse_id()
            self.global_queue.add(next_nurse_id)
            nurse_queue.in_global_queue = True

    def __remove_from_global_queue__(self, nurse_id):
        # if nurse has timed_nurse_id in global queue, remove it
        nurse_queue = self.nurse_queues[nurse_id]
        if nurse_queue.in_global_queue:
            self.global_queue.remove(nurse_queue.current_timed_nurse_id())
            nurse_queue.in_global_queue = False

    def __pop_from_global_queue__(self) -> int:
        # pop top nurse id from global queue
        nurse_id: int = self.global_queue.pop().nurse_id
        nurse_queue = self.nurse_queues[nurse_id]
        nurse_queue.in_global_queue = False
        return nurse_id

    def __run_next_step__(self):
        # take top step from global queue and run it, update sim time to step time
        step_time = self.global_queue.next_time()
        self.sim_time.sim_time = step_time

        # get nurse id from global queue and find the corresponding nurse queue
        next_step_nurse_id = self.__pop_from_global_queue__()
        nurse_queue = self.nurse_queues[next_step_nurse_id]

        # run the step, put the nurse's next step in global queue
        finished = nurse_queue.run_next_step()
        if finished and len(self.waiting_requests) > 0:
            # if the event is finished, try to reassign the top waiting request
            success = self.__assign_request__(self.waiting_requests.pop(0))
            if not success:
                self.__add_to_global_queue__(next_step_nurse_id)
        else:
            self.__add_to_global_queue__(next_step_nurse_id)

    def __assign_request__(self, request: Request) -> bool:
        # attempt to assign request to nurse

        #choose nurse
        chosen_nurse_id = self.request_assigner.assign_request(request)

        if chosen_nurse_id is not None:
            #take next nurse step out of global queue
            self.__remove_from_global_queue__(chosen_nurse_id)
            #put new next nurse step into global queue
            self.__add_to_global_queue__(chosen_nurse_id)
            return True
        else:
            #put in waiting requests
            self.waiting_requests.add(request)
            return False

    def __assign_next_request__(self):
        # take top request from waiting requests and attempt to assign it, update sim time to request time
        self.sim_time.sim_time = self.request_queue.next_time()
        request: Request = self.request_queue.pop_front()
        self.__assign_request__(request)

    def nurse_log(self) -> list[dict]:
        """
        Collects all nurse logs and merges them into a list of dicts
        :return: list of dicts, each dict is a nurse action
        """
        nurse_logs = []
        for nurse in self.nurses:
            nurse_logs += nurse.log

        return nurse_logs

    def event_log(self) -> list[dict]:
        """
        Collects all event logs and merges them into a list of dicts
        :return: list of dicts, each dict is an event action
        """
        event_logs = []
        for nurse_queue in self.nurse_queues:
            event_logs += nurse_queue.event_logs

        return event_logs

    def simulate(self) -> None:
        """
        Run the simulation
        """
        #while any queue is not empty:
        #take next planned or waiting thing - request or step
        #if step, run it, replace it with that nurses next step
        #if request, decide which queue to put it in
        #log whatever happens
        print("Simulating...")
        while not self.request_queue.empty() or not self.global_queue.empty():
            if self.request_queue.empty():
                self.__run_next_step__()
            elif self.global_queue.empty():
                self.__assign_next_request__()
            elif self.global_queue.next_time() < self.request_queue.next_time():
                self.__run_next_step__()
            else:
                self.__assign_next_request__()
