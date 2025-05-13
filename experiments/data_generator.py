import json
import numpy as np

from src.importer import GenImporter


class DataGenerator:
    """
    class for generating events for simulation input
    """
    def __init__(self, rnd: int,layout_file: str, people_file: str, out_file: str, plan_starts: list[int] = [0, 1800],
                 request_assigner: str = 'basic', include_plans: bool = True , med_duration: int = 60, interval_len: int = 3600,
                 min_requests = 3, max_requests = 10, min_req_len = 30, max_req_len = 180):
        """
        :param rnd: random seed
        :param layout_file: path to file with the department layout
        :param people_file: path to the file specifying nurses and patients
        :param out_file: path to the file to which to write the generated events
        :param plan_starts: list of times at which to start group of generated plans
        :param request_assigner: request assigner type
        :param include_plans: true if plans should be generated as plans, false for requests level 1
        :param med_duration: duration of generated plans
        :param interval_len: length of the time in which to generate events
        :param min_requests: minimum number of requests generated per patient
        :param max_requests: maximum number of requests generated per patient
        :param min_req_len: minimum length of each generated request in seconds
        :param max_req_len: maximum length of each generated request in seconds
        """
        self.gen_importer = GenImporter(graph_file_name = layout_file, entity_file_name = people_file)
        self.gen_importer.import_data()
        self.nurse_patients = self.gen_importer.nurse_patients

        self.plans = []
        self.requests = []

        self.request_assigner = request_assigner
        self.include_plans = include_plans
        self.out_file = out_file
        self.plan_starts = plan_starts
        self.med_duration = med_duration
        self.interval_len = interval_len
        self.min_requests = min_requests
        self.max_requests = max_requests
        self.min_req_len = min_req_len
        self.max_req_len = max_req_len

        self.rng = np.random.default_rng(rnd)

    def med_plan_group(self, start_time: int) -> list[dict]:
        # each nurse visits all of her patients and gives them meds, create plans for that
        plan_gap = self.max_graph_dst()
        plans = []
        for nurse_id, patient_lst in enumerate(self.nurse_patients):
            time = start_time
            for patient_id in patient_lst:
                if self.include_plans:
                    plan = {"time": time, "patient": patient_id, "nurse": nurse_id, "duration": self.med_duration}
                else:
                    plan = {"time": time, "patient": patient_id, "level": 1, "duration": self.med_duration}
                time += self.med_duration + plan_gap
                plans.append(plan)

        return plans

    def med_plans(self):
        # create group of plans for each given plan group start
        for time in self.plan_starts:
            if self.include_plans:
                self.plans += self.med_plan_group(time)
            else:
                self.requests += self.med_plan_group(time)

    def generate_requests(self):
        # randomly generate requests for each patient in the give time interval
        patient_cnt = self.gen_importer.patient_cnt

        req_levels = [2, 3]
        level_probabilities = [0.75, 0.25]
        for patient_id in range(patient_cnt):
            request_amount = self.rng.integers(self.min_requests, self.max_requests)
            for _ in range(request_amount):
                req_time = self.rng.uniform(0, self.interval_len)
                level = int(self.rng.choice(req_levels, p=level_probabilities))
                duration = self.rng.uniform(self.min_req_len, self.max_req_len)

                req = {}
                req["time"] = req_time
                req["patient"] = patient_id
                req["level"] = level
                req["duration"] = duration
                self.requests.append(req)

    def to_json(self):
        # write plans and events to given file in json format
        event_dict = {}
        event_dict["request_assigner"] = self.request_assigner
        event_dict["requests"] = self.requests
        event_dict["plans"] = self.plans
        json_str = json.dumps(event_dict, indent=4)
        file = open(self.out_file, "w")
        file.write(json_str)
        file.close()

    def max_graph_dst(self):
        return self.gen_importer.max_graph_dst()

    def create_events(self):
        """
        generate events and write them to given output file
        """
        self.plans = []
        self.requests = []
        self.med_plans()
        self.generate_requests()
        self.to_json()