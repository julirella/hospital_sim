import unittest
from unittest.mock import Mock

from src import EventList
from src.simulation.timed_object import PatientEvent



class TestEventList(unittest.TestCase):
    def setUp(self):
        # Create mock events for testing
        self.mock_event1 = Mock(spec=PatientEvent)
        self.mock_event1.time = 10.0
        self.mock_event1.next_time.return_value = 15.0

        self.mock_event2 = Mock(spec=PatientEvent)
        self.mock_event2.time = 20.0
        self.mock_event2.next_time.return_value = 25.0

        self.mock_event3 = Mock(spec=PatientEvent)
        self.mock_event3.time = 30.0
        self.mock_event3.next_time.return_value = 35.0

    def test_init_empty_list(self):
        event_list = EventList([])
        self.assertTrue(event_list.empty())
        self.assertIsNone(event_list.front())

    def test_init_single_event(self):
        event_list = EventList([self.mock_event1])
        self.assertFalse(event_list.empty())
        self.assertEqual(event_list.front(), self.mock_event1)

    def test_init_multiple_events_sorted(self):
        # Create events in unsorted order
        events = [self.mock_event2, self.mock_event1, self.mock_event3]
        event_list = EventList(events)

        # Check if events are sorted by time
        self.assertEqual(event_list.front(), self.mock_event1)
        event_list.pop_front()
        self.assertEqual(event_list.front(), self.mock_event2)
        event_list.pop_front()
        self.assertEqual(event_list.front(), self.mock_event3)

    def test_empty(self):
        event_list = EventList([])
        self.assertTrue(event_list.empty())

        event_list = EventList([self.mock_event1])
        self.assertFalse(event_list.empty())

    def test_front(self):
        event_list = EventList([self.mock_event1, self.mock_event2])
        self.assertEqual(event_list.front(), self.mock_event1)

    def test_pop_front(self):
        event_list = EventList([self.mock_event1, self.mock_event2])

        # First pop
        popped_event = event_list.pop_front()
        self.assertEqual(popped_event, self.mock_event1)
        self.assertEqual(event_list.front(), self.mock_event2)

        # Second pop
        popped_event = event_list.pop_front()
        self.assertEqual(popped_event, self.mock_event2)
        self.assertTrue(event_list.empty())

        # Pop from empty list
        popped_event = event_list.pop_front()
        self.assertIsNone(popped_event)

    def test_next_time(self):
        # Test with empty list
        event_list = EventList([])
        self.assertIsNone(event_list.next_time())

        # Test with non-empty list
        event_list = EventList([self.mock_event1])
        self.assertEqual(event_list.next_time(), 15.0)


if __name__ == '__main__':
    unittest.main()