import unittest
from unittest.mock import Mock

from src.event import *


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.mock_patient = Mock()
        self.mock_patient.room = Mock()
        self.mock_graph = Mock()
        self.mock_nurse = Mock()
        self.mock_nurse.get_pos.return_value = Mock()
        self.event = Event(event_id=1, time=50, duration=30, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                           graph=self.mock_graph)

    def test_run_next_step_starts_event(self):
        self.event.run_next_step()
        self.assertNotEqual(self.event.get_next_step(), None)

    def test_run_next_step_executes_steps(self):
        while not self.event.run_next_step():
            pass
        self.mock_nurse.finish_event.assert_called()

    def test_steps_execution_order(self):
        self.event.run_next_step()
        previous_step = None
        while not self.event.run_next_step():
            current_step = self.event.get_next_step()
            if previous_step:
                self.assertGreater(current_step._time, previous_step._time)
            previous_step = current_step

if __name__ == "__main__":
    unittest.main()
