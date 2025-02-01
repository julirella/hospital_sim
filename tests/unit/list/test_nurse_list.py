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
        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())

    def test_add_to_gap_front(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(new_event, self.nurse_list.front())
        self.assertEqual(15, new_event.time())

    def test_add_to_gap_middle(self):
        new_event = Event(event_id=0, time=0, duration=15, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(65, new_event.time())

    def test_add_to_gap_end(self):
        new_event = Event(event_id=0, time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(260, new_event.time())

    def test_add_after_current_first(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.NOT_STARTED)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(15, new_event.time())

    def test_add_after_current_second(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.ACTIVE)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(55, new_event.time())

    def test_add_after_current_pushback_one(self):
        new_event = Event(event_id=0, time=0, duration=25, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.NOT_STARTED)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(35, self.nurse_list.pop_front().time())
        self.assertEqual(55, self.nurse_list.pop_front().time())
        self.assertEqual(90, self.nurse_list.pop_front().time())
        self.assertEqual(150, self.nurse_list.pop_front().time())

    def test_add_after_current_pushback_all(self):
        new_event = Event(event_id=0, time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event1.get_status = Mock(return_value=EventStatus.ACTIVE)
        self.nurse_list.add_after_current(new_event)

        self.assertEqual(40, self.nurse_list.pop_front().time())
        self.assertEqual(150, self.nurse_list.pop_front().time())
        self.assertEqual(170, self.nurse_list.pop_front().time())
        self.assertEqual(190, self.nurse_list.pop_front().time())

if __name__ == "__main__":
    unittest.main()

