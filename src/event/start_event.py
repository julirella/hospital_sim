from .event import Event

class StartEvent(Event):
    def __init__(self, event_id: int) -> None:
        Event.__init__(self, event_id)