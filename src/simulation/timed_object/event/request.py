from src.simulation.timed_object import PatientEvent
from src.simulation.people.patient import Patient
from src.simulation.people.nurse import Nurse
from src import Graph, SimTime


class Request(PatientEvent):
    """
    class representing a patient's request
    """
    def __init__(self, time: float, duration: float, patient: Patient, level: int, graph: Graph, sim_time: SimTime) -> None:
        """
        :param time: time of patient's request
        :param duration: length of time to be spent caring for the patient during this event
        :param patient: patient that has the request
        :param level: level of urgency of request (1 - low, 2 - medium, 3 - high)
        :param graph: department graph
        :param sim_time: SimTime object to track simulation time
        """
        self._level = level
        super().__init__(time, duration, patient, None, graph, sim_time)

    def assign_nurse(self, nurse: Nurse):
        self._assigned_nurse = nurse

    @property
    def level(self) -> int:
        return self._level

    @property
    def type(self) -> str:
        return "request"

    def __log_action__(self, action: str, time: float) -> None:
        action_dict = {"time": time, "event": self._event_id, "action": action,
                          "patient": self._patient.patient_id, "type": self.type, "request_level": self.level}
        # print(action_dict)
        self._log.append({"time": time, "event": self._event_id, "action": action,
                          "patient": self._patient.patient_id, "type": self.type, "request_level": self.level})
