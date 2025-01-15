class EventQueue:
    def __init__(self):
        self.queue = []

    def add(self, event):
        self.queue.append(event)

    def get(self):
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0