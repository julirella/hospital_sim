from src import SimTime
from src.event import Event, EventStatus
from src.queue.event_list import EventList, ListEvent

MAX_WALK_TIME = 20 #TODO: recalculate based on dept size

#linkded list of nurse events
class NurseList(EventList):
    def __init__(self, events: list[Event], sim_time: SimTime):
        super().__init__(events)
        self._sim_time: SimTime = sim_time

    def __max_event_duration__(self, event: Event) -> float:
        return event.get_duration() + MAX_WALK_TIME  # TODO switch to smarter walk time

    def __insert_after__(self, new_event: Event, pred_event: ListEvent=None) -> None:
        #insert new_event after pred_event. If pred_event is None, add to front of list
        new_list_event: ListEvent

        if pred_event is None:
            new_list_event = ListEvent(new_event, self._front)
            self._front = new_list_event
            new_event.set_time(self._sim_time.get_sim_time() + MAX_WALK_TIME / 2 + new_event.get_duration())
        else:
            new_list_event = ListEvent(new_event, pred_event.next)
            pred_event.next = new_list_event
            new_event.set_time(pred_event.event.get_time() + MAX_WALK_TIME / 2 + new_event.get_duration())

        #push_back if necessary, could probably be a separate method
        current = new_list_event
        while current.next is not None and current.event.get_time() + MAX_WALK_TIME / 2 > current.next.event.start_time():
            current.next.event.set_time(current.event.get_time() + MAX_WALK_TIME / 2 + current.next.event.get_duration())
            current = current.next

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self._sim_time.get_sim_time()

        prev = None
        current: ListEvent = self._front
        done = False
        while current is not None:
            next_start_time = current.event.start_time()
            if next_start_time - prev_end_time > max_event_duration: #new event fits
                self.__insert_after__(event, prev)
                done = True
                break
            prev_end_time = current.event.get_time()
            prev = current
            current = current.next

        if not done:
            self.__insert_after__(event, prev)

    #add event after end of current running event
    def add_after_current(self, event: Event) -> None:
        current_event: Event = self.front()
        # max_event_duration = self.__max_event_duration__(event)
        if current_event.get_status() == EventStatus.NOT_STARTED:
            #it just goes straight away
            self.__insert_after__(event)
        else:
            self.__insert_after__(event, self._front)
