from sortedcontainers import SortedDict

from src.event import TimedOccurrence


class TimeQueue:
    #TODO: maybe create another queue higher up that will work with any item and then this one will work with just TimedOccurrence, rather than combining it into one
    #priority queue for storing anything with time as a key
    def __init__(self):
        self.queue = SortedDict()

    def add_by_time(self, time: float, item) -> None:
        self.queue[time] = item

    def add(self, item: TimedOccurrence):
        self.queue[item.time] = item

    def pop(self): #-> TimedOccurrence:
    #remove and return first element
        return self.queue.popitem(0)[1]

    def top_item(self):
        return self.queue.peekitem(0)[1]

    def next_time(self) -> float:
        return self.queue.peekitem(0)[0]

    def is_empty(self):
        return len(self.queue) == 0

    def remove(self, item: TimedOccurrence):
        self.queue.pop(item.time)