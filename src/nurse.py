from .node import Node
from .sim_time import SimTime

# NURSE_KPH = 4
# NURSE_PPS = 30 #pixels per second
NURSE_SPEED_MPS = 1

class Nurse:
    def __init__(self, nurse_id: int, pos: Node, sim_time: SimTime) -> None:
        self.__nurse_id = nurse_id
        self.__pos: Node = pos
        self.__sim_time: SimTime = sim_time
        self.__assigned_event_id: int | None = None
        self.__log: list[dict] = []
        self._speed = NURSE_SPEED_MPS

    @property
    def speed(self) -> float:
        return self._speed

    def get_id(self) -> int:
        return self.__nurse_id

    def set_pos(self, pos: Node) -> None:
        self.__pos = pos

    def get_pos(self) -> Node:
        return self.__pos

    def get_log(self) -> list[dict]:
        return self.__log

    def assign_event(self, event_id: int) -> None:
        self.__assigned_event_id = event_id
        self.__log_action__("assign event")

    def unassign_event(self) -> None:
        #effectively the same as finish except for different log message
        self.__log_action__("unassign event")
        self.__assigned_event_id = None

    def finish_event(self) -> None:
        self.__log_action__("finish event")
        self.__assigned_event_id = None

    def move(self, dst: Node) -> None:
        #the same as set_pos, but logs movement
        self.__pos = dst
        self.__log_action__("move to")

    def time_at_patient(self)-> None:
        self.__log_action__("time at patient")

    def __log_action__(self, action: str) -> None:
        # self.__log.append({"time": self.__sim_time.get_sim_time(), "position": self.__pos.node_id, "event": self.__assigned_event_id, "action": action})
        self.__log.append({"time": self.__sim_time.get_sim_time(), "x": self.__pos.x, "y": self.__pos.y, "event": self.__assigned_event_id, "action": action})
