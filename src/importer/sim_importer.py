
from src import Graph, EventList, NurseList, RequestAssigner
from src.simulation.event import Request, Plan
from src.simulation.nurse import Nurse
from src.simulation.patient import Patient
from src.simulation.simulator import Simulator
from .importer import Importer
from src.simulation.request_assigner import BasicAssigner
from src.simulation.request_assigner import OtherAssigner
from src.simulation.sim_time import SimTime


class SimImporter(Importer):
    def __init__(self, graph_file_name: str, entity_file_name: str, event_file_name: str ) -> None:
        super().__init__(graph_file_name, entity_file_name)
        self.entity_file_name = entity_file_name
        self.event_file_name = event_file_name
        self.request_assigner: RequestAssigner

    def import_entities(self, graph: Graph, sim_time: SimTime) -> tuple[list[Nurse], list[Patient]]:
        entities_json = self.load_json(self.entity_file_name)

        nurse_cnt = entities_json["nurses"]
        nurses: list[Nurse] = []
        for i in range(nurse_cnt):
            nurses.append(Nurse(i, graph.nurse_office, sim_time))

        patient_lst = entities_json["patients"]
        patients: list[Patient] = []
        for i, patient_info in enumerate(patient_lst):
            nurse = nurses[patient_info["nurse_id"]]
            room = graph.patient_rooms[patient_info["room"]]
            patient = Patient(i, nurse, room, sim_time)
            patients.append(patient)

        return nurses, patients

    def import_events(self, nurses: list[Nurse], patients: list[Patient], graph: Graph, sim_time: SimTime) -> tuple[EventList, list[NurseList]]:
        events_json = self.load_json(self.event_file_name)

        request_assigner = events_json["request_assigner"]
        request_lst = events_json["requests"]
        plan_lst = events_json["plans"]

        # request_queue = EventQueue()
        requests = []
        for request_dict in request_lst:
            time: float = request_dict["time"]
            patient: Patient = patients[request_dict["patient"]]
            level: int = request_dict["level"]
            duration: float = request_dict["duration"]
            request = Request(time, duration, patient, level, graph, sim_time)
            requests.append(request)
            # request_queue.add(request)
        request_queue = EventList(requests)

        nurse_queues: [NurseList] = []
        # for nurse in nurses:
        #     nurse_queues.append(NurseQueue(nurse, sim_time))

        plans = [[] for _ in range(len(nurses))]

        for plan_dict in plan_lst:
            time: float = plan_dict["time"]
            patient: Patient = patients[plan_dict["patient"]]
            duration: float = plan_dict["duration"]
            nurse_id: int = plan_dict["nurse"]
            nurse: Nurse = nurses[nurse_id]
            plan = Plan(time, duration, patient, nurse, graph, sim_time)
            # nurse_queues[nurse_id].add(plan)
            plans[nurse_id].append(plan)

        for nurse_id, plan_array in enumerate(plans):
            nurse_queues.append(NurseList(plan_array, sim_time, nurses[nurse_id], graph.max_distance(), graph))

        if request_assigner == "basic":
            self.request_assigner = BasicAssigner(nurse_queues)
        elif request_assigner == "other":
            self.request_assigner = OtherAssigner(nurse_queues)

        return request_queue, nurse_queues


    def import_data(self) -> Simulator:
        print("importing")
        graph = self._import_graph()
        sim_time = SimTime()
        nurses, patients = self.import_entities(graph, sim_time)
        req_queue, nurse_queues = self.import_events(nurses, patients, graph, sim_time)
        simulator = Simulator(graph, nurses, patients, req_queue, nurse_queues, sim_time, self.request_assigner)
        return simulator