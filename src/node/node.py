from typing import Self

class Node:
    def __init__(self, node_id: int, x: float, y: float) -> None:
        self.node_id = node_id
        self.x = x
        self.y = y

    def neighbours(self) -> tuple[Self, Self] | None:
        return None