from typing import Self

from src import Node


class TempNode(Node):
    def __init__(self, x: float, y: float, neighbour1: tuple[int, float], neighbour2: tuple[int, float]):
        super().__init__(-1, x, y)
        self._neighbour1 = neighbour1
        self._neighbour2 = neighbour2

    def neighbours(self) -> tuple[Self, Self] | None:
        return self._neighbour1, self._neighbour2