
from src import Graph, EventList, NurseList, RequestAssigner
from src.simulation.timed_object import Request, Plan
from src.simulation.people.nurse import Nurse
from src.simulation.people.patient import Patient
from src.simulation.simulator import Simulator
from .importer import Importer
from src.simulation.request_assigner import BasicAssigner
from src.simulation.request_assigner import OtherAssigner
from src.simulation.sim_time import SimTime


class SimImporter(Importer):
    """
    class for importing simulation input and constructing the Simulator object
    """
    def __init__(self, graph_file_name: str, entity_file_name: str, event_file_name: str ) -> None:
        """
        :param graph_file_name: path to file with department layout graph
        :param entity_file_name: path to file specifying people
        :param event_file_name: path to file specifying events
        """
        super().__init__(graph_file_name, entity_file_name)
        self.event_file_name = event_file_name
        self.request_assigner: RequestAssigner

    def __import_entities__(self, graph: Graph, sim_time: SimTime) -> tuple[list[Nurse], list[Patient]]:
        # import specified nurses and patients from files and construct corresponding objects

        entities_json = self.__load_json__(self.entity_file_name)

        nurse_cnt = entities_json["nurses"]
        nurses: list[Nurse] = []
        for i in range(nurse_cnt):
            nurses.append(Nurse(i, graph.nurse_office, sim_time))

        patient_lst = entities_json["patients"]
        patients: list[Patient] = []
        for i, patient_info in enumerate(patient_lst):
            nurse = nurses[patient_info["nurse_id"]]
            room = graph.patient_rooms[patient_info["room"]]
            patient = Patient(i, nurse, room)
            patients.append(patient)

        return nurses, patients

    def __import_events__(self, nurses: list[Nurse], patients: list[Patient], graph: Graph, sim_time: SimTime) -> tuple[EventList[Request], list[NurseList]]:
        # import events from files and construct corresponding objects

        events_json = self.__load_json__(self.event_file_name)

        request_assigner = events_json["request_assigner"]
        request_lst = events_json["requests"]
        plan_lst = events_json["plans"]

        requests = []
        for request_dict in request_lst:
            time: float = request_dict["time"]
            patient: Patient = patients[request_dict["patient"]]
            level: int = request_dict["level"]
            duration: float = request_dict["duration"]
            request = Request(time, duration, patient, level, graph, sim_time)
            requests.append(request)
        request_queue = EventList(requests)

        nurse_queues: [NurseList] = []

        plans = [[] for _ in range(len(nurses))]

        for plan_dict in plan_lst:
            time: float = plan_dict["time"]
            patient: Patient = patients[plan_dict["patient"]]
            duration: float = plan_dict["duration"]
            nurse_id: int = plan_dict["nurse"]
            nurse: Nurse = nurses[nurse_id]
            plan = Plan(time, duration, patient, nurse, graph, sim_time)
            plans[nurse_id].append(plan)

        for nurse_id, plan_array in enumerate(plans):
            nurse_queues.append(NurseList(plan_array, sim_time, nurses[nurse_id], graph.max_distance(), graph))

        if request_assigner == "basic":
            self.request_assigner = BasicAssigner(nurse_queues)
        elif request_assigner == "other":
            self.request_assigner = OtherAssigner(nurse_queues)

        return request_queue, nurse_queues


    def import_data(self) -> Simulator:
        """
        import simulation data and construct Simulator
        :return: the constructed Simulator
        """
        print("Importing...")
        graph = self.__import_graph__()
        sim_time = SimTime()
        nurses, patients = self.__import_entities__(graph, sim_time)
        req_queue, nurse_queues = self.__import_events__(nurses, patients, graph, sim_time)
        simulator = Simulator(graph, nurses, patients, req_queue, nurse_queues, sim_time, self.request_assigner)
        return simulator