from .event_queue import EventQueue
from src.nurse import Nurse
from src.event import Event, Step


class NurseQueue(EventQueue):
    def __init__(self, nurse: Nurse) -> None:
        super().__init__()
        self.nurse = nurse

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        pass

    def get_next_step(self) -> Step:
        time: float
        event: Event
        time, event = self.queue.peekitem(0)
        return event.get_next_step() #sort out if this is the last step

    def run_next_step(self) -> None:
        #call run next step of top event
        next_event: Event = self.top_item()
        finished: bool = next_event.run_next_step()
        #if the event is over, remove it (and maybe log that)
        if finished:
            self.pop()

    def next_time(self) -> float:
        next_event: Event = self.top_item()
        return next_event.next_time()
