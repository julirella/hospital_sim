import unittest
from unittest.mock import Mock

from src import Nurse


class TestNurse(unittest.TestCase):
    def setUp(self):
        self.mock_node = Mock()
        self.mock_node.node_id = 1
        self.mock_sim_time = Mock()
        self.mock_sim_time.get_sim_time.return_value = 100
        self.nurse = Nurse(nurse_id=1, pos=self.mock_node, sim_time=self.mock_sim_time)

    def test_assign_event(self):
        self.nurse.assign_event(10, 0)
        self.assertEqual(self.nurse.get_pos(), self.mock_node)  # Position should not change
        log = self.nurse.get_log()
        self.assertEqual(log[-1]["time"], 100)
        self.assertEqual(log[-1]["position"], self.mock_node.node_id)
        self.assertEqual(log[-1]["event"], 10)
        self.assertEqual(log[-1]["action"], "assign event")

    def test_finish_event(self):
        self.nurse.finish_event()
        self.assertEqual(self.nurse.get_pos(), self.mock_node)  # Position should remain unchanged
        log = self.nurse.get_log()
        self.assertEqual(log[-1]["time"], 100)
        self.assertEqual(log[-1]["position"], self.mock_node.node_id)
        self.assertIsNone(log[-1]["event"])
        self.assertEqual(log[-1]["action"], "finish event")

    def test_move(self):
        new_node = Mock()
        new_node.node_id = 2
        self.nurse.move(new_node)
        self.assertEqual(self.nurse.get_pos(), new_node)
        log = self.nurse.get_log()
        self.assertEqual(log[-1]["time"], 100)
        self.assertEqual(log[-1]["position"], 2)
        self.assertEqual(log[-1]["event"], None)
        self.assertEqual(log[-1]["action"], "move to")

if __name__ == "__main__":
    unittest.main()
