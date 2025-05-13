class Corridor:
    """
    class representing a department corridor/graph edge
    """
    def __init__(self, one_end: tuple[float, float], other_end: tuple[float, float]):
        """
        :param one_end: coordinates of one end of the corridor
        :param other_end: coordinates of the other end of the corridor
        """
        self.one_end = one_end
        self.other_end = other_end
