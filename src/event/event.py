from src.nurse import Nurse

class Event:
    def __init__(self, event_id: int, assigned_nurse: Nurse | None) -> None:
        self.event_id = event_id
        self.assigned_nurse = assigned_nurse