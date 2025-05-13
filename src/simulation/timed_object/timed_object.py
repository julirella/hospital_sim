class TimedObject:
    """
    class representing an object that has a time attribute
    """
    def __init__(self, time):
        """
        :param time: time
        """
        self._time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        self._time = val