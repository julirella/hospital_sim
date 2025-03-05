import unittest
from unittest.mock import Mock

from src import TimeQueue
from src.simulation.timed_object import TimedObject


class TestTimeQueue(unittest.TestCase):
    def setUp(self):
        self.queue = TimeQueue()

        self.event1 = Mock(spec=TimedObject)
        self.event1.time = 10.0

        self.event2 = Mock(spec=TimedObject)
        self.event2.time = 20.0

        self.event3 = Mock(spec=TimedObject)
        self.event3.time = 15.0

        self.event4 = Mock(spec=TimedObject)
        self.event4.time = 15.0

    def test_add_and_top_item(self):
        self.queue.add(self.event1)
        self.assertEqual(self.event1, self.queue.top_item())

    def test_add_and_pop(self):
        self.queue.add(self.event1)
        self.queue.add(self.event2)
        self.assertEqual(self.event1, self.queue.pop())
        self.assertEqual(self.event2, self.queue.pop())

    def test_ordering(self):
        self.queue.add(self.event2)
        self.queue.add(self.event3)
        self.queue.add(self.event1)
        self.queue.add(self.event4)

        self.assertEqual(self.event1, self.queue.pop())
        next_event = self.queue.pop()
        self.assertTrue(next_event == self.event3 or next_event == self.event4)
        next_event = self.queue.pop()
        self.assertTrue(next_event == self.event3 or next_event == self.event4)
        self.assertEqual(self.event2, self.queue.pop())

    def test_next_time(self):
        self.queue.add(self.event1)
        self.queue.add(self.event2)
        self.assertEqual(10.0, self.queue.next_time())

    def test_is_empty(self):
        self.assertTrue(self.queue.empty())
        self.queue.add(self.event1)
        self.assertFalse(self.queue.empty())
        self.queue.pop()
        self.assertTrue(self.queue.empty())

    def test_remove(self):
        self.queue.add(self.event1)
        self.queue.add(self.event2)
        self.queue.remove(self.event1)
        self.assertEqual(self.event2, self.queue.top_item())
        self.queue.remove(self.event2)
        self.assertTrue(self.queue.empty())


if __name__ == "__main__":
    unittest.main()
