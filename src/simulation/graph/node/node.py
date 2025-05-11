
class Node:
    """
    Node/vertex in the graph
    """
    def __init__(self, node_id: int, x: float, y: float) -> None:
        """
        :param node_id: ID of the node
        :param x: x coordinate in meters
        :param y: y coordinate in meters
        """
        self.node_id = node_id
        self._x = x
        self._y = y
        self._neighbours: list[tuple[int, float]] = []

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def neighbours(self) -> list[tuple[int, float]]:
        return self._neighbours

    def add_neighbour(self, neighbour_id: int, weight: float) -> None:
        """
        Add neighbouring node
        :param neighbour_id: ID of the neighbour
        :param weight: weight of the edge between the nodes (so their Euclidean distance)
        """
        self._neighbours.append((neighbour_id, weight))