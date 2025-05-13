from src import Node


class TempNode(Node):
    """
    temporary node that splits an edge (corridor) in two, it's neighbours are the edges vertices
    """
    def __init__(self, x: float, y: float, neighbour1: tuple[int, float], neighbour2: tuple[int, float]):
        """
        :param x: node x coordinate
        :param y: node y coordinate
        :param neighbour1: one edge vertex
        :param neighbour2: the other edge vertex
        """
        super().__init__(-1, x, y) # sets node ID to -1 to later identify this node type
        self.add_neighbour(neighbour1[0], neighbour1[1])
        self.add_neighbour(neighbour2[0], neighbour2[1])