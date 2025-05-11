from abc import abstractmethod
import json


from src import Graph
from src.simulation.graph.node import Node, Junction, NurseOffice, PatientRoom
from src.constants import *


class Importer:
    """
    abstract class for importing and processing simulation input
    """
    def __init__(self, graph_filename: str, entity_file_name: str, graph_type: str="graphit") -> None:
        """
        :param graph_filename: path to file with department layout graph
        :param entity_file_name: path to file specifying people
        :param graph_type: type of graph to import, currently the only option is "graphit" for graphs created with
        graphIT (https://graphit.web.app/app)
        """
        self.graph_filename = graph_filename
        self.graph_type = graph_type
        self.entity_file_name = entity_file_name

        self.node_ids = {} # ID's that graphIT gives the nodes
        self.nodes: list[Node] = []
        self.nurse_office: NurseOffice | None = None
        self.patient_rooms: list[PatientRoom] = []
        self.edges: list[tuple[int, int]] = []

    def __load_json__(self, path):
        # load json into nested lists
        file = open(path)
        res = json.load(file)
        file.close()
        return res

    def __parse_nodes__(self, nodes_dict: dict) -> None:
        # parse graph nodes from graphIT node dict, construct corresponding Node objects and save graphIT ID's

        room_number = 0

        for node_id, item in enumerate(nodes_dict.items()):
            key, val = item
            self.node_ids[key] = node_id
            x = val["ui"]["pos"]["x"] / GRAPHIT_PIXELS_PER_METER
            y = val["ui"]["pos"]["y"] / GRAPHIT_PIXELS_PER_METER
            node_type = val["properties"]["name"]

            if node_type == "J":
                node = Junction(node_id, x, y)
            elif node_type == "N":
                node = NurseOffice(node_id, x, y)
                if self.nurse_office is not None:
                    raise Exception("can't have two nurse offices")
                self.nurse_office = node
            else:
                node = PatientRoom(node_id, x, y, room_number)
                self.patient_rooms.append(node)
                room_number += 1

            self.nodes.append(node)


    def __parse_edges__(self, edges_dict: dict) -> None:
        # parse graph edges from graphIT edge dict, add them as edges of correct nodes based on graphIT ID's

        for val in edges_dict.values():
            src_node = val["ui"]["connects"]["from"]
            dst_node = val["ui"]["connects"]["to"]
            src_id = self.node_ids[src_node]
            dst_id = self.node_ids[dst_node]
            # graph.add_edge(src_id, dst_id)
            self.edges.append((src_id, dst_id))

    def __parse_graphit_graph__(self) -> None:
        # parse nodes and edges from graphIT graph
       graph_json = self.__load_json__(self.graph_filename)
       nodes_dict = graph_json['nodes']
       edges_dict = graph_json['edges']
       self.__parse_nodes__(nodes_dict)
       self.__parse_edges__(edges_dict)

    def __import_graphit_graph__(self) -> Graph:
        # import graphIT graph and construct a Graph object from it
        self.__parse_graphit_graph__()

        graph = Graph(self.nodes, self.nurse_office, self.patient_rooms)
        for edge in self.edges:
            graph.add_edge(edge[0], edge[1])

        return graph

    def __import_graph__(self) -> Graph:
        if self.graph_type == "graphit":
            return self.__import_graphit_graph__()
        else:
            raise "only graphit graph supported currently"

    @abstractmethod
    def import_data(self) -> None:
        """
        import specified files
        """
        pass