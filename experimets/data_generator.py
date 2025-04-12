import json
import numpy as np

from src.importer import GenImporter


class DataGenerator:
    def __init__(self, rnd: int,layout_file: str, people_file: str, out_file: str, plan_starts: list[int] = [0, 1800],
                 request_assigner: str = 'basic', include_plans: bool = True , med_duration: int = 60, interval_len: int = 3600,
                 min_requests = 3, max_requests = 10, min_req_len = 30, max_req_len = 180):
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
        np.random.seed(rnd)

    def med_plan_group(self, start_time: int) -> list[dict]:
        #each nurse visits all of her patients and gives them meds
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
        for time in self.plan_starts:
            if self.include_plans:
                self.plans += self.med_plan_group(time)
            else:
                self.requests += self.med_plan_group(time)

    def generate_requests(self):
        patient_cnt = self.gen_importer.patient_cnt

        req_levels = [2, 3]
        level_probabilities = [0.75, 0.25]
        for patient_id in range(patient_cnt):
            request_amount = np.random.randint(self.min_requests, self.max_requests)
            for _ in range(request_amount):
                req_time = np.random.uniform(0, self.interval_len)
                level = int(np.random.choice(req_levels, p=level_probabilities))
                duration = np.random.uniform(self.min_req_len, self.max_req_len)

                req = {}
                req["time"] = req_time
                req["patient"] = patient_id
                req["level"] = level
                req["duration"] = duration
                print(req)
                self.requests.append(req)

    def to_json(self):
        event_dict = {}
        event_dict["request_assigner"] = self.request_assigner
        event_dict["requests"] = self.requests
        event_dict["plans"] = self.plans
        json_str = json.dumps(event_dict, indent=4)
        # print(json_str)
        file = open(self.out_file, "w")
        file.write(json_str)
        file.close()

    def max_graph_dst(self):
        return self.gen_importer.max_graph_dst()

    def create_events(self):
        self.plans = []
        self.requests = []
        self.med_plans()
        self.generate_requests()
        self.to_json()