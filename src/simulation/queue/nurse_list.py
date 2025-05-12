from src import SimTime, Nurse, Graph
from src.simulation.timed_object import EventStatus, TimedNurseId, ReturnToOffice, Event
from src.simulation.queue.event_list import EventList, ListEvent

class NurseList(EventList[Event]):
    """
    class representing a linked list of events in a nurse queue
    """
    def __init__(self, events: list[Event], sim_time: SimTime, nurse: Nurse, max_graph_dst: float, graph: Graph):
        """
        :param events: events to be stored in queue
        :param sim_time: SimTime object to track simulation time
        :param nurse: nurse to whom the queue belongs
        :param max_graph_dst: max distance that can be walked in graph
        :param graph: department graph
        """
        super().__init__(events)
        self._sim_time: SimTime = sim_time
        self._graph = graph
        self._nurse: Nurse = nurse
        self._nurse_id = nurse.nurse_id
        self._max_walk_time = max_graph_dst / nurse.speed #longest walk time for nurse between any two nodes in graph
        self._timed_nurse_id: TimedNurseId # combination of time of first event and the nurse's ID
        self._event_logs = [] # list for logs of finished events
        self._in_global_queue: bool = False

    @property
    def event_logs(self):
        return self._event_logs

    @property
    def in_global_queue(self) -> bool:
        return self._in_global_queue

    @property
    def nurse(self) -> Nurse:
        return self._nurse

    @in_global_queue.setter
    def in_global_queue(self, value: bool):
        self._in_global_queue = value

    def __max_event_duration__(self, event: Event) -> float:
        # maximum duration of an event including time to walk there
        return event.duration + self._max_walk_time

    def __insert_after__(self, new_event: Event, pred_event: ListEvent=None) -> None:
        #insert new_event after pred_event. If pred_event is None, add to front of list
        new_list_event: ListEvent

        if pred_event is None:
            new_list_event = ListEvent(new_event, self._front)
            self._front = new_list_event
            new_event.time = self._sim_time.sim_time
        else:
            new_list_event = ListEvent(new_event, pred_event.next)
            pred_event.next = new_list_event
            new_event.time = pred_event.event.time + pred_event.event.duration + self._max_walk_time

        #push_back if necessary, could probably be a separate method
        #at this point we know new event is far enough from the event before it, but the following event may be too close
        current = new_list_event
        while current.next is not None and current.event.time + current.event.duration + self._max_walk_time > current.next.event.time:
            current.next.event.time = current.event.time + current.event.duration + self._max_walk_time
            current = current.next

    def __replace_return_to_office__(self, event: Event):
        #stops current return to office event, removes it, logs it and adds event to start
        current_event = self._front.event
        if current_event.type != 'return_to_office':
            raise Exception("can't replace event that isn't return to office")

        current_event.pause()
        finished_log = self.pop_front().log
        self._event_logs += finished_log
        self.__insert_after__(event)

    def has_time_now(self, event: Event) -> bool:
        """
        checks if nurse currently has enough free time to deal with event including walking there
        :param event: the event to be dealt with
        :return: True if nurse has enough time, else False
        """

        if self.empty():
            return True

        front_event_time = self._front.event.time

        # if the first event is return to office, the event after that is considered as the first event
        # because return to office can always be cancelled
        if self.front().type == 'return_to_office':
            if self._front.next is None:
                return True
            else:
                front_event_time = self._front.next.event.time

        return self.empty() or self.__max_event_duration__(event) <= front_event_time - self._sim_time.sim_time

    def current_event_level(self) -> int:
        """
        :return: if current event is a request, then its level, if it's a plan then 1, else -1 (even if the queue is empty)
        """
        if self.empty():
            return -1

        current_event = self._front.event
        if current_event.status == EventStatus.ACTIVE and current_event.type == 'request':
            return current_event.level
        elif current_event.status == EventStatus.ACTIVE and current_event.type == 'plan':
            return 1
        else:
            return -1

    def add_to_gap(self, event: Event) -> None:
        """
        finds a gap in the list big enough for event (including walk time) and inserts it there
        :param event: the event to be added
        """
        if self.empty():
            self.__insert_after__(event)
            return

        max_event_duration = self.__max_event_duration__(event)
        prev_end_time = self._sim_time.sim_time

        prev_event = None
        next_event: ListEvent = self._front
        done = False

        if (next_event.event.type == 'return_to_office' and
                (next_event.next is None or next_event.next.event.time - prev_end_time > max_event_duration)):
            # there is enough time before the next non return to office event, but there is a return to office in the way
            # so the return to office event should be stopped
            done = True
            self.__replace_return_to_office__(event)
        else:
            while next_event is not None:
                next_start_time = next_event.event.time
                if next_start_time - prev_end_time > max_event_duration: #new event fits
                    self.__insert_after__(event, prev_event)
                    done = True
                    break
                prev_end_time = next_event.event.time + next_event.event.duration + self._max_walk_time
                prev_event = next_event
                next_event = next_event.next

        if not done:
            self.__insert_after__(event, prev_event)

    def add_after_current(self, event: Event) -> None:
        """
        If there is currently a running event, adds the new event behind it, pushing back subsequent events. If there
        is no running event or the first event is return to office, adds it to start.
        :param event: the event to be added
        """
        if self.empty():
            self.__insert_after__(event)
            return

        current_event: Event = self.front()
        if current_event.type == 'return_to_office':
            # running return to office just gets cancelled
            self.__replace_return_to_office__(event)
        elif current_event.status == EventStatus.NOT_STARTED:
            # it just goes straight away
            self.__insert_after__(event)
        else:
            self.__insert_after__(event, self._front)

    def add_to_start(self, event: Event) -> None:
        """
        Adds new event to the start of the list, pausing the first event if it is running and pushing back all
        events in queue.
        :param event: the event to be added
        """
        if self.empty():
            self.__insert_after__(event)
            return

        current_event: Event = self.front()

        if current_event.type == 'return_to_office':
            # return to office can just be cancelled (even if it hasn't started yet)
            current_event.pause()
            finished_log = self.pop_front().log
            self._event_logs += finished_log

        elif current_event.status == EventStatus.ACTIVE:
            current_event.pause() #pause current if necessary


        #insert new and push back rest
        self.__insert_after__(event, None)


    def run_next_step(self) -> bool:
        """
        run the next step of the first event in list, removing first event if it is finished in the process
        :return: True if this finishes the current event, else False
        """

        if self.empty():
            raise Exception("can't run next step of emtpy list")

        #call run next step of top event
        next_event: Event = self.front()
        finished: bool = next_event.run_next_step()
        #if the event is over, remove it
        if finished: # don't return again if already returned to office
            finished_log = self.pop_front().log
            self._event_logs += finished_log
            if (self.empty() or self.next_time() - self._sim_time.sim_time >= self._max_walk_time * 2) and self._nurse.pos != self._graph.nurse_office:
                #create return to office event
                return_event = ReturnToOffice(self._nurse, self._graph, self._sim_time)
                self.__insert_after__(return_event)

        return finished

    def create_timed_nurse_id(self) -> TimedNurseId:
        """
        create a TimedNurseId object for the combination of the time of the next event and the nurse's ID
        :return: the created TimedNurseId
        """
        self._timed_nurse_id = TimedNurseId(self.next_time(), self._nurse_id)
        return self._timed_nurse_id

    def current_timed_nurse_id(self) -> TimedNurseId:
        """
        :return: current TimedNurseId representing the time of the next event in the list and the nurse's ID
        """
        return self._timed_nurse_id