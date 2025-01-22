from sortedcontainers import SortedDict
from src.event import Event
from src.queue import TimeQueue


class EventQueue(TimeQueue):
    #for now the key is only time. Maybe switch to (time, event_id) to eliminate time collisions
    def __init__(self):
        super().__init__()
