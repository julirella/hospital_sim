import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from src.process_data.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):

    @patch('src.process_data.data_processor.GenImporter')
    @patch('src.process_data.data_processor.pd.read_csv')
    def test_data_processor_patient_time_waiting_per_event(self, mock_read_csv, mock_gen_importer):
        # Mock unused nurse_df
        mock_read_csv.side_effect = [MagicMock(), None]

        # Mock GenImporter
        mock_gen_instance = MagicMock()
        mock_gen_importer.return_value = mock_gen_instance
        mock_gen_instance.nurse_patients = {}
        mock_gen_instance.patient_cnt = 0

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

        processor = DataProcessor('a', 'b', 'c')
        processor.event_df = mock_event_df

        # request lvl 2
        result_level2 = processor.patient_time_waiting_per_event(0, request_level=2)
        self.assertEqual([10], result_level2)

        # request level 1, so we want times lvl 1 requests and plans
        result_level1 = processor.patient_time_waiting_per_event(0, request_level=1)
        result_level1.sort() # don't care about event order
        self.assertEqual([4, 5, 10], list(map(lambda x: int(x), result_level1))) #sometimes it comes back as np.int

        # no request level, so we want waiting times for all events
        result_none = processor.patient_time_waiting_per_event(0, request_level=None)
        result_none.sort()
        self.assertEqual([4, 5, 10, 10], list(map(lambda x: int(x), result_none)))

if __name__ == '__main__':
    unittest.main()
