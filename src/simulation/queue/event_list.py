from src.simulation.timed_object import Event
from typing import TypeVar, Generic


E = TypeVar("E", bound=Event)

class ListEvent:
    """
    wrapper around event for storage in linked list
    """
    def __init__(self, event: E, next_event):
        self.event = event
        self.next: ListEvent | None = next_event

class EventList(Generic[E]):
    """
    linked list of events sorted by time of occurrence
    """
    def __init__(self, events: list[E]):
        """
        :param events: regular list of events to be stored
        """

        #build linked list
        events.sort(key=lambda x: x.time)
        prev = None
        for event in reversed(events):
            prev = ListEvent(event, prev)
        self._front: ListEvent | None = prev

    def empty(self) -> bool:
        """
        :return: True if the list is empty, else False
        """
        return self._front is None

    def front(self) -> E | None:
        """
        access the front of the list
        :return: the front event or None if the list is empty
        """
        if self._front is None:
            return None
        else:
            return self._front.event

    def pop_front(self) -> E | None:
        """
        remove and return the front event of the list
        :return: the front event or None if the list is empty
        """
        event = self.front()
        if event is not None:
            self._front = self._front.next
        return event

    def next_time(self) -> float | None:
        """
        access the time of the front event
        :return: the time of the front event or None if the list is empty
        """
        if self.empty():
            return None
        return self.front().next_time()