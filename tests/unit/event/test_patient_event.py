import unittest
from unittest.mock import Mock

from src.event import *


class TestPatientEvent(unittest.TestCase):
    def setUp(self):
        self.mock_patient = Mock()
        self.mock_patient.room = Mock()
        self.mock_graph = Mock()
        self.mock_nurse = Mock()
        self.mock_nurse.get_pos.return_value = Mock()
        self.mock_nurse.speed = 1
        self.mock_sim_time = Mock()
        self.mock_node1 = Mock()
        self.mock_node2 = Mock()
        self.mock_node3 = Mock()
        self.mock_graph.find_path.return_value = [(self.mock_node1, 60), (self.mock_node2, 90), (self.mock_node3, 150)]
        self.event = PatientEvent(time=50, duration=30, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                  graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.mock_move = Movement(0, self.mock_nurse, self.mock_node1, self.mock_node2)
        self.mock_time_at_patient = TimeAtPatient(0, self.mock_nurse, 0)

    def test_run_next_step_creates_steps_of_type(self):
        self.event.run_next_step()
        # print(type(Movement))
        self.assertEqual(type(self.mock_move), type(self.event.get_next_step()))
        self.event.run_next_step()
        self.assertEqual(type(self.mock_move), type(self.event.get_next_step()))
        self.event.run_next_step()
        self.assertEqual(type(self.mock_move), type(self.event.get_next_step()))
        self.event.run_next_step()
        self.assertEqual(type(self.mock_time_at_patient), type(self.event.get_next_step()))

    def test_run_next_step_creates_steps_with_time(self):
        self.event.run_next_step()
        self.assertEqual(110, self.event.next_time())
        self.event.run_next_step()
        self.assertEqual(200, self.event.next_time())
        self.event.run_next_step()
        self.assertEqual(350, self.event.next_time())
        self.event.run_next_step()
        self.assertEqual(380, self.event.next_time())


    def test_first_next_time_returns_event_time(self):
        self.assertEqual(50, self.event.next_time())

    def test_run_next_step_starts_event(self):
        self.event.run_next_step()
        self.assertEqual(EventStatus.ACTIVE, self.event.status)

    def test_run_next_step_finishes_event(self):
        steps_taken = 0
        while not self.event.run_next_step():
            steps_taken += 1
        self.mock_nurse.finish_event.assert_called_once()
        self.assertEqual(4, steps_taken)

    def test_pause_and_restart(self):
        self.event.run_next_step()
        self.event.run_next_step()
        self.event.get_next_step().pause = Mock()
        self.event.get_next_step().pause.return_value = 0

        self.mock_nurse.unassign_event = Mock()
        self.event.pause()
        self.assertEqual(EventStatus.PAUSED, self.event.status)
        self.mock_nurse.unassign_event.assert_called_once()

        self.event.run_next_step()
        self.assertEqual(EventStatus.ACTIVE, self.event.status)

    def test_pause_during_time_at_patient(self):
        self.event.run_next_step()
        self.event.run_next_step()
        self.event.run_next_step()
        self.event.run_next_step()
        self.mock_sim_time.sim_time.return_value = 75
        self.event.get_next_step = Mock()
        self.event.get_next_step().pause.return_value = 15

        self.event.pause()

        self.assertEqual(15, self.event.duration)

if __name__ == "__main__":
    unittest.main()
