from .node import Node

class Nurse:
    def __init__(self, nurse_id: int, pos: Node) -> None:
        self.pos: Node = pos

    def set_pos(self, pos: Node) -> None:
        self.pos = pos

    def get_pos(self) -> Node:
        return self.pos