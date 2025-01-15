from .start_event import StartEvent

class Request(StartEvent):
    def __init__(self, event_id: int, patient_id: int, level: int, duration: float) -> None:
        super().__init__(event_id)
        self.patient_id = patient_id
        self.level = level
        self.duration = duration