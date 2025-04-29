from typing import TypeVar, Generic

from sortedcontainers import SortedDict
import heapdict as hd

from src.simulation.timed_object import TimedObject

T = TypeVar("T", bound=TimedObject)

class TimeQueue(Generic[T]):
    #priority queue for storing anything with (time, id) as a key
    def __init__(self):
        # self._queue = SortedDict()
        self._queue = hd.heapdict()

    def add(self, item: T):
        #id is unique for each object throughout its existence https://docs.python.org/3/library/functions.html#id
        # self._queue[(item.time, id(item))] = item
        self._queue[item] = item.time

    def pop(self) -> T:
    #remove and return first element
        # return self._queue.popitem(0)[1]
        return self._queue.popitem()[0]

    def top_item(self) -> T:
        # return self._queue.peekitem(0)[1] #this is still O(log(n)) which is not ideal
        return self._queue.peekitem()[0]

    def next_time(self) -> float:
        # return self._queue.peekitem(0)[0][0]
        return self._queue.peekitem()[1]

    def empty(self):
        return len(self._queue) == 0

    def remove(self, item: T):
        self._queue.pop(item)