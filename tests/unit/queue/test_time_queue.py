import unittest
from unittest.mock import Mock

from src import TimeQueue
from src.event import TimedOccurrence


class TestTimeQueue(unittest.TestCase):
    def setUp(self):
        self.queue = TimeQueue()

        self.event1 = Mock(spec=TimedOccurrence)
        self.event1.time = 10.0

        self.event2 = Mock(spec=TimedOccurrence)
        self.event2.time = 20.0

        self.event3 = Mock(spec=TimedOccurrence)
        self.event3.time = 15.0

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
        self.assertEqual(self.event1, self.queue.pop())
        self.assertEqual(self.event3, self.queue.pop())
        self.assertEqual(self.event2, self.queue.pop())

    def test_next_time(self):
        self.queue.add(self.event1)
        self.queue.add(self.event2)
        self.assertEqual(10.0, self.queue.next_time())

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.add(self.event1)
        self.assertFalse(self.queue.is_empty())
        self.queue.pop()
        self.assertTrue(self.queue.is_empty())

    def test_remove(self):
        self.queue.add(self.event1)
        self.queue.add(self.event2)
        self.queue.remove(self.event1)
        self.assertEqual(self.event2, self.queue.top_item())


if __name__ == "__main__":
    unittest.main()
