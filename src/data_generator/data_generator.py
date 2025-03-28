import json

from src.importer import GenImporter


class DataGenerator:
    def __init__(self, layout_file: str, people_file: str, out_file: str, plan_starts: list[int],
                 request_assigner: str = 'basic', med_duration: int = 60):
        self.gen_importer = GenImporter(graph_file_name = layout_file, entity_file_name = people_file)
        self.gen_importer.import_data()
        self.nurse_patients = self.gen_importer.nurse_patients
        self.plans = []
        self.requests = []
        self.request_assigner = request_assigner
        self.out_file = out_file
        self.plan_starts = plan_starts
        self.med_duration = med_duration

    def med_plan_group(self, start_time: int) -> list[dict]:
        #each nurse visits all of her patients and gives them meds
        plan_gap = self.max_graph_dst()
        plans = []
        for nurse_id, patient_lst in enumerate(self.nurse_patients):
            time = start_time
            for patient_id in patient_lst:
                plan = {"time": time, "patient": patient_id, "nurse": nurse_id, "duration": self.med_duration}
                time += self.med_duration + plan_gap
                plans.append(plan)

        return plans

    def med_plans(self):
        for time in self.plan_starts:
            self.plans += self.med_plan_group(time)

    def to_json(self):
        event_dict = {}
        event_dict["request_assigner"] = self.request_assigner
        event_dict["requests"] = self.requests
        event_dict["plans"] = self.plans
        json_str = json.dumps(event_dict, indent=4)
        print(json_str)
        file = open(self.out_file, "w")
        file.write(json_str)
        file.close()

    def max_graph_dst(self):
        return self.gen_importer.max_graph_dst()

    def create_events(self):
        self.med_plans()
        # requests
        self.to_json()