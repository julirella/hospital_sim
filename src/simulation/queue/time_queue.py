from typing import TypeVar, Generic

import heapdict as hd

from src.simulation.timed_object import TimedObject

T = TypeVar("T", bound=TimedObject)

class TimeQueue(Generic[T]):
    """
    priority queue for storing objects with time as an attribute (sorted by time),
    a wrapper around heapdict
    """
    def __init__(self):
        self._queue = hd.heapdict()

    def add(self, item: T) -> None:
        """
        add item to queue
        :param item: the item to be added
        """
        self._queue[item] = item.time

    def pop(self) -> T:
        """
        remove and return the first item from the queue
        :return: first item from the queue
        """
        return self._queue.popitem()[0]

    def top_item(self) -> T:
        """
        return the first item from the queue
        :return: first item from the queue
        """
        return self._queue.peekitem()[0]

    def next_time(self) -> float:
        """
        :return: time of the next item in the queue
        """
        return self._queue.peekitem()[1]

    def empty(self) -> bool:
        """
        :return: True if the queue is empty, else False
        """
        return len(self._queue) == 0

    def remove(self, item: T):
        """
        remove an item from the queue
        :param item: the item to be removed
        """
        self._queue.pop(item)