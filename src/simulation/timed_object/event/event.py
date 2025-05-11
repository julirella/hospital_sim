from abc import abstractmethod
from enum import IntEnum
import itertools

from src import Nurse, Graph, SimTime, Node
from src.simulation.timed_object import TimedObject, Movement, Step


class EventStatus(IntEnum):
    # enum to track event status
    NOT_STARTED = 1
    ACTIVE = 2
    PAUSED = 3

class Event(TimedObject):
    """
    class representing an event
    """
    _id_generator = itertools.count(0) # gives each object a unique ID sequentially (starts from 0 and goes up by 1)

    def __init__(self, time: float, duration: float, assigned_nurse: Nurse | None,
                 graph: Graph, sim_time: SimTime):
        """
        :param time: event planned start time
        :param duration: event duration (without walking to it)
        :param assigned_nurse: nurse dealing with event
        :param graph: department graph
        :param sim_time: SimTime object to track simulation time
        """
        super().__init__(time)
        self._event_id = next(Event._id_generator)
        self._duration = duration
        self._assigned_nurse = assigned_nurse
        self._graph = graph
        self._sim_time = sim_time
        self._status = EventStatus.NOT_STARTED
        self._steps: list[Step] = [] # list of event steps
        self._log: list[dict] = [] # log of the event's actions throughout the simulation
        self.__log_action__("planned start", self._time)

    @property
    @abstractmethod
    def type(self) -> str:
        # https://stackoverflow.com/questions/2736255/abstract-attributes-in-python
        pass

    def __create_movement_steps__(self, start: Node, end: Node) -> float:
        # calculate steps for getting to destination where event takes place
        path_there = self._graph.find_path(start, end)
        prev_step_time = self._time

        # getting there
        from_node = start
        for i in range(len(path_there)):
            to_node, dst = path_there[i]
            step_duration = dst / self._assigned_nurse.speed
            step_time = prev_step_time + step_duration
            step = Movement(step_time, self._assigned_nurse, from_node, to_node)
            self._steps.append(step)
            prev_step_time = step_time
            from_node = to_node

        return prev_step_time

    @abstractmethod
    def __create_steps__(self) -> None:
        # calculate event steps and add to list
        pass

    def __start__(self) -> None:
        # start event by calculating steps and assigning to nurse
        self.__create_steps__()
        self._assigned_nurse.assign_event(self._event_id)
        self._status = EventStatus.ACTIVE

    def __pop_next_step__(self) -> Step:
        # remove and return top step from list of steps
        step: Step = self._steps.pop(0)
        return step

    def __is_finished__(self) -> bool:
        if len(self._steps) == 0:
            return True
        else:
            return False

    @property
    def status(self) -> EventStatus:
        return self._status

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def log(self) -> list[dict]:
        return self._log

    def next_time(self) -> float:
        """
        :return: time of next step, or of event itself if steps have not yet been created
        """
        if len(self._steps) == 0:
            return self.time
        else:
            return self._steps[0].time

    def get_next_step(self) -> Step:
        """
        :return: next event step if event is active
        :raise: exception if event is not active
        """
        # assumes only future steps are in this list
        if self._status == EventStatus.ACTIVE:
            return self._steps[0]
        else:
            raise Exception("get next step can only be called on active event")

    def run_next_step(self) -> bool:
        """
        run the next event step
        :return: true if running the step finishes the event
        """

        if self._status == EventStatus.NOT_STARTED:
            self.__start__()  # at this point start and resume is the same
            self.__log_action_now__("actual start")
        elif self._status == EventStatus.PAUSED:
            self.__start__()
            self.__log_action_now__("resume")
        elif self._status == EventStatus.ACTIVE:
            step: Step = self.__pop_next_step__()
            step.run()

        if self.__is_finished__():
            self._assigned_nurse.finish_event()
            self.__log_action_now__("end")

        return self.__is_finished__()

    @abstractmethod
    def pause(self) -> None:
        """
        pause event
        """
        pass

    def __log_action__(self, action: str, time: float) -> None:
        self._log.append({"time": time, "event": self._event_id, "action": action, "type": self.type})

    def __log_action_now__(self, action: str) -> None:
        self.__log_action__(action, self._sim_time.sim_time)