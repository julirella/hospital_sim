class VisPatient:
    def __init__(self, colour, room_number, req_start_times, req_end_times):
        self.colour = colour
        self.room_number = room_number
        self.req_start_times: list[float] = req_start_times
        self.req_end_times: list[float] = req_end_times