import unittest
from unittest.mock import Mock

from src.simulation.event import ReturnToOffice, Movement


class TestReturnToOffice(unittest.TestCase):
    def setUp(self):
        self.mock_sim_time = Mock()
        self.mock_sim_time.sim_time = 50

        self.mock_nurse = Mock()
        self.mock_nurse.speed = 1
        self.mock_nurse.get_pos.return_value = Mock()

        self.mock_graph = Mock()
        self.mock_graph.nurse_office = Mock()

        self.mock_node1 = Mock()
        self.mock_node2 = Mock()
        self.mock_node3 = Mock()
        self.mock_graph.find_path.return_value = [(self.mock_node1, 60), (self.mock_node2, 90), (self.mock_node3, 150)]

        self.event = ReturnToOffice(assigned_nurse=self.mock_nurse, graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.mock_move = Movement(0, self.mock_nurse, self.mock_node1, self.mock_node2)


    def test_run_next_step_creates_movement_steps(self):
        self.event.run_next_step()
        self.assertEqual(type(self.mock_move), type(self.event.get_next_step()))
        self.event.run_next_step()
        self.assertEqual(type(self.mock_move), type(self.event.get_next_step()))
        finished = self.event.run_next_step()
        self.assertEqual(type(self.mock_move), type(self.event.get_next_step()))
        self.assertEqual(False, finished)
        finished = self.event.run_next_step()
        self.assertEqual(True, finished)



if __name__ == '__main__':
    unittest.main()
