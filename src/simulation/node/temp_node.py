from src import Node


class TempNode(Node):
    def __init__(self, x: float, y: float, neighbour1: tuple[int, float], neighbour2: tuple[int, float]):
        super().__init__(-1, x, y)
        self.add_neighbour(neighbour1[0], neighbour1[1])
        self.add_neighbour(neighbour2[0], neighbour2[1])