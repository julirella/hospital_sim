import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from src.process_data.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):

    @patch('src.process_data.data_processor.GenImporter')
    @patch('src.process_data.data_processor.pd.read_csv')
    def setUp(self, mock_read_csv, mock_gen_importer):


        mock_gen_instance = MagicMock()
        mock_gen_importer.return_value = mock_gen_instance
        mock_gen_instance.nurse_patients = [[0, 1], [2], []]
        mock_gen_instance.patient_cnt = 3

        self.processor = DataProcessor('a', 'b', 'c')

    def test_nurse_time_walked(self):

        data = []
        # event and patient ids are irrelevant
        data.append({'nurse': 0, 'patient': 0, 'action': 'assign event', 'x': 0, 'y': 0, 'time': 0, 'event': 1})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 0, 'y': 0, 'time': 5, 'event': 1})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 3, 'y': 4, 'time': 10, 'event': 2})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 6, 'y': 8, 'time': 20, 'event': 3})
        data.append({'nurse': 0, 'patient': 0, 'action': 'time at patient', 'x': 6, 'y': 8, 'time': 25, 'event': 4})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 9, 'y': 12, 'time': 30, 'event': 5})
        data.append({'nurse': 0, 'patient': 0, 'action': 'time at patient', 'x': 9, 'y': 12, 'time': 35, 'event': 6})
        data.append({'nurse': 0, 'patient': 1, 'action': 'move to', 'x': 10, 'y': 14, 'time': 40, 'event': 7})

        self.nurse_df = pd.DataFrame(data)
        self.processor.nurse_df = self.nurse_df

        self.assertEqual(30, self.processor.nurse_time_walked(0))

    def test_nurse_dst_walked(self):
        data = []
        # event and patient ids are irrelevant
        data.append({'nurse': 0, 'patient': 0, 'action': 'assign event', 'x': 0, 'y': 0, 'time': 0, 'event': 1})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 3, 'y': 4, 'time': 5, 'event': 1})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 6, 'y': 8, 'time': 10, 'event': 2})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 9, 'y': 12, 'time': 20, 'event': 3})
        data.append({'nurse': 0, 'patient': 0, 'action': 'time at patient', 'x': 9, 'y': 12, 'time': 25, 'event': 4})
        data.append({'nurse': 0, 'patient': 0, 'action': 'move to', 'x': 12, 'y': 8, 'time': 30, 'event': 5})
        data.append({'nurse': 0, 'patient': 0, 'action': 'time at patient', 'x': 12, 'y': 8, 'time': 35, 'event': 6})
        data.append({'nurse': 0, 'patient': 1, 'action': 'move to', 'x': 9, 'y': 4, 'time': 40, 'event': 7})

        self.nurse_df = pd.DataFrame(data)
        self.processor.nurse_df = self.nurse_df

        self.assertEqual(25, self.processor.nurse_dst_walked(0))

    def test_nurse_time_at_patient(self):
        self.processor.nurse_df = pd.DataFrame([
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'move to', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'move to', 'time': 5},
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'unassign event', 'time': 10}, #5
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'move to', 'time': 15},
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'assign event', 'time': 20},
            {'nurse': 0, 'patient': 0, 'event': 100, 'action': 'time at patient', 'time': 25}, # 5, with pause
            {'nurse': 0, 'patient': 0, 'event': 20, 'action': 'move to', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 20, 'action': 'move to', 'time': 2},
            {'nurse': 0, 'patient': 0, 'event': 20, 'action': 'move to', 'time': 5},
            {'nurse': 0, 'patient': 0, 'event': 20, 'action': 'time at patient', 'time': 10}, # 5, no pause
            {'nurse': 0, 'patient': 0, 'event': 10, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 10, 'action': 'time at patient', 'time': 10}, # 10, no movement
            {'nurse': 0, 'patient': 0, 'event': 30, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 30, 'action': 'unassign event', 'time': 5}, #5
            {'nurse': 0, 'patient': 0, 'event': 30, 'action': 'move to', 'time': 7},
            {'nurse': 0, 'patient': 0, 'event': 30, 'action': 'move to', 'time': 10},
            {'nurse': 0, 'patient': 0, 'event': 30, 'action': 'time at patient', 'time': 20}, #10, unassign before first
            {'nurse': 0, 'patient': 1, 'event': 10, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 1, 'event': 10, 'action': 'time at patient', 'time': 10},  # wrong patient
            {'nurse': 1, 'patient': 0, 'event': 10, 'action': 'assign event', 'time': 0},
            {'nurse': 1, 'patient': 0, 'event': 10, 'action': 'time at patient', 'time': 10},  # wrong nurse
        ])

        self.assertEqual(40, self.processor.nurse_time_at_patient(nurse_id=0, patient_id=0))

    def test_time_at_specific_patients(self):
        self.processor.nurse_df = pd.DataFrame([
            {'nurse': 0, 'patient': 0, 'event': 0, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 0, 'action': 'time at patient', 'time': 10},
            {'nurse': 0, 'patient': 1, 'event': 1, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 1, 'event': 1, 'action': 'time at patient', 'time': 9},
            {'nurse': 0, 'patient': 2, 'event': 3, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 2, 'event': 3, 'action': 'time at patient', 'time': 8},
            {'nurse': 0, 'patient': 0, 'event': 2, 'action': 'assign event', 'time': 0},
            {'nurse': 0, 'patient': 0, 'event': 2, 'action': 'time at patient', 'time': 7},
        ])

        self.assertEqual(26, self.processor.nurse_time_at_own_patients(0))
        self.assertEqual(8, self.processor.nurse_time_at_other_patients(0))
        self.assertEqual(34, self.processor.nurse_time_at_all_patients(0))


    def test_data_processor_patient_time_waiting_per_event(self):
        data = []

        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 1, 'action': 'planned start', 'time': 10})
        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 1, 'action': 'end', 'time': 15})
        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 5, 'action': 'planned start', 'time': 10})
        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 5, 'action': 'end', 'time': 20})
        data.append({'patient': 0, 'type': 'plan', 'request_level': None, 'event': 2, 'action': 'end', 'time': 12})
        data.append({'patient': 0, 'type': 'plan', 'request_level': None, 'event': 2, 'action': 'planned start', 'time': 8})
        data.append({'patient': 0, 'type': 'request', 'request_level': 2, 'event': 3, 'action': 'planned start', 'time': 20})
        data.append({'patient': 0, 'type': 'request', 'request_level': 2, 'event': 3, 'action': 'actual start', 'time': 25})
        data.append({'patient': 0, 'type': 'request', 'request_level': 2, 'event': 3, 'action': 'end', 'time': 30})
        data.append({'patient': 1, 'type': 'request', 'request_level': 2, 'event': 3, 'action': 'actual start', 'time': 30})
        data.append({'patient': 1, 'type': 'request', 'request_level': 2, 'event': 3, 'action': 'end', 'time': 40})
        data.append({'patient': 0, 'type': 'return to office', 'request_level': 1, 'event': 1, 'action': 'planned start', 'time': 10})
        data.append({'patient': 0, 'type': 'return to office', 'request_level': 1, 'event': 1, 'action': 'end', 'time': 15})

        mock_event_df = pd.DataFrame(data)

        self.processor.event_df = mock_event_df

        # request lvl 2
        result_level2 = self.processor.patient_time_waiting_per_event(0, request_level=2)
        self.assertEqual([10], result_level2)

        # request level 1, so we want times lvl 1 requests and plans
        result_level1 = self.processor.patient_time_waiting_per_event(0, request_level=1)
        result_level1.sort() # don't care about event order
        self.assertEqual([4, 5, 10], list(map(lambda x: int(x), result_level1))) #sometimes it comes back as np.int

        # no request level, so we want waiting times for all events
        result_none = self.processor.patient_time_waiting_per_event(0, request_level=None)
        result_none.sort()
        self.assertEqual([4, 5, 10, 10], list(map(lambda x: int(x), result_none)))
        self.assertEqual(29, self.processor.patient_total_time_waiting(0, request_level=None))
        self.assertEqual(29 / 4, self.processor.patient_avg_time_waiting(0, request_level=None))

    def test_patient_wait_time_no_value_in_df(self):
        data = []

        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 1, 'action': 'planned start', 'time': 10})
        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 1, 'action': 'end', 'time': 15})
        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 5, 'action': 'planned start', 'time': 10})
        data.append({'patient': 0, 'type': 'request', 'request_level': 1, 'event': 5, 'action': 'end', 'time': 20})
        data.append({'patient': 0, 'type': 'plan', 'request_level': None, 'event': 2, 'action': 'end', 'time': 12})
        data.append({'patient': 0, 'type': 'plan', 'request_level': None, 'event': 2, 'action': 'planned start', 'time': 8})
        mock_event_df = pd.DataFrame(data)

        result_level3 = self.processor.patient_time_waiting_per_event(0, request_level=3)
        self.assertEqual([], result_level3)
        self.assertEqual(0, self.processor.patient_total_time_waiting(0, request_level=3))
        self.assertEqual(0, self.processor.patient_avg_time_waiting(0, request_level=3))

        # print(result_level3)

if __name__ == '__main__':
    unittest.main()
