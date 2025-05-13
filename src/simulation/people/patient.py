from src.simulation.people.nurse import Nurse
from src.simulation.graph.node import PatientRoom
from src.simulation.sim_time import SimTime


class Patient:
    """
    class representing a patient
    """
    def __init__(self, patient_id: int, nurse: Nurse, room: PatientRoom) -> None:
        """
        :param patient_id: ID of the patient
        :param nurse: the patient's assigned nurse
        :param room: the room in which the patient is located
        """
        self._patient_id = patient_id
        self._nurse = nurse
        self._room = room

    @property
    def patient_id(self) -> int:
        return self._patient_id

    @property
    def nurse(self) -> Nurse:
        return self._nurse

    @property
    def room(self) -> PatientRoom:
        return self._room