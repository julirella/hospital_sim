from sortedcontainers import SortedDict

from .event_queue import EventQueue
from src.nurse import Nurse
from src.event import Event, Step, EventStatus
from src import SimTime

MAX_WALK_TIME = 20 #TODO: recalculate based on dept size

class NurseQueue(EventQueue):
    def __init__(self, nurse: Nurse, sim_time: SimTime) -> None:
        super().__init__()
        self.nurse = nurse
        self.__sim_time = sim_time

    def __max_event_duration__(self, event: Event) -> float:
        return event.get_duration() + MAX_WALK_TIME  # TODO switch to smarter walk time

    #add amount to time of all events from start_time until a big enough gap is found
    def __push_back_events__(self, amount: float, start_time: float) -> None:
        #TODO something more efficient
        new_queue = SortedDict()
        push_back = True
        start = False
        prev_end = self.__sim_time.get_sim_time()
        time: float
        event: Event
        for time, event in self._queue.items():
            event_start = time - event.get_duration()
            if time > start_time:
                start = True
            if event_start - prev_end > amount: #found big enough gap for event, no need to push rest back
                push_back = False
            if push_back is True and start is True:
                event.set_time(time + amount)
                new_queue[time + amount] = event
                prev_end = time + amount
            else:
                new_queue[time] = event
                prev_end = time
        self.queue = new_queue

    #find gap in queue to fit event and add it there
    def add_to_gap(self, event: Event) -> None:
        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self.__sim_time.get_sim_time()

        queue_event: Event
        for queue_event in self.queue.values():
            next_start_time = queue_event.time()
            if next_start_time - prev_end_time > max_event_duration:
                event.set_time(prev_end_time)
                self.queue[prev_end_time] = event
                break
            prev_end_time = next_start_time + queue_event.get_duration()

    #add event after end of current running event
    def add_after_current(self, new_event: Event) -> None:
        current_event: Event = self.top_item()
        max_event_duration = self.__max_event_duration__(new_event)
        if current_event.get_status() == EventStatus.NOT_STARTED:
            #it just goes straight away
            self.__push_back_events__(max_event_duration, self.__sim_time.get_sim_time())
            #if inserting request, its time is already current time, but if it was used elsewhere the time would have to be changed
            self.queue[self.__sim_time.get_sim_time()] = new_event
        else:
            current_end = current_event.end_time()
            self.__push_back_events__(max_event_duration, current_end)
            new_event.set_time(current_end)
            self.queue[current_end] = new_event
        #push back other events? or recalculate their times later?


    #add event to absolute start of event, pausing running event if necessary
    def add_to_start(self, new_event: Event) -> None:
        #pause current event
        current_event: Event = self.top_item()
        if current_event.get_status() == EventStatus.ACTIVE:
            current_event.pause()

        #push events back?
        self.__push_back_events__(self.__max_event_duration__(new_event), self.__sim_time.get_sim_time())
        #add to start
        self.add_by_time(self.__sim_time.get_sim_time(), new_event)




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
