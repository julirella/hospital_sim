from src import SimTime
from src.event import Event

MAX_WALK_TIME = 20 #TODO: recalculate based on dept size

class ListEvent:
    def __init__(self, event: Event, next_event):
        self.event = event
        self.next: ListEvent | None = next_event

#linkded list of nurse events
class NurseList:
    def __init__(self, events: list[Event], sim_time: SimTime):
        #build linked list
        events.sort(key=lambda x: x.get_time())
        prev = None
        for event in reversed(events):
            prev = ListEvent(event, prev)
        self.__front: ListEvent | None = prev

        self.__sim_time: SimTime = sim_time

    def __max_event_duration__(self, event: Event) -> float:
        return event.get_duration() + MAX_WALK_TIME  # TODO switch to smarter walk time

    def __insert_after(self, new_event: Event, pred_event: ListEvent=None) -> None:
        #insert new_event after pred_event. If pred_event is None, add to front of list
        if pred_event is None:
            new_front = ListEvent(new_event, self.__front)
            self.__front = new_front
            new_event.set_time(self.__sim_time.get_sim_time())
        else:
            new_list_event = ListEvent(new_event, pred_event.next)
            pred_event.next = new_list_event
            new_event.set_time(pred_event.event.get_time() + MAX_WALK_TIME / 2 + new_event.get_duration())

    def empty(self) -> bool:
        return self.__front is None

    def top(self) -> Event:
        return self.__front.event

    def pop(self) -> Event:
        event = self.top()
        self.__front = self.__front.next
        return event

    def add_to_gap(self, event: Event):
        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self.__sim_time.get_sim_time()

        prev = None
        current: ListEvent = self.__front
        done = False
        while current is not None:
            next_start_time = current.event.start_time()
            if next_start_time - prev_end_time > max_event_duration: #new event fits
                self.__insert_after(event, prev)
                done = True
                break
            prev_end_time = current.event.get_time()
            prev = current
            current = current.next

        if not done:
            self.__insert_after(event, prev)
