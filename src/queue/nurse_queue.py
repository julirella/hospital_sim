from .event_queue import EventQueue
from src.nurse import Nurse
from src.event import Event, Step, EventStatus
from .. import Request

MAX_WALK_TIME = 20 #TODO: recalculate based on dept size

class NurseQueue(EventQueue):
    def __init__(self, nurse: Nurse) -> None:
        super().__init__()
        self.nurse = nurse

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        max_event_duration = event.get_duration() + MAX_WALK_TIME #TODO switch to smarter walk time
        prev_end_time = event.get_time() #again assuming this is a request which has time set to now.
        #probably better to get it from the time struct

        for queue_event in self.queue.values():
            next_start_time = queue_event.get_time()
            if next_start_time - prev_end_time > max_event_duration:
                event.set_time(prev_end_time)
                self.queue[prev_end_time] = event
                break
            prev_end_time = next_start_time + queue_event.get_duration()


    #add event after end of current running event
    def add_after_current(self, new_event: Event) -> None:
        current_event: Event = self.top_item()
        if current_event.get_status() == EventStatus.NOT_STARTED:
            #it just goes straight away
            #if inserting request, it's time is already current time, but if it was used elsewhere the time would have to be changed
            self.queue[new_event.get_time()] = new_event
        else:
            current_end = current_event.end_time()
            new_event.set_time(current_end)
            self.queue[current_end] = new_event
        #push back other events? or recalculate their times later?

    #add event to absolute start of event, pausing running event if necessary
    def add_to_start(self, new_event: Event) -> None:
        #pause event
        current_event: Event = self.top_item()
        if current_event.get_status() == EventStatus.NOT_STARTED:
            current_event.pause()
        #add to start
        self.add_by_time(new_event.get_time(), new_event)
        #push events back?
        ...

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
