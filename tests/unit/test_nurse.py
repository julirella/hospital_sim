import unittest
from unittest.mock import Mock

from src import Nurse


class TestNurse(unittest.TestCase):
    def setUp(self):
        self.mock_node = Mock()
        self.mock_node.node_id = 1
        self.mock_node.x = 3
        self.mock_node.y = 4
        self.mock_sim_time = Mock()
        self.mock_sim_time.sim_time = 100
        self.nurse = Nurse(nurse_id=1, pos=self.mock_node, sim_time=self.mock_sim_time)

    def test_assign_event(self):
        self.nurse.assign_event(10, 0)
        self.assertEqual(self.nurse.pos, self.mock_node)

        log = self.nurse.log
        self.assertEqual(100, log[-1]["time"])
        self.assertEqual(1, log[-1]["nurse"])
        self.assertEqual(3, log[-1]["x"])
        self.assertEqual(4, log[-1]["y"])
        self.assertEqual(10, log[-1]["event"])
        self.assertEqual("assign event", log[-1]["action"])
        self.assertEqual(0, log[-1]["patient"])

    def test_unassign_event(self):
        self.nurse.assign_event(10, 0)
        self.nurse.unassign_event()

        log = self.nurse.log
        self.assertEqual(100, log[-1]["time"])
        self.assertEqual(1, log[-1]["nurse"])
        self.assertEqual(3, log[-1]["x"])
        self.assertEqual(4, log[-1]["y"])
        self.assertEqual(10, log[-1]["event"])
        self.assertEqual("unassign event", log[-1]["action"])
        self.assertEqual(0, log[-1]["patient"])

    def test_finish_event(self):
        self.nurse.assign_event(10, 0)
        self.nurse.finish_event()
        self.assertEqual(self.nurse.pos, self.mock_node)

        log = self.nurse.log
        self.assertEqual(100, log[-1]["time"])
        self.assertEqual(1, log[-1]["nurse"])
        self.assertEqual(3, log[-1]["x"])
        self.assertEqual(4, log[-1]["y"])
        self.assertEqual(10, log[-1]["event"])
        self.assertEqual("finish event", log[-1]["action"])
        self.assertEqual(0, log[-1]["patient"])

    def test_time_at_patient(self):
        self.nurse.time_at_patient()
        self.assertEqual(self.nurse.pos, self.mock_node)

        log = self.nurse.log
        self.assertEqual("time at patient", log[-1]["action"])

    def test_move(self):
        new_node = Mock()
        new_node.node_id = 2
        new_node.x = 5
        new_node.y = 6

        self.nurse.move(new_node)
        self.assertEqual(self.nurse.pos, new_node)

        log = self.nurse.log
        self.assertEqual(100, log[-1]["time"])
        self.assertEqual(1, log[-1]["nurse"])
        self.assertEqual(5, log[-1]["x"])
        self.assertEqual(6, log[-1]["y"])
        self.assertEqual(None, log[-1]["event"])
        self.assertEqual("move to", log[-1]["action"])
        self.assertEqual(None, log[-1]["patient"])

    def test_assign_and_unassign(self):
        new_node = Mock()

        self.nurse.assign_event(10, 0)
        self.nurse.unassign_event()
        self.nurse.move(new_node)

        log = self.nurse.log
        self.assertEqual(10, log[0]["event"])
        self.assertEqual(10, log[1]["event"])
        self.assertEqual(None, log[2]["event"])
        self.assertEqual(0, log[0]["patient"])
        self.assertEqual(0, log[1]["patient"])
        self.assertEqual(None, log[2]["patient"])


if __name__ == "__main__":
    unittest.main()
