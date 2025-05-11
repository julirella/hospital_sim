import math

from src.simulation.timed_object.step.step import Step
from src.simulation.people.nurse import Nurse
from src.simulation.graph.node import Node
from src.simulation.graph.node.temp_node import TempNode


class Movement(Step):
    """
    class representing a movement step
    """
    def __init__(self, time: float, nurse: Nurse, start: Node, end: Node) -> None:
        """
        :param time: time of the movement's end, so the time of arrival at the end node
        :param nurse: the nurse that is moving
        :param start: starting node of the step
        :param end: ending node of the step
        """
        super().__init__(time, nurse)
        self._start = start
        self._end = end

    def run(self) -> None:
        """
        move the nurse from the start node to the end node
        """
        self._nurse.move(self._end)

    def pause(self, pause_time) -> float:
        """
        pause the movement step, calculating and staving the nurse's location at pause time
        :param pause_time: the time at which the pause happens
        :return: 0
        """

        # calculate the nurse's location at pause time based on start and end node location
        total_x = self._end.x - self._start.x
        total_y = self._end.y - self._start.y
        total_dst = math.sqrt(total_x**2 + total_y**2)
        total_time = total_dst / self._nurse.speed
        remaining_time = self._time - pause_time
        remaining_time_ratio = remaining_time / total_time
        remaining_x = remaining_time_ratio * total_x
        remaining_y = remaining_time_ratio * total_y
        current_x = self._end.x - remaining_x
        current_y = self._end.y - remaining_y
        remaining_dst = remaining_time_ratio * total_dst
        covered_dst = total_dst - remaining_dst

        # move nurse to the paused position
        current_pos = TempNode(current_x, current_y, (self._start.node_id, covered_dst),
                               (self._end. node_id, remaining_dst))
        self._nurse.move(current_pos)

        return 0 # yes, this is a bit hacky