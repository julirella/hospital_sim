import json
import src.node
from src.node import Junction, PatientRoom, Room, NurseOffice
from src.graph import Graph
from src.nurse import Nurse
from src.patient import Patient

def parse_nodes(nodes_dict: dict) -> tuple[Graph, dict]:
    nodes: list[src.node.Node] = []
    node_ids = {}
    room_number = 0
    nurse_office: NurseOffice | None = None
    patient_rooms: list[PatientRoom] = []

    for node_id, key, val in enumerate(nodes_dict.items()):
        node_ids[key] = node_id
        x = val["ui"]["pos"]["x"]
        y = val["ui"]["pos"]["y"]
        node_type = val["properties"]["name"]
        if node_type == "J":
            node = Junction(node_id, x, y)
        elif node_type == "P":
            node = PatientRoom(node_id, x, y, room_number)
            patient_rooms.append(node)
            room_number += 1
        elif node_type == "N":
            node = NurseOffice(node_id, x, y)
            if nurse_office is None:
                raise Exception("can't have two nurse offices")
            nurse_office = node
        else:
            raise Exception(f"Unknown node type: {node_type}")
        nodes.append(node)

    graph = Graph(nodes, nurse_office, patient_rooms)
    return graph, node_ids

def parse_edges(edges_dict: dict, node_ids: dict[str, int], graph: Graph) -> None:
    for val in edges_dict.values():
        src_node = val["ui"]["connects"]["from"]
        dst_node = val["ui"]["connects"]["to"]
        src_id = node_ids[src_node]
        dst_id = node_ids[dst_node]
        graph.add_edge(src_id, dst_id)


def import_graphit_graph(file_path: str) -> Graph:
    file = open(file_path)
    graph_json = json.load(file)
    nodes_dict = graph_json['nodes']
    edges_dict = graph_json['edges']

    graph, node_ids = parse_nodes(nodes_dict)
    parse_edges(edges_dict, node_ids, graph)

    return graph


def import_entities(file_path: str, graph: Graph) -> tuple[list[Nurse], list[Patient]]:
    file = open(file_path)
    entities_json = json.load(file)

    nurse_cnt = entities_json["nurses"]
    nurses: list[Nurse] = []
    for i in nurse_cnt:
        nurses.append(Nurse(i, graph.nurse_office))

    patient_lst = entities_json["patients"]
    patients: list[Patient] = []
    for patient_info in patient_lst:
        nurse = nurses[patient_info["nurse_id"]]
        room = graph.patient_rooms[patient_info["room"]]
        patient = Patient(nurse, room)
        patients.append(patient)

    return nurses, patients


def import_events(file_path: str):
    pass