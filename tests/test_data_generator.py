import unittest

from src.data_generator import DataGenerator


class TestDataGenerator(unittest.TestCase):
    def test_data_generation(self):
        graph_path = "input/layouts/expLayout.json"
        people_path = "input/people/expPeople1.json"
        event_path = "input/events/genTestEvents.json"
        gen = DataGenerator(layout_file=graph_path, people_file=people_path, out_file=event_path,
                               plan_starts=[0, 200])
        gen.create_events()

if __name__ == '__main__':
    unittest.main()
