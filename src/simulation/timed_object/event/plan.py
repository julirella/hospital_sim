from src.simulation.timed_object import PatientEvent
from src.simulation.people.patient import Patient
from src.simulation.people.nurse import Nurse
from src import Graph, SimTime


class Plan(PatientEvent):
    """
    class representing a nurse's planned event
    """
    def __init__(self, time: float, duration: float, patient: Patient, nurse: Nurse, graph: Graph, sim_time: SimTime) -> None:
        """
        :param time: event planned start time
        :param duration: length of time to be spent caring for the patient during this event
        :param patient: patient who the nurse plans to care for during this event
        :param nurse: nurse whose plan this event is
        :param graph: department graph
        :param sim_time: SimTime object to track simulation time
        """
        super().__init__(time, duration, patient, nurse, graph, sim_time)

    @property
    def type(self) -> str:
        return "plan"
