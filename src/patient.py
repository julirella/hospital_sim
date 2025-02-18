from .nurse import Nurse
from .node import PatientRoom
from .sim_time import SimTime


class Patient:
    def __init__(self, patient_id: int, nurse: Nurse, room: PatientRoom, sim_time: SimTime) -> None:
        self._patient_id = patient_id
        self._nurse = nurse
        self._room = room
        self._sim_time = sim_time
        # self._waiting_events = set()
        # self._log: list[dict] = []

    @property
    def patient_id(self) -> int:
        return self._patient_id

    @property
    def nurse(self) -> Nurse:
        return self._nurse

    @property
    def room(self) -> PatientRoom:
        return self._room

    # def start_waiting(self, event_id):
    #     self._waiting_events.add(event_id)
    #     self.__log_action__("start waiting", event_id)
    #
    # def finish_event(self, event_id):
    #     self._waiting_events.remove(event_id)
    #     self.__log_action__("finish event", event_id)
    #
    #
    # def __log_action__(self, action: str, event_id: int) -> None:
    #     self._log.append({"time": self.__sim_time.sim_time, "event": event_id, "action": action})