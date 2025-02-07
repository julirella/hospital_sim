from abc import abstractmethod
import json
from src import Graph
from src.node import Node, Junction, NurseOffice, PatientRoom

PIXELS_PER_METER = 35

class Importer:
    def __init__(self, graph_filename: str, graph_type: str="graphit") -> None:
        self.graph_filename = graph_filename
        self.graph_type = graph_type
        self.node_ids = {}
        self.nodes: list[Node] = []
        self.nurse_office: NurseOffice | None = None
        self.patient_rooms: list[PatientRoom] = []
        self.edges: list[tuple[int, int]] = []

    def load_json(self, path):
        file = open(path)
        res = json.load(file)
        file.close()
        return res

    def parse_nodes(self, nodes_dict: dict) -> None:
        room_number = 0

        for node_id, item in enumerate(nodes_dict.items()):
            key, val = item
            self.node_ids[key] = node_id
            x = val["ui"]["pos"]["x"] / PIXELS_PER_METER
            y = val["ui"]["pos"]["y"] / PIXELS_PER_METER
            node_type = val["properties"]["name"]
            if node_type == "J":
                node = Junction(node_id, x, y)
            # elif node_type == "P":
            #     node = PatientRoom(node_id, x, y, room_number)
            #     patient_rooms.append(node)
            #     room_number += 1
            elif node_type == "N":
                node = NurseOffice(node_id, x, y)
                if self.nurse_office is not None:
                    raise Exception("can't have two nurse offices")
                self.nurse_office = node
            else:
                node = PatientRoom(node_id, x, y, room_number)
                self.patient_rooms.append(node)
                room_number += 1
            # else:
            #     raise Exception(f"Unknown node type: {node_type}")
            self.nodes.append(node)


    def parse_edges(self, edges_dict: dict) -> None:

        for val in edges_dict.values():
            src_node = val["ui"]["connects"]["from"]
            dst_node = val["ui"]["connects"]["to"]
            src_id = self.node_ids[src_node]
            dst_id = self.node_ids[dst_node]
            # graph.add_edge(src_id, dst_id)
            self.edges.append((src_id, dst_id))

    def parse_graphit_graph(self):
       graph_json = self.load_json(self.graph_filename)
       nodes_dict = graph_json['nodes']
       edges_dict = graph_json['edges']
       self.parse_nodes(nodes_dict)
       self.parse_edges(edges_dict)

    def import_graphit_graph(self) -> Graph:
        self.parse_graphit_graph()

        graph = Graph(self.nodes, self.nurse_office, self.patient_rooms)
        for edge in self.edges:
            graph.add_edge(edge[0], edge[1])

        return graph

    def _import_graph(self) -> Graph:
        if self.graph_type == "graphit":
            return self.import_graphit_graph()

    @abstractmethod
    def import_data(self) -> None:
        pass