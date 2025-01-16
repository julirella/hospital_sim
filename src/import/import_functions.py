import json
import src.node
from src.node import Node, Junction, PatientRoom
from src.graph import Graph


def parse_nodes(nodes_dict: dict) -> tuple[list[src.node.Node], dict[str, int]]:
    nodes: list[src.node.Node] = []
    node_ids = {}

    for node_id, key, val in enumerate(nodes_dict.items()):
        node_ids[key] = node_id
        x = val["ui"]["pos"]["x"]
        y = val["ui"]["pos"]["y"]
        node_type = val["properties"]["name"]
        if node_type == "J":
            node = Junction(node_id, x, y)
        elif node_type == "P":
            node = PatientRoom(node_id, x, y)
        # elif node_type == "N":
        #     node = NurseOffice(node_id, x, y)
        else:
            raise Exception(f"Unknown node type: {node_type}")
        nodes.append(node)

    return nodes, node_ids

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

    nodes, node_ids = parse_nodes(nodes_dict)
    graph = Graph(nodes)

    parse_edges(edges_dict, node_ids, graph)

    return graph




def import_events(file_path: str):
    pass

def import_entities(file_path: str):
    pass