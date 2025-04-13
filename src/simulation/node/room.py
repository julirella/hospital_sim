from .node import Node

class Room(Node):
    def __init__(self, node_id: int, x: float, y: float) -> None:
        super().__init__(node_id, x, y)