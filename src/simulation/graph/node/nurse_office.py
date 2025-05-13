from .room import Room

class NurseOffice(Room):
    """
    node representing the nurse office
    currently there is only one nurse office
    """
    def __init__(self, node_id: int, x: float, y: float) -> None:
        super().__init__(node_id, x, y)
