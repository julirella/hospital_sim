from .node import Node

class Junction(Node):
    def __init__(self, node_id: int, x: int, y: int) -> None:
        super().__init__(node_id, x, y)