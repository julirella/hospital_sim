import math
import unittest
from unittest.mock import Mock

from src import Nurse, Node
from src.event import Movement

class TestMovement(unittest.TestCase):
    def setUp(self):
        self.nurse_pos = Node(0, 0, 0)
        self.sim_time = Mock()
        self.nurse = Nurse(0, self.nurse_pos, self.sim_time)

    def test_run(self):
        new_pos = Mock()
        move = Movement(100, self.nurse, self.nurse_pos, new_pos)
        move.run()
        self.assertEqual(new_pos, self.nurse.pos)

    def test_pause_forward(self):
        start = Node(0, 0, 0)
        end = Node(0, 3, 4)
        move = Movement(100, self.nurse, start, end)
        move.pause(100 - 2.5 / self.nurse.speed)
        x = self.nurse.pos.x
        y = self.nurse.pos.y
        self.assertTrue(0.000001 > abs(x - 1.5))
        self.assertTrue(0.000001 > abs(y - 2.0))

    def test_pause_backward(self):
        start = Node(0, 120, 60)
        end = Node(0, 0, 0)
        move = Movement(100, self.nurse, start, end)
        move.pause(100 - (math.sqrt(5) * 40) / self.nurse.speed)
        x = self.nurse.pos.x
        y = self.nurse.pos.y
        self.assertTrue(0.000001 > abs(x - 80.0))
        self.assertTrue(0.000001 > abs(y - 40.0))

if __name__ == '__main__':
    unittest.main()
