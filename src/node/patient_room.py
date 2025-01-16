from .room import Room

class PatientRoom(Room):
    def __init__(self, node_id: int, x: int, y: int, room_number: int) -> None:
        super().__init__(node_id, x, y)
        self.room_number = room_number