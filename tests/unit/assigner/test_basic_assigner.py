import unittest
from unittest.mock import Mock

from src import NurseList, Request
from src.request_assigner import BasicAssigner


class TestBasicAssigner(unittest.TestCase):
    def setUp(self):
        self.mock_nurse_queues = [Mock(spec=NurseList) for _ in range(5)]
        self.assigner = BasicAssigner(self.mock_nurse_queues)

        self.mock_request = Mock(spec=Request)
        self.mock_patient = Mock()
        self.mock_nurse = Mock()

        self.mock_request.patient = self.mock_patient
        self.mock_patient.nurse = self.mock_nurse
        self.mock_nurse.nurse_id = 2
        self.mock_request.assign_nurse = Mock()

    def test_assign_request_level_1(self):
        self.mock_request.level = 1
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_request.assign_nurse.assert_called_once_with(self.mock_nurse)
        self.mock_nurse_queues[2].add_to_gap.assert_called_once_with(self.mock_request)
        self.assertEqual(chosen_nurse_id, 2)

    def test_assign_request_level_2(self):
        self.mock_request.level = 2
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_request.assign_nurse.assert_called_once_with(self.mock_nurse)
        self.mock_nurse_queues[2].add_after_current.assert_called_once_with(self.mock_request)
        self.assertEqual(chosen_nurse_id, 2)

    def test_assign_request_level_3(self):
        self.mock_request.level = 3
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_request.assign_nurse.assert_called_once_with(self.mock_nurse)
        self.mock_nurse_queues[2].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(chosen_nurse_id, 2)


if __name__ == "__main__":
    unittest.main()
