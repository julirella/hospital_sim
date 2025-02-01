import math

from .step import Step
from src.nurse import Nurse
from src.node import Node
from src.node.temp_node import TempNode


class Movement(Step):
    def __init__(self, time: float, nurse: Nurse, start: Node, end: Node) -> None:
        super().__init__(time, nurse)
        self._start = start #does this need to know start?
        self._end = end

    def run(self) -> None:
        self._nurse.move(self._end)

    def pause(self, pause_time) -> None:
        #surely there's a simpler way
        total_x = self._end.x - self._start.x
        total_y = self._end.y - self._start.y
        total_dst = math.sqrt(total_x**2 + total_y**2)
        nurse_speed = 30 #TODO: figure out actual speed
        total_time = total_dst / nurse_speed
        remaining_time = self._time - pause_time
        remaining_time_ratio = remaining_time / total_time
        remaining_x = remaining_time_ratio * total_x
        remaining_y = remaining_time_ratio * total_y
        current_x = self._end.x - remaining_x
        current_y = self._end.y - remaining_y
        remaining_dst = remaining_time_ratio / total_dst
        covered_dst = total_dst - remaining_dst

        current_pos = TempNode(current_x, current_y, (self._start.node_id, covered_dst),
                               (self._end. node_id, remaining_dst))

        self._nurse.set_pos(current_pos)
