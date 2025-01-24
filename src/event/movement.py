from .step import Step
from src.nurse import Nurse
from src.node import Node

class Movement(Step):
    def __init__(self, time: float, nurse: Nurse, start: Node, end: Node) -> None:
        super().__init__(time, nurse)
        self.start = start #does this need to know start?
        self.end = end

    def run(self) -> None:
        self.nurse.set_pos(self.end)