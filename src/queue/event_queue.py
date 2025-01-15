from sortedcontainers import SortedDict
from src.event import Event

class EventQueue:
    #for now the key is only time. Maybe switch to (time, event_id) to eliminate time collisions
    def __init__(self):
        self.queue = SortedDict()

    def add(self, event: Event):
        self.queue[event.time] = event

    def pop(self) -> Event:
    #remove and return first element
        return self.queue.popitem(0)[1]

    def is_empty(self):
        return len(self.queue) == 0

    def remove(self, event: Event):
        pass