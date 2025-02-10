from .nurse import Nurse
from .node import PatientRoom
from .sim_time import SimTime


class Patient:
    def __init__(self, patient_id: int, nurse: Nurse, room: PatientRoom, sim_time: SimTime) -> None:
        self._patient_id = patient_id
        self.__nurse = nurse
        self.__room = room
        self.__sim_time = sim_time
        # self._waiting_events = set()
        # self._log: list[dict] = []

    @property
    def patient_id(self) -> int:
        return self._patient_id

    def get_nurse(self) -> Nurse:
        return self.__nurse

    def get_room(self) -> PatientRoom:
        return self.__room

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
    #     self._log.append({"time": self.__sim_time.get_sim_time(), "event": event_id, "action": action})