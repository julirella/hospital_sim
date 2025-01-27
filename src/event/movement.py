from .step import Step
from src.nurse import Nurse
from src.node import Node

class Movement(Step):
    def __init__(self, time: float, nurse: Nurse, start: Node, end: Node) -> None:
        super().__init__(time, nurse)
        self.__start = start #does this need to know start?
        self.__end = end

    def run(self) -> None:
        self._nurse.move(self.__end)