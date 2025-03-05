class TimedObject:
    def __init__(self, time):
        self._time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        self._time = val