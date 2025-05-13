import unittest
from unittest.mock import Mock

from src import NurseList, Request
from src.simulation.request_assigner.other_assigner import OtherAssigner


class TestOtherAssigner(unittest.TestCase):
    def setUp(self):
        self.mock_nurse_queues = [Mock(spec=NurseList) for _ in range(5)]
        self.assigner = OtherAssigner(self.mock_nurse_queues)

        self.mock_request = Mock(spec=Request)
        self.mock_patient = Mock()
        self.mock_nurse = Mock()

        self.mock_request.patient = self.mock_patient
        self.mock_patient.nurse = self.mock_nurse
        self.mock_nurse.nurse_id = 2

        for mock_nurse_queue in self.mock_nurse_queues:
            mock_nurse_queue.has_time_now.return_value = False

    def test_assign_request_level_1(self):
        self.mock_request.level = 1
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[2].add_to_gap.assert_called_once_with(self.mock_request)
        self.assertEqual(2, chosen_nurse_id)

    def test_assign_request_level_2_nurse_has_time_now(self):
        self.mock_request.level = 2
        self.mock_nurse_queues[2].has_time_now.return_value = True
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[2].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(2, chosen_nurse_id)


    def test_assign_request_level_2_other_nurse_has_time_now(self):
        self.mock_request.level = 2
        self.mock_nurse_queues[4].has_time_now.return_value = True
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[4].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(4, chosen_nurse_id)

    def test_assign_request_level_2_noone_has_time_now(self):
        self.mock_request.level = 2
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.assertEqual(None, chosen_nurse_id)

    def test_assign_request_level_3_nurse_has_time_now(self):
        self.mock_request.level = 3
        self.mock_nurse_queues[0].has_time_now.return_value = True #different nurse also has time, but patients nurse should be chosen
        self.mock_nurse_queues[2].has_time_now.return_value = True
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[2].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(2, chosen_nurse_id)

    def test_assign_request_level_3_other_has_time_now(self):
        self.mock_request.level = 3
        for queue in self.mock_nurse_queues:
            queue.current_event_level.return_value = 2
        self.mock_nurse_queues[3].has_time_now.return_value = True
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[3].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(3, chosen_nurse_id)

    def test_assign_request_level_3_no_emergency(self):
        self.mock_request.level = 3
        for queue in self.mock_nurse_queues:
            queue.current_event_level.return_value = 2
        self.mock_nurse_queues[1].current_event_level.return_value = 1
        self.mock_nurse_queues[4].current_event_level.return_value = 1
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[1].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(chosen_nurse_id, 1)

    def test_assign_request_level_3_all_emergency(self):
        self.mock_request.level = 3
        for queue in self.mock_nurse_queues:
            queue.current_event_level.return_value = 3
        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.assertIsNone(chosen_nurse_id)

    def test_assign_request_level_3_nurse_among_min(self):
        self.mock_request.level = 3
        self.mock_nurse_queues[0].current_event_level.return_value = 3
        self.mock_nurse_queues[1].current_event_level.return_value = 1
        self.mock_nurse_queues[2].current_event_level.return_value = 1
        self.mock_nurse_queues[3].current_event_level.return_value = 1
        self.mock_nurse_queues[4].current_event_level.return_value = 2

        chosen_nurse_id = self.assigner.assign_request(self.mock_request)
        self.mock_nurse_queues[2].add_to_start.assert_called_once_with(self.mock_request)
        self.assertEqual(chosen_nurse_id, 2)


if __name__ == '__main__':
    unittest.main()
