from .room import Room

class PatientRoom(Room):
    def __init__(self, node_id: int, x: float, y: float, room_number: int) -> None:
        super().__init__(node_id, x, y)
        self._room_number = room_number

    @property
    def room_number(self) -> int:
        return self._room_number