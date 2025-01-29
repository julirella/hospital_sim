import unittest
from unittest.mock import Mock

from src.event import Event, EventStatus
from src.queue import NurseList


class TestNurseList(unittest.TestCase):
    def setUp(self):
        self.mock_patient = Mock()
        self.mock_nurse = Mock()
        self.mock_graph = Mock()
        self.mock_sim_time = Mock()
        self.mock_sim_time.get_sim_time.return_value = 0

        self.event1 = Event(event_id=0, time=40, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event2 = Event(event_id=0, time=90, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event3 = Event(event_id=0, time=150, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.nurse_list = NurseList([self.event3, self.event1, self.event2], self.mock_sim_time)

    def test_init(self):
        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(self.nurse_list.pop(), self.event3)

    def test_add_to_gap_front(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.nurse_list.top(), new_event)
        self.assertEqual(new_event.get_time(), 0)

    def test_add_to_gap_middle(self):
        new_event = Event(event_id=0, time=0, duration=15, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), new_event)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(new_event.get_time(), 65)

    def test_add_to_gap_end(self):
        new_event = Event(event_id=0, time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(self.nurse_list.pop(), self.event3)
        self.assertEqual(self.nurse_list.pop(), new_event)
        self.assertEqual(new_event.get_time(), 260)

    def test_add_after_current_first(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.NOT_STARTED)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(self.nurse_list.pop(), new_event)
        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(new_event.get_time(), 0)

    def test_add_after_current_second(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.ACTIVE)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), new_event)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(new_event.get_time(), 55)

    def test_add_after_current_pushback_one(self):
        new_event = Event(event_id=0, time=0, duration=25, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.NOT_STARTED)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(0, self.nurse_list.pop().get_time())
        self.assertEqual(45, self.nurse_list.pop().get_time())
        self.assertEqual(90, self.nurse_list.pop().get_time())
        self.assertEqual(150, self.nurse_list.pop().get_time())

if __name__ == "__main__":
    unittest.main()

