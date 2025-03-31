import unittest
import pandas as pd

from src import Simulator
from src.exporter.log_exporter import LogExporter
from src.importer import SimImporter
from src.main import App
from src.process_data import DataProcessor


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.graph_path = "input/layouts/testLayout2.json"
        self.people_path = "input/people/testPeople2.json"
        self.test_event_output = "output/testEventLog.csv"
        self.test_nurse_output = "output/testNurseLog.csv"

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

    def check_conditions(self, conditions) -> bool:
        result = True
        for condition in conditions:
            result &= (self.nurse_df[condition[0]] == condition[1])

        return result.any()

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
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('x', 6), ('y', 3), ('time', 22), ('action', 'move to'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('x', 3), ('y', 3), ('time', 45), ('action', 'time at patient'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('x', 3), ('y', 3), ('time', 45), ('action', 'finish event'))
        self.assertTrue(self.check_conditions(conditions))

        #return to office
        conditions = (('x', 9), ('y', 17), ('time', 65), ('action', 'move to'))
        self.assertTrue(self.check_conditions(conditions))

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
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('nurse', 0), ('x', 9), ('y', 17), ('time', 90), ('action', 'assign event'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('nurse', 1), ('x', 9), ('y', 17), ('time', 10), ('action', 'assign event'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('nurse', 1), ('x', 3), ('y', 8), ('time', 70), ('action', 'assign event'))
        self.assertTrue(self.check_conditions(conditions))

        conditions = (('nurse', 0), ('x', 3), ('y', 3), ('time', 45), ('action', 'finish event'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('nurse', 0), ('x', 3), ('y', 3), ('time', 130), ('action', 'finish event'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('nurse', 1), ('x', 3), ('y', 8), ('time', 45), ('action', 'finish event'))
        self.assertTrue(self.check_conditions(conditions))
        conditions = (('nurse', 1), ('x', 3), ('y', 8), ('time', 90), ('action', 'finish event'))
        self.assertTrue(self.check_conditions(conditions))

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


    def test_sim_other_assigner(self):
        #TODO: something weird is going on with displayed request numbers
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/manyPeople.json"
        event_path = "input/events/testEventsRequestsOther.json"
        app = App(graph_path=graph_path, people_path=people_path, event_path=event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)

        app.run_simulation(visualise=True)

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

    def test_other_assigner_one_nurse(self):
        graph_path = "input/layouts/toScaleLayout.json"
        people_path = "input/people/oneNurse.json"
        basic_event_path = "input/events/basic1nurse.json"
        other_event_path = "input/events/other1nurse.json"

        # app = App(graph_path=graph_path, people_path=people_path, event_path=basic_event_path,
        #           nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        # app.run_simulation()
        # dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output, people_path=people_path)
        # basic_time_at_patients = dp.nurse_time_at_all_patients(0)

        app = App(graph_path=graph_path, people_path=people_path, event_path=other_event_path,
                  nurse_output_path=self.test_nurse_output, event_output_path=self.test_event_output)
        app.run_simulation()
        dp = DataProcessor(nurse_log_path=self.test_nurse_output, event_log_path=self.test_event_output,
                           people_path=people_path)
        other_time_at_patients = dp.nurse_time_at_all_patients(0)

        self.assertEqual(basic_time_at_patients, other_time_at_patients)

if __name__ == '__main__':
    unittest.main()
