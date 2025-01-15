from . import Event
from .step import Step
from src.nurse import Nurse
from src.node import Node

class Movement(Step):
    def __init__(self, event_id: int, nurse: Nurse, start: Node, end: Node ) -> None:
        super().__init__(event_id, nurse)
        self.start = start
        self.end = end