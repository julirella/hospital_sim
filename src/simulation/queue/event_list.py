from src.simulation.timed_object import Event
from typing import TypeVar, Generic


E = TypeVar("E", bound=Event)

class ListEvent:
    def __init__(self, event: E, next_event):
        self.event = event
        self.next: ListEvent | None = next_event

#linked list of events
class EventList(Generic[E]):
    def __init__(self, events: list[E]):
        #build linked list
        events.sort(key=lambda x: x.time)
        prev = None
        for event in reversed(events):
            prev = ListEvent(event, prev)
        self._front: ListEvent | None = prev

    def empty(self) -> bool:
        return self._front is None

    def front(self) -> E | None:
        if self._front is None:
            return None
        else:
            return self._front.event

    def pop_front(self) -> E | None:
        event = self.front()
        if event is not None:
            self._front = self._front.next
        return event

    def next_time(self) -> float | None:
        if self.empty():
            return None
        return self.front().next_time()