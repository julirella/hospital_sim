from .node import Node

class Room(Node):
    """
    Node that is a room
    """
    def __init__(self, node_id: int, x: float, y: float) -> None:
        """
        :param node_id: ID of the node
        :param x: x coordinate of room centre in meters
        :param y: y coordinate of room centre in meters
        """
        super().__init__(node_id, x, y)