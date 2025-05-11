import numpy as np


class VisPatient:
    """
    class representing a patient for visualisation
    """
    def __init__(self, colour, room_number, req_start_times: list[float], req_end_times: list[float]) -> None:
        """
        :param colour: colour of the patient rectangle
        :param room_number: number of the room the patient is in
        :param req_start_times: list of start times of all the patient's requests, sorted in ascending order
        :param req_end_times: list of end times of all the patient's requests, sorted such that the ith end time
        corresponds to the ith start time
        """
        self.colour = colour
        self.room_number = room_number
        self.req_start_times = np.array(req_start_times)
        self.req_end_times = np.array(req_end_times)

    def waiting_requests(self, time: float) -> int:
        """
        calculates the number of requests the patient is waiting for at a given time
        :param time: the given time
        :return: the number of requests the patient is waiting for at time
        """
        started_req = np.searchsorted(self.req_start_times, time, side='right').item()
        ended_req = np.searchsorted(self.req_end_times, time, side='right').item()
        return started_req - ended_req
