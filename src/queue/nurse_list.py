from src import SimTime, Nurse, Graph
from src.event import PatientEvent, EventStatus, TimedNurseId, Request, ReturnToOffice, Event
from src.queue.event_list import EventList, ListEvent

#linkded list of nurse events
class NurseList(EventList):
    def __init__(self, events: list[PatientEvent], sim_time: SimTime, nurse: Nurse, max_graph_dst: float, graph: Graph):
        super().__init__(events)
        self._sim_time: SimTime = sim_time
        self._graph = graph
        self._nurse: Nurse = nurse
        self._nurse_id = nurse.nurse_id
        self._max_walk_time = max_graph_dst / nurse.speed #longest walk time for nurse between any two nodes in graph
        self._timed_nurse_id: TimedNurseId
        self._event_logs = []

    @property
    def event_logs(self):
        return self._event_logs

    def __max_event_duration__(self, event: Event) -> float:
        return event.duration + self._max_walk_time

    def __insert_after__(self, new_event: Event, pred_event: ListEvent=None) -> None:
        #insert new_event after pred_event. If pred_event is None, add to front of list
        new_list_event: ListEvent

        if pred_event is None:
            new_list_event = ListEvent(new_event, self._front)
            self._front = new_list_event
            new_event.time = self._sim_time.sim_time
        else:
            new_list_event = ListEvent(new_event, pred_event.next)
            pred_event.next = new_list_event
            new_event.time = pred_event.event.time + pred_event.event.duration + self._max_walk_time

        #push_back if necessary, could probably be a separate method
        #at this point we know new event is far enough from the event before it, but the following event may be too close
        current = new_list_event
        while current.next is not None and current.event.time + current.event.duration + self._max_walk_time > current.next.event.time:
            current.next.event.time = current.event.time + current.event.duration + self._max_walk_time
            current = current.next

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self._sim_time.sim_time

        prev_event = None
        next_event: ListEvent = self._front
        done = False
        while next_event is not None:
            next_start_time = next_event.event.time
            if next_start_time - prev_end_time > max_event_duration: #new event fits
                self.__insert_after__(event, prev_event)
                done = True
                break
            prev_end_time = next_event.event.time + next_event.event.duration + self._max_walk_time
            prev_event = next_event
            next_event = next_event.next

        if not done:
            self.__insert_after__(event, prev_event)

    #add event after end of current running event
    def add_after_current(self, event: Event) -> None:
        current_event: Event = self.front()
        # max_event_duration = self.__max_event_duration__(event)
        if current_event.status == EventStatus.NOT_STARTED:
            #it just goes straight away
            self.__insert_after__(event)
        else:
            self.__insert_after__(event, self._front)

    def add_to_start(self, event: Event) -> None:
        current_event: Event = self.front()
        if current_event.status == EventStatus.ACTIVE:
            current_event.pause() #pause current if necessary

        #insert new and push back rest
        self.__insert_after__(event, None)


    def add_request(self, request: Request) -> bool:
        top_event_changed = False

        #TODO what if list is empty
        if self.front().type == 'return_to_office':
            #return to office should be paused and removed
            self.pop_front().pause()
            top_event_changed = True

        request_level = request.get_level()
        if request_level == 1:
            self.add_to_gap(request)
        elif request_level == 2:
            self.add_after_current(request)
        elif request_level == 3:
            # add to start of nurse queue (and pause current if necessary)
            self.add_to_start(request)
            top_event_changed = True

        return top_event_changed

    def run_next_step(self) -> None:
        #call run next step of top event
        next_event: Event = self.front()
        finished: bool = next_event.run_next_step()
        #if the event is over, remove it (and maybe log that)
        if finished: # don't return again if already returned to office
            finished_log = self.pop_front().log
            self._event_logs += finished_log
            # if (self.empty() or self.next_time() - self._sim_time.sim_time > self._max_walk_time * 2) and self._nurse.pos != self._graph.nurse_office:
            #     #create return to office event
            #     return_event = ReturnToOffice(self._nurse, self._graph, self._sim_time)
            #     self.__insert_after__(return_event)

    def create_timed_nurse_id(self) -> TimedNurseId:
        self._timed_nurse_id = TimedNurseId(self.next_time(), self._nurse_id)
        return self._timed_nurse_id

    def current_timed_nurse_id(self) -> TimedNurseId:
        return self._timed_nurse_id