from sortedcontainers import SortedDict

from src.event import TimedOccurrence


class TimeQueue:
    #priority queue for storing anything with time as a key
    def __init__(self):
        self.queue = SortedDict()


    def add(self, item: TimedOccurrence):
        self.queue[item.time] = item

    def pop(self) -> TimedOccurrence:
    #remove and return first element
        return self.queue.popitem(0)[1]

    def is_empty(self):
        return len(self.queue) == 0

    def remove(self, item: TimedOccurrence):
        self.queue.pop(item.time)