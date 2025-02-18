from typing import Self

class Node:
    def __init__(self, node_id: int, x: float, y: float) -> None:
        self.node_id = node_id
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def neighbours(self) -> tuple[Self, Self] | None:
        return None