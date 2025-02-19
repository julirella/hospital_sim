from src.event import PatientEvent

class ListEvent:
    def __init__(self, event: PatientEvent, next_event):
        self.event = event
        self.next: ListEvent | None = next_event

#linked list of events
class EventList:
    def __init__(self, events: list[PatientEvent]):
        #build linked list
        events.sort(key=lambda x: x.time)
        prev = None
        for event in reversed(events):
            prev = ListEvent(event, prev)
        self._front: ListEvent | None = prev

    def empty(self) -> bool:
        return self._front is None

    def front(self) -> PatientEvent:
        return self._front.event

    def pop_front(self) -> PatientEvent:
        event = self.front()
        self._front = self._front.next
        return event

    def next_time(self) -> float:
        return self.front().next_time()