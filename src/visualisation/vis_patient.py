import numpy as np


class VisPatient:
    def __init__(self, colour, room_number, req_start_times: list[float], req_end_times: list[float]):
        self.colour = colour
        self.room_number = room_number
        self.req_start_times = np.array(req_start_times)
        self.req_end_times = np.array(req_end_times)

    def waiting_requests(self, time) -> int:
        started_req = np.searchsorted(self.req_start_times, time, side='right').item()
        ended_req = np.searchsorted(self.req_end_times, time, side='right').item()
        return started_req - ended_req
