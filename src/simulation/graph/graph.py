from math import sqrt
import heapdict as hd

from src.simulation.graph.node import NurseOffice, PatientRoom
from src.simulation.graph.node import Node

class Graph:
    """
    Graph of the department
    """
    def __init__(self, nodes: list[Node], nurse_office: NurseOffice, patient_rooms: list[PatientRoom]) -> None:
        """
        :param nodes: list of all graph nodes (including rooms and nurse office)
        :param nurse_office: nurse office node
        :param patient_rooms: list of patient room nodes
        """
        self._nodes = nodes
        self._nurse_office = nurse_office
        self._patient_rooms = patient_rooms
        self._max_distance: float | None = None # graph diameter, longest shortest path between any two nodes

    @property
    def nurse_office(self) -> NurseOffice:
        return self._nurse_office

    @property
    def patient_rooms(self) -> list[PatientRoom]:
        return self._patient_rooms

    def __edge_weight__(self, src_node_id: int, dst_node_id: int) -> float:
        #Euclidean distance between nodes
        src_x, src_y = self._nodes[src_node_id].x, self._nodes[src_node_id].y
        dst_x, dst_y = self._nodes[dst_node_id].x, self._nodes[dst_node_id].y
        weight = sqrt((src_x - dst_x)**2 + (src_y - dst_y)**2)
        return weight

    def add_edge(self, src_node_id: int, dst_node_id: int) -> None:
        """
        Adds undirected edge to graph between two nodes, calculates edge weight. Input node order does not matter
        but doesn't check for duplicate edges in the graph.
        :param src_node_id:
        :param dst_node_id:
        :return:
        """
        weight = self.__edge_weight__(src_node_id, dst_node_id)

        self._nodes[src_node_id].add_neighbour(dst_node_id, weight)
        self._nodes[dst_node_id].add_neighbour(src_node_id, weight)

    def __retrace_path__(self, start_id: int, end_id: int, prev: list[tuple[int, float]]) -> list[tuple[Node, float]]:
        # build path from list of predecessors found by dijkstra's algorithm
        path: list[tuple[Node, float]] = []
        current_id = end_id
        while current_id != start_id:
            prev_id, dst = prev[current_id]
            path.append((self._nodes[current_id], dst))
            current_id = prev_id
        path.reverse()
        return path

    def find_path(self, start: Node, end: Node) -> list[tuple[Node, float]]:
        """
        Finds shortest path between start and end using dijkstra's algorithm
        Dijkstra implementation based on: https://courses.fit.cvut.cz/BI-AG1/lectures/media/bi-ag1-p12-handout.pdf
        :param start: start node
        :param end: end node
        :return: list of tuple[node, distance], where distance is the distance from the node from the previous tuple
        to the node from the current one. The list contains the end node but not the start node
        """

        start_id = start.node_id
        end_id = end.node_id
        node_cnt = len(self._nodes)
        if start_id == -1: #in case of tmp node start
            node_cnt += 1

        prev: list[tuple[int, float]] = [(-1, -1)] * node_cnt #predecessors
        dist = [float('inf')] * node_cnt #distances to all nodes
        open_dist = hd.heapdict() # distances to open nodes

        dist[start_id] = 0
        open_dist[start_id] = 0

        while len(open_dist) > 0:
            current_id: int = open_dist.popitem()[0] # get the open node with the smallest distance
            if current_id == -1: # -1 means it's a tmp node, which can only be start
                neighbours = start.neighbours
            else:
                neighbours = self._nodes[current_id].neighbours
            for neighbour_id, weight in neighbours:
                new_dist = dist[current_id] + weight
                if dist[neighbour_id] > new_dist:
                    dist[neighbour_id] = new_dist
                    prev[neighbour_id] = (current_id, weight)
                    open_dist[neighbour_id] = new_dist

        return self.__retrace_path__(start_id, end_id, prev)

    def max_distance(self) -> float:
        """
        Finds max distance a nurse has to walk in the graph, so graph diameter
        :return: max distance in the graph
        """

        # run it only the first time and save the result
        if self._max_distance is not None:
            return self._max_distance
        else:
            distances = []
            for start in self._nodes:
                for end in self._nodes:
                    if start != end:
                        path = self.find_path(start, end)
                        dst = 0
                        for node in path:
                            dst += node[1]
                        distances.append(dst)
            max_dst = max(distances)
            self._max_distance = max_dst
            return max_dst