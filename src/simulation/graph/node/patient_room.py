from .room import Room

class PatientRoom(Room):
    """
    node representing a patient room
    """
    def __init__(self, node_id: int, x: float, y: float, room_number: int) -> None:
        """
        :param node_id: ID of the node
        :param x: x coordinate of room centre in meters
        :param y: y coordinate of room centre in meters
        :param room_number: room number
        """
        super().__init__(node_id, x, y)
        self._room_number = room_number

    @property
    def room_number(self) -> int:
        return self._room_number