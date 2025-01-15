from .room import Room

class PatientRoom(Room):
    def init(self, node_id: int, x: int, y: int) -> None:
        super().__init__(node_id, x, y)