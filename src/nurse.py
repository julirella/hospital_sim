from .node import Node
from .sim_time import SimTime
from .constants import *

# NURSE_KPH = 4
# NURSE_PPS = 30 #pixels per second

class Nurse:
    def __init__(self, nurse_id: int, pos: Node, sim_time: SimTime) -> None:
        self._nurse_id = nurse_id
        self._pos: Node = pos
        self._sim_time: SimTime = sim_time
        self._assigned_event_id: int | None = None
        self._current_patient_id: int | None = None
        self._log: list[dict] = []
        self._speed = NURSE_SPEED_MPS

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def nurse_id(self) -> int:
        return self._nurse_id

    def move_to(self, pos: Node) -> None:
        self._pos = pos

    @property
    def pos(self) -> Node:
        return self._pos

    @property
    def log(self) -> list[dict]:
        return self._log

    def assign_event(self, event_id: int, patient_id: int) -> None:
        self._assigned_event_id = event_id
        self._current_patient_id = patient_id
        self.__log_action__("assign event")

    def unassign_event(self) -> None:
        #effectively the same as finish except for different log message
        self.__log_action__("unassign event")
        self._assigned_event_id = None
        self._current_patient_id = None

    def finish_event(self) -> None:
        self.__log_action__("finish event")
        self._assigned_event_id = None

    def move(self, dst: Node) -> None:
        #the same as set_pos, but logs movement
        self._pos = dst
        self.__log_action__("move to")

    def time_at_patient(self)-> None:
        self.__log_action__("time at patient")

    def __log_action__(self, action: str) -> None:
        self._log.append({"time": self._sim_time.get_sim_time(), "nurse": self._nurse_id, "x": self._pos.x, "y": self._pos.y,
                          "event": self._assigned_event_id, "action": action, "patient": self._current_patient_id})