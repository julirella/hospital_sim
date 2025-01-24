from abc import abstractmethod
import json
from src import Graph
from src.node import *


class Importer:
    def __init__(self, graph_filename: str, graph_type: str="graphit") -> None:
        self.graph_filename = graph_filename
        self.graph_type = graph_type

    def parse_nodes(self, nodes_dict: dict) -> tuple[Graph, dict]:
        nodes: list[Node] = []
        node_ids = {}
        room_number = 0
        nurse_office: NurseOffice | None = None
        patient_rooms: list[PatientRoom] = []

        for node_id, item in enumerate(nodes_dict.items()):
            key, val = item
            node_ids[key] = node_id
            x = val["ui"]["pos"]["x"]
            y = val["ui"]["pos"]["y"]
            node_type = val["properties"]["name"]
            if node_type == "J":
                node = Junction(node_id, x, y)
            # elif node_type == "P":
            #     node = PatientRoom(node_id, x, y, room_number)
            #     patient_rooms.append(node)
            #     room_number += 1
            elif node_type == "N":
                node = NurseOffice(node_id, x, y)
                if nurse_office is not None:
                    raise Exception("can't have two nurse offices")
                nurse_office = node
            else:
                node = PatientRoom(node_id, x, y, room_number)
                patient_rooms.append(node)
                room_number += 1
            # else:
            #     raise Exception(f"Unknown node type: {node_type}")
            nodes.append(node)

        graph = Graph(nodes, nurse_office, patient_rooms)
        return graph, node_ids

    def parse_edges(self, edges_dict: dict, node_ids: dict[str, int], graph: Graph) -> None:
        for val in edges_dict.values():
            src_node = val["ui"]["connects"]["from"]
            dst_node = val["ui"]["connects"]["to"]
            src_id = node_ids[src_node]
            dst_id = node_ids[dst_node]
            graph.add_edge(src_id, dst_id)

    def import_graphit_graph(self) -> Graph:
        file = open(self.graph_filename)
        graph_json = json.load(file)
        nodes_dict = graph_json['nodes']
        edges_dict = graph_json['edges']

        graph, node_ids = self.parse_nodes(nodes_dict)
        self.parse_edges(edges_dict, node_ids, graph)

        return graph

    def _import_graph(self) -> Graph:
        if self.graph_type == "graphit":
            return self.import_graphit_graph()

    @abstractmethod
    def import_data(self) -> None:
        pass