import unittest
import pandas as pd
import json
import itertools

from src import Simulator
from src.exporter.log_exporter import LogExporter
from src.importer import SimImporter
from src.main import App
from src.process_data import DataProcessor
from src.simulation.timed_object import Event


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        self.people_path = "input/people/testPeople2.json"
        self.test_event_output = "output/testEventLog.csv"
        self.test_nurse_output = "output/testNurseLog.csv"

        # reset id generation between test so that event ids can be tested
        Event._id_generator = itertools.count(0)

    def run_sim(self, event_path, graph_path=None, people_path=None):
        if graph_path is None:
            graph_path = self.graph_path
        if people_path is None:
            people_path = self.people_path
        importer = SimImporter(graph_path, people_path, event_path)
        sim = importer.import_data()
        sim.simulate()
        return sim

    def export_logs(self, sim: Simulator):
        log_exporter = LogExporter(sim, self.test_nurse_output, self.test_event_output)
        log_exporter.export_data()
        self.nurse_df = pd.read_csv("output/testNurseLog.csv")
        self.event_df = pd.read_csv("output/testEventLog.csv")

    def check_nurse_conditions(self, conditions) -> bool:
        result = True
        for condition in conditions:
            result &= (self.nurse_df[condition[0]] == condition[1])

        return result.any()

    def check_event_conditions(self, conditions) -> bool:
        result = True
        for condition in conditions:
            result &= (self.event_df[condition[0]] == condition[1])

        return result.any()

    # ---------- BASIC ASSIGNER TESTS ----------
    def test_sim_plans_only(self):
        event_path = "input/events/testEvents2.json"
        self.run_sim(event_path=event_path)
        # importer = SimImporter(self.graph_path, self.people_path, event_path)
        # sim = importer.import_data()
        # sim.simulate()

    def test_sim_plans_and_requests(self):
        event_path = "input/events/testEventsRequests.json"
        self.run_sim(event_path=event_path)
        # importer = SimImporter(self.graph_path, self.people_path, event_path)
        # sim = importer.import_data()
        # sim.simulate()

    def test_sim_many_people(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/testEventsRequests.json"

        self.run_sim(event_path=event_path, graph_path=graph_path, people_path=people_path)

    def test_sim_uninterrupted_event(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/oneEvent.json"

        sim = self.run_sim(event_path=event_path, graph_path=graph_path, people_path=people_path)
        self.export_logs(sim=sim)

        conditions = (('x', 9), ('y', 17), ('time', 5), ('action', 'assign event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('x', 6), ('y', 3), ('time', 22), ('action', 'move to'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('x', 3), ('y', 3), ('time', 45), ('action', 'time at patient'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('x', 3), ('y', 3), ('time', 45), ('action', 'finish event'))
        self.assertTrue(self.check_nurse_conditions(conditions))

        #return to office
        conditions = (('x', 9), ('y', 17), ('time', 65), ('action', 'move to'))
        self.assertTrue(self.check_nurse_conditions(conditions))

        #only nurse 0 did something
        active_nurses = self.nurse_df['nurse'].unique()
        self.assertEqual(1, len(active_nurses))
        self.assertEqual(0, active_nurses[0])

    def test_two_nurses_alternating(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/twoNurses.json"

        sim = self.run_sim(event_path=event_path, graph_path=graph_path, people_path=people_path)
        self.export_logs(sim=sim)

        #nurses both do work that overlaps timewise and don't interfere with each other
        #nurse 0 has time to return to office, nurse 1 doesn't
        conditions = (('nurse', 0), ('x', 9), ('y', 17), ('time', 5), ('action', 'assign event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 0), ('x', 9), ('y', 17), ('time', 90), ('action', 'assign event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('x', 9), ('y', 17), ('time', 10), ('action', 'assign event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('x', 3), ('y', 8), ('time', 70), ('action', 'assign event'))
        self.assertTrue(self.check_nurse_conditions(conditions))

        conditions = (('nurse', 0), ('x', 3), ('y', 3), ('time', 45), ('action', 'finish event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 0), ('x', 3), ('y', 3), ('time', 130), ('action', 'finish event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('x', 3), ('y', 8), ('time', 45), ('action', 'finish event'))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('x', 3), ('y', 8), ('time', 90), ('action', 'finish event'))
        self.assertTrue(self.check_nurse_conditions(conditions))

    # def test_sim_basic_patients_nurse_always_chosen(self):
    #     graph_path = "input/layouts/toScaleLayout.json"
    #     people_path = "input/people/manyPeople.json"
    #     event_path = "input/events/testEventsRequests.json"
    #
    #     sim = self.run_sim(event_path=event_path, graph_path=graph_path, people_path=people_path)
    #     self.export_logs(sim=sim)
    #
    def test_sim_basic_event_ordering(self):
        # events should be run in correct order, requests should not reorder plans
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/reqReorder.json"

        sim = self.run_sim(event_path=event_path, graph_path=graph_path, people_path=people_path)
        self.export_logs(sim=sim)

        df2 = self.event_df[self.event_df.action == "actual start"]
        df3 = df2.sort_values(by=['time'])
        res_event_order = df3.event.to_list()

        self.assertEqual([3,1,2,4,0,5], res_event_order)

    # ---------- OTHER ASSIGNER TESTS ----------
    def test_sim_other_all_queues(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/twoPatients.json"
        event_path = "input/events/allQueues.json"

        app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)

        app.run_simulation()
        self.nurse_df = pd.read_csv("output/testNurseLog.csv")
        self.event_df = pd.read_csv("output/testEventLog.csv")

        # nurse 0 only does her three plans
        conditions = (('nurse', 0), ('x', 9), ('y', 17), ('time', 0), ('action', 'assign event'), ('event', 2))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 0), ('x', 3), ('y', 3), ('time', 35), ('action', 'finish event'), ('event', 2))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 0), ('time', 50), ('action', 'assign event'), ('event', 3))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 0), ('time', 100), ('action', 'assign event'), ('event', 4))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 0), ('x', 3), ('y', 3), ('time', 120), ('action', 'finish event'), ('event', 4))
        self.assertTrue(self.check_nurse_conditions(conditions))

        # nurse 1 should do two requests when they have time
        conditions = (('nurse', 1), ('x', 9), ('y', 17), ('time', 0), ('action', 'assign event'), ('event', 5))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('time', 40), ('action', 'assign event'), ('event', 0))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('time', 60), ('action', 'assign event'), ('event', 1))
        self.assertTrue(self.check_nurse_conditions(conditions))
        conditions = (('nurse', 1), ('time', 100), ('action', 'assign event'), ('event', 6))
        self.assertTrue(self.check_nurse_conditions(conditions))

        # plans should go at planned times
        conditions = (('time', 0), ('event', 2), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))
        conditions = (('time', 50), ('event', 3), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))
        conditions = (('time', 100), ('event', 4), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))
        conditions = (('time', 0), ('event', 5), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))
        conditions = (('time', 100), ('event', 6), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))

        #requests are lvl 2 so should be kept in waiting queue until nurse 1 has time for them
        conditions = (('time', 40), ('event', 0), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))
        conditions = (('time', 60), ('event', 1), ('action', 'actual start'))
        self.assertTrue(self.check_event_conditions(conditions))

    # ---------- TESTING IT DOESN'T CRASH ON RANDOM DATA ----------
    def test_sim_other_assigner(self):
        #TODO: something weird is going on with displayed request numbers
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/testEventsRequestsOther.json"
        app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)

        app.run_simulation(visualise=False)

    def test_sim_other_assigner_exp2(self):
        graph_path = "input/layouts/expLayout.json"
        people_path = "input/people/expPeople1.json"
        event_path = "input/events/expEvents2.json"
        app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)

        app.run_simulation()

    def test_sim_exp5(self):
        graph_path = "input/layouts/expLayout.json"
        people_path = "input/people/expPeople1.json"
        event_path = "input/events/expEvents5.json"
        app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)

        app.run_simulation()


    # ---------- COMPARISON TESTS ----------
    def test_sim_assigner_comparison_one_nurse(self):
        #one nurse should spend the same amount of time at patients with both assigners
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/oneNurse.json"
        basic_event_path = "input/events/basic1nurse.json"
        other_event_path = "input/events/other1nurse.json"

        app = App(graph_path=graph_path, people_path=people_path, event_path=basic_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output, people_path=people_path)
        basic_time_at_patients = dp.nurse_time_at_all_patients(0)

        app = App(graph_path=graph_path, people_path=people_path, event_path=other_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output,
                           people_path=people_path)
        other_time_at_patients = dp.nurse_time_at_all_patients(0)

        self.assertEqual(basic_time_at_patients, other_time_at_patients)

    def test_sim_assigner_comparison_two_nurse(self):
        #total time spent at patients across all nurses should be the same for both assigners
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/twoNurses.json"
        basic_event_path = "input/events/basic2nurses.json"
        other_event_path = "input/events/other2nurses.json"

        app = App(graph_path=graph_path, people_path=people_path, event_path=basic_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output, people_path=people_path)
        basic_time_at_patients = dp.nurse_time_at_all_patients(0) + dp.nurse_time_at_all_patients(1)

        app = App(graph_path=graph_path, people_path=people_path, event_path=other_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output,
                           people_path=people_path)
        other_time_at_patients = dp.nurse_time_at_all_patients(0) + dp.nurse_time_at_all_patients(1)

        self.assertEqual(basic_time_at_patients, other_time_at_patients)

    def test_sim_assigner_comparison_exp3_and_4(self):
        # one nurse should spend the same amount of time at patients with both assigners
        graph_path = "input/layouts/expLayout.json"
        people_path = "input/people/expOneNurse.json"
        basic_event_path = "input/events/expEvents3.json"
        other_event_path = "input/events/expEvents4.json"

        # fieldnames = ['event', 'time']
        # file1 = open('tmp/basic.csv', 'w', newline='')
        # file2 = open('tmp/other.csv', 'w', newline='')
        #
        # writer1 = csv.DictWriter(file1, fieldnames=fieldnames)
        # writer1.writeheader()
        # writer2 = csv.DictWriter(file2, fieldnames=fieldnames)
        # writer2.writeheader()

        app = App(graph_path=graph_path, people_path=people_path, event_path=basic_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output,
                           people_path=people_path)
        # basic_time_at_patients = dp.nurse_time_at_all_patients(0, writer1)
        basic_time_at_patients = dp.nurse_time_at_all_patients(0)

        app = App(graph_path=graph_path, people_path=people_path, event_path=other_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output,
                           people_path=people_path)
        # other_time_at_patients = dp.nurse_time_at_all_patients(0, writer2)
        other_time_at_patients = dp.nurse_time_at_all_patients(0)

        # self.assertEqual(basic_time_at_patients, other_time_at_patients)
        self.assertTrue(abs(basic_time_at_patients - other_time_at_patients) < 0.00001)

    def total_event_duration(self, event_path):
        event_file = open(event_path)
        events_json = json.load(event_file)
        event_file.close()

        reqs = events_json['requests']
        plans = events_json['plans']

        total_duration = 0
        for event in plans + reqs:
            total_duration += event['duration']

        return total_duration

    def compare_total_event_durations(self, graph_path, people_path, event_path, nurse_cnt):
        app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()

        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output,
                           people_path=people_path)

        actual_total_duration = 0
        for nurse_id in range(nurse_cnt):
            actual_total_duration += dp.nurse_time_at_all_patients(nurse_id)

        expected_total_duration = self.total_event_duration(event_path)

        self.assertTrue(abs(expected_total_duration - actual_total_duration) < 0.00001)

    def test_sim_time_at_patients_equals_event_duration_basic(self):
        graph_path = "input/layouts/expLayout.json"
        people_path = "input/people/expPeople1.json"
        event_path = "input/events/expEvents1.json"

        self.compare_total_event_durations(graph_path, people_path, event_path, 2)

    def test_sim_time_at_patients_equals_event_duration_other(self):
        graph_path = "input/layouts/expLayout.json"
        people_path = "input/people/expPeople1.json"
        event_path = "input/events/expEvents2.json"

        self.compare_total_event_durations(graph_path, people_path, event_path, 2)


if __name__ == '__main__':
    unittest.main()
