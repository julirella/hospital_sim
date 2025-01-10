class Request:
    def __init__(self, id: int, patient_id: int, level: int, duration: float) -> None:
        self.id = id
        self.patient_id = patient_id
        self.level = level
        self.duration = duration