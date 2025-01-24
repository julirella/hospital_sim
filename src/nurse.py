from .node import Node
from .sim_time import SimTime


class Nurse:
    def __init__(self, nurse_id: int, pos: Node, sim_time: SimTime) -> None:
        self.nurse_id = nurse_id
        self.pos: Node = pos
        self.sim_time: SimTime = sim_time
        self.assigned_event_id: int | None = None
        self.log = []

    def set_pos(self, pos: Node) -> None:
        self.pos = pos

    def get_pos(self) -> Node:
        return self.pos

    def assign_event(self, event_id: int) -> None:
        self.assigned_event_id = event_id
        self.log_action("assign event")

    def finish_event(self) -> None:
        self.assigned_event_id = None
        self.log_action("finish event")

    def move(self, dst: Node) -> None:
        #the same as set_pos, but logs movement
        self.pos = dst
        self.log_action("move to")

    def log_action(self, action: str) -> None:
        self.log.append({"time": self.sim_time.get_sim_time(), "position": self.pos.node_id, "event": self.assigned_event_id, "action": action})