import unittest
from unittest.mock import Mock
from src.queue import NurseList, ListEvent


class TestNurseList(unittest.TestCase):
    def setUp(self):
        self.mock_sim_time = Mock()
        self.mock_sim_time.get_sim_time.return_value = 0

        self.event1 = Mock()
        self.event1.start_time.return_value = 30
        self.event1.get_time.return_value = 40
        self.event1.get_duration.return_value = 10

        self.event2 = Mock()
        self.event2.start_time.return_value = 80
        self.event2.get_time.return_value = 90
        self.event2.get_duration.return_value = 10

        self.event3 = Mock()
        self.event3.start_time.return_value = 140
        self.event3.get_time.return_value = 150
        self.event3.get_duration.return_value = 10

        self.nurse_list = NurseList([self.event3, self.event1, self.event2], self.mock_sim_time)

    def test_init(self):
        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(self.nurse_list.pop(), self.event3)

    def test_add_to_gap_front(self):
        new_event = Mock()
        new_event.get_duration.return_value = 5
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.nurse_list.top(), new_event)
        new_event.set_time.assert_called_with(0)

    def test_add_to_gap_middle(self):
        new_event = Mock()
        new_event.get_duration.return_value = 15
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), new_event)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        new_event.set_time.assert_called_with(65)


    def test_add_to_gap_end(self):
        new_event = Mock()
        new_event.get_duration.return_value = 100
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.nurse_list.pop(), self.event1)
        self.assertEqual(self.nurse_list.pop(), self.event2)
        self.assertEqual(self.nurse_list.pop(), self.event3)
        self.assertEqual(self.nurse_list.pop(), new_event)
        new_event.set_time.assert_called_with(260)


if __name__ == "__main__":
    unittest.main()

