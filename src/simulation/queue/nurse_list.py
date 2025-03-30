from src import SimTime, Nurse, Graph
from src.simulation.timed_object import EventStatus, TimedNurseId, ReturnToOffice, Event
from src.simulation.queue.event_list import EventList, ListEvent

#linkded list of nurse events
class NurseList(EventList[Event]):
    def __init__(self, events: list[Event], sim_time: SimTime, nurse: Nurse, max_graph_dst: float, graph: Graph):
        super().__init__(events)
        self._sim_time: SimTime = sim_time
        self._graph = graph
        self._nurse: Nurse = nurse
        self._nurse_id = nurse.nurse_id
        self._max_walk_time = max_graph_dst / nurse.speed #longest walk time for nurse between any two nodes in graph
        self._timed_nurse_id: TimedNurseId
        self._event_logs = []
        self._in_global_queue: bool = False

    @property
    def event_logs(self):
        return self._event_logs

    @property
    def in_global_queue(self) -> bool:
        return self._in_global_queue

    @property
    def nurse(self) -> Nurse:
        return self._nurse

    @in_global_queue.setter
    def in_global_queue(self, value: bool):
        self._in_global_queue = value

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

    def __replace_return_to_office__(self, event: Event):
        #stops current return to office event, removes it, logs it and adds event to start
        self._front.event.pause()
        finished_log = self.pop_front().log
        self._event_logs += finished_log
        self.__insert_after__(event)

    def has_time_now(self, event: Event) -> bool:
        return self.empty() or self.__max_event_duration__(event) <= self._front.event.time - self._sim_time.sim_time

    def current_event_level(self) -> int:
        if self.empty():
            return -1

        current_event = self._front.event
        if current_event.status == EventStatus.ACTIVE and current_event.type == 'request':
            return current_event.level #TODO: maybe just get level from event too?
        else:
            return -1

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        if self.empty():
            self.__insert_after__(event)
            return

        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self._sim_time.sim_time

        prev_event = None
        next_event: ListEvent = self._front
        done = False

        if next_event.event.type == 'return_to_office' and next_event.next.event.time - prev_end_time > max_event_duration:
            #there is enough time before the next non return to office event, but there is a return to office in the way
            # TODO: this path is not tested
            done = True
            self.__replace_return_to_office__(event)
            # self.add_to_gap(event)
        else:
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
        if self.empty():
            self.__insert_after__(event)
            return

        current_event: Event = self.front()
        # max_event_duration = self.__max_event_duration__(event)
        if current_event.status == EventStatus.NOT_STARTED:
            #it just goes straight away
            self.__insert_after__(event)
        elif current_event.type == 'return_to_office':
            # current_event.pause()
            # finished_log = self.pop_front().log
            # self._event_logs += finished_log
            # self.__insert_after__(event)
            self.__replace_return_to_office__(event)
        else:
            self.__insert_after__(event, self._front)

    def add_to_start(self, event: Event) -> None:
        if self.empty():
            self.__insert_after__(event)
            return

        current_event: Event = self.front()
        if current_event.status == EventStatus.ACTIVE:
            current_event.pause() #pause current if necessary
            if current_event.type == 'return_to_office':
                finished_log = self.pop_front().log
                self._event_logs += finished_log

        #insert new and push back rest
        self.__insert_after__(event, None)


    def run_next_step(self) -> bool:
        #returns true if step run was last step of event (aka event was finished)
        if self.empty():
            raise Exception("can't run next step of emtpy list")

        #call run next step of top event
        next_event: Event = self.front()
        finished: bool = next_event.run_next_step()
        #if the event is over, remove it (and maybe log that)
        if finished: # don't return again if already returned to office
            finished_log = self.pop_front().log
            self._event_logs += finished_log
            if (self.empty() or self.next_time() - self._sim_time.sim_time >= self._max_walk_time * 2) and self._nurse.pos != self._graph.nurse_office:
                #create return to office event
                return_event = ReturnToOffice(self._nurse, self._graph, self._sim_time)
                self.__insert_after__(return_event)

        return finished

    def create_timed_nurse_id(self) -> TimedNurseId:
        self._timed_nurse_id = TimedNurseId(self.next_time(), self._nurse_id)
        return self._timed_nurse_id

    def current_timed_nurse_id(self) -> TimedNurseId:
        return self._timed_nurse_id