from src.simulation.graph.node import Node
from src.simulation.sim_time import SimTime
from src.constants import *


class Nurse:
    """
    class representing a nurse
    """
    def __init__(self, nurse_id: int, pos: Node, sim_time: SimTime) -> None:
        """
        :param nurse_id: ID of the nurse
        :param pos: node on which the nurse is located
        :param sim_time: SimTime object to track simulation time
        """
        self._nurse_id = nurse_id
        self._pos: Node = pos
        self._sim_time: SimTime = sim_time
        self._assigned_event_id: int | None = None # id of event that nurse is currently doing
        self._current_patient_id: int | None = None # id of patient that nurse is currently caring for based on assigned event
        self._log: list[dict] = [] # log of the nurse's actions throughout the simulation
        self._speed = NURSE_SPEED_MPS # nurse walking speed

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def nurse_id(self) -> int:
        return self._nurse_id

    @property
    def pos(self) -> Node:
        return self._pos

    @property
    def log(self) -> list[dict]:
        return self._log

    def assign_event(self, event_id: int, patient_id: int=None) -> None:
        """
        assigns an event to the nurse, the nurses actions are then driven by that event, logs it
        :param event_id: ID of the event
        :param patient_id: ID of the patient connected to the event (if it is a patient event)
        """
        self._assigned_event_id = event_id
        self._current_patient_id = patient_id
        self.__log_action__("assign event")

    def unassign_event(self) -> None:
        """
        unassigns the current event, logs it
        """
        #effectively the same as finish except for different log message
        self.__log_action__("unassign event")
        self._assigned_event_id = None
        self._current_patient_id = None

    def finish_event(self) -> None:
        """
        finishes the current event, logs it
        :return:
        """
        self.__log_action__("finish event")
        self._assigned_event_id = None
        self._current_patient_id = None

    def move(self, dst: Node) -> None:
        """
        sets nurse position to dst, logs the movement
        :param dst: destination node
        """
        #the same as set_pos, but logs movement
        self._pos = dst
        self.__log_action__("move to")

    def time_at_patient(self)-> None:
        """
        logs time spent at patient
        """
        self.__log_action__("time at patient")

    def __log_action__(self, action: str) -> None:
        self._log.append({"time": self._sim_time.sim_time, "nurse": self._nurse_id, "x": self._pos.x, "y": self._pos.y,
                          "event": self._assigned_event_id, "action": action, "patient": self._current_patient_id})