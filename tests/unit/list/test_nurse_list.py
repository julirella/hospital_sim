import unittest
from unittest.mock import Mock, PropertyMock, patch

from src.event import Event, EventStatus
from src.queue import NurseList


class TestNurseList(unittest.TestCase):
    def setUp(self):
        print("setup called")
        self.mock_patient = Mock()
        self.mock_nurse = Mock()
        self.mock_nurse.speed = 1
        self.mock_graph = Mock()
        # self.mock_graph.max_graph_dst().return_value = 20
        self.mock_sim_time = Mock()
        self.mock_sim_time.sim_time = 0

        self.event1 = Event(event_id=0, time=40, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event2 = Event(event_id=0, time=90, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event3 = Event(event_id=0, time=170, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.nurse_list = NurseList([self.event3, self.event1, self.event2], self.mock_sim_time, self.mock_nurse, 20)

    def test_init(self):
        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())

    def test_add_to_gap_front(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                            graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(new_event, self.nurse_list.front())
        self.assertEqual(0, new_event.time)

    def test_add_to_gap_middle(self):
        new_event = Event(event_id=0, time=0, duration=25, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())
        self.assertEqual(120, new_event.time)

    def test_add_to_gap_end(self):
        new_event = Event(event_id=0, time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(200, new_event.time)

    def test_add_after_current_first(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)

       # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock
        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.NOT_STARTED):
            self.nurse_list.add_after_current(new_event)

        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(0, new_event.time)
        self.assertEqual(40, self.event1.time)

    def test_add_after_current_second(self):
        new_event = Event(event_id=0, time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)

        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.nurse_list.add_after_current(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(70, new_event.time)
        self.assertEqual(95, self.event2.time)
        self.assertEqual(170, self.event3.time)

    def test_add_after_current_pushback_all(self):
        new_event = Event(event_id=0, time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)

        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.nurse_list.add_after_current(new_event)

        self.assertEqual(40, self.nurse_list.pop_front().time)
        self.assertEqual(70, self.nurse_list.pop_front().time)
        self.assertEqual(190, self.nurse_list.pop_front().time)
        self.assertEqual(220, self.nurse_list.pop_front().time)

    def test_add_to_start_no_pause(self):
        new_event = Event(event_id=0, time=0, duration=35, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        # self.event1.get_status = Mock(return_value=EventStatus.ACTIVE)
        self.nurse_list.add_to_start(new_event)

        self.assertEqual(0, self.nurse_list.pop_front().time)
        self.assertEqual(55, self.nurse_list.pop_front().time)
        self.assertEqual(90, self.nurse_list.pop_front().time)
        self.assertEqual(170, self.nurse_list.pop_front().time)

        self.assertEqual(EventStatus.NOT_STARTED, self.event1.status)

    def test_add_to_start_pause(self):
        new_event = Event(event_id=0, time=0, duration=45, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.event1.pause = Mock()
        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.nurse_list.add_to_start(new_event)

        self.event1.pause.assert_called_once()

if __name__ == "__main__":
    unittest.main()

