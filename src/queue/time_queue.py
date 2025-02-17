from sortedcontainers import SortedDict

from src.event import TimedOccurrence


class TimeQueue:
    #TODO: maybe create another queue higher up that will work with any item and then this one will work with just TimedOccurrence, rather than combining it into one
    #priority queue for storing anything with time as a key
    def __init__(self):
        self._queue = SortedDict()

    # def add_by_time(self, time: float, item) -> None:
    #     self.queue[time] = item
    #
    # def remove_by_time(self, time: float) -> None:
    #     #TODO sort out for multiple entries for one time
    #     self.queue.pop(time)

    def add(self, item: TimedOccurrence):
        #id is unique for each object throughout its existence https://docs.python.org/3/library/functions.html#id
        self._queue[(item.time, id(item))] = item

    def pop(self): #-> TimedOccurrence:
    #remove and return first element
        return self._queue.popitem(0)[1]

    def top_item(self):
        return self._queue.peekitem(0)[1] #this is still O(log(n)) which is not ideal

    def next_time(self) -> float:
        return self._queue.peekitem(0)[0][0]

    def is_empty(self):
        return len(self._queue) == 0

    def remove(self, item: TimedOccurrence):
        self._queue.pop((item.time, id(item)))