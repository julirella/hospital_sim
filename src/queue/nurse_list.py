from src import SimTime, Nurse
from src.event import Event, EventStatus, TimedNurseId
from src.queue.event_list import EventList, ListEvent

#linkded list of nurse events
class NurseList(EventList):
    def __init__(self, events: list[Event], sim_time: SimTime, nurse: Nurse, max_graph_dst: float):
        super().__init__(events)
        self._sim_time: SimTime = sim_time
        self._nurse_id = nurse.get_id()
        self._max_walk_time = max_graph_dst / nurse.speed #longest walk time for nurse between any two nodes in graph
        self._timed_nurse_id: TimedNurseId

    def __max_event_duration__(self, event: Event) -> float:
        return event.get_duration() + self._max_walk_time

    def __insert_after__(self, new_event: Event, pred_event: ListEvent=None) -> None:
        #insert new_event after pred_event. If pred_event is None, add to front of list
        new_list_event: ListEvent

        if pred_event is None:
            new_list_event = ListEvent(new_event, self._front)
            self._front = new_list_event
            new_event.set_time(self._sim_time.get_sim_time())
        else:
            new_list_event = ListEvent(new_event, pred_event.next)
            pred_event.next = new_list_event
            new_event.set_time(pred_event.event.time() + pred_event.event.get_duration() + self._max_walk_time)

        #push_back if necessary, could probably be a separate method
        #at this point we know new event is far enough from the event before it, but the following event may be too close
        current = new_list_event
        while current.next is not None and current.event.time() + current.event.get_duration() + self._max_walk_time > current.next.event.time():
            current.next.event.set_time(current.event.time() + current.event.get_duration() + self._max_walk_time)
            current = current.next

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self._sim_time.get_sim_time()

        prev_event = None
        next_event: ListEvent = self._front
        done = False
        while next_event is not None:
            next_start_time = next_event.event.time()
            if next_start_time - prev_end_time > max_event_duration: #new event fits
                self.__insert_after__(event, prev_event)
                done = True
                break
            prev_end_time = next_event.event.time() + next_event.event.get_duration() + self._max_walk_time
            prev_event = next_event
            next_event = next_event.next

        if not done:
            self.__insert_after__(event, prev_event)

    #add event after end of current running event
    def add_after_current(self, event: Event) -> None:
        current_event: Event = self.front()
        # max_event_duration = self.__max_event_duration__(event)
        if current_event.get_status() == EventStatus.NOT_STARTED:
            #it just goes straight away
            self.__insert_after__(event)
        else:
            self.__insert_after__(event, self._front)

    def add_to_start(self, event: Event) -> None:
        current_event: Event = self.front()
        if current_event.get_status() == EventStatus.ACTIVE:
            current_event.pause() #pause current if necessary

        #insert new and push back rest
        self.__insert_after__(event, None)

    def run_next_step(self) -> None:
        #call run next step of top event
        next_event: Event = self.front()
        finished: bool = next_event.run_next_step()
        #if the event is over, remove it (and maybe log that)
        if finished:
            self.pop_front()

    def create_timed_nurse_id(self) -> TimedNurseId:
        self._timed_nurse_id = TimedNurseId(self.next_time(), self._nurse_id)
        return self._timed_nurse_id

    def get_timed_nurse_id(self) -> TimedNurseId:
        return self._timed_nurse_id