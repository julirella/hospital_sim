from sortedcontainers import SortedDict
from math import sqrt

from src.simulation.node import NurseOffice, PatientRoom
from src.simulation.node import Node

class Graph:
    def __init__(self, nodes: list[Node], nurse_office: NurseOffice, patient_rooms: list[PatientRoom]) -> None:
        self._nodes = nodes
        self._nurse_office = nurse_office
        self._patient_rooms = patient_rooms
        self._max_distance: float | None = None

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
        weight = self.__edge_weight__(src_node_id, dst_node_id)

        #TODO: maybe check for duplicate edges
        self._nodes[src_node_id].add_neighbour(dst_node_id, weight)
        self._nodes[dst_node_id].add_neighbour(src_node_id, weight)

    def __retrace_path__(self, start_id: int, end_id: int, prev: list[tuple[int, float]]) -> list[tuple[Node, float]]:
        path: list[tuple[Node, float]] = []
        current_id = end_id
        while current_id != start_id:
            prev_id, dst = prev[current_id]
            path.append((self._nodes[current_id], dst))
            current_id = prev_id
        # path.append((self.nodes[start_id], 0.0)) #we don't need start in the path
        path.reverse()
        return path

    def find_path(self, start: Node, end: Node) -> list[tuple[Node, float]]:
        #finds shortest path between nodes using dijkstra
        #returns list of tuple[node, distance], where distance is the distance from the node from the previous tuple to the node from the current one
        #the list should not contain start node but should contain end node
        #dijkstra, source: https://courses.fit.cvut.cz/BI-AG1/lectures/media/bi-ag1-p12-handout.pdf
        start_id = start.node_id
        end_id = end.node_id
        node_cnt = len(self._nodes)
        if start_id == -1: #in case of tmp node start
            node_cnt += 1

        open_nodes = set()
        prev: list[tuple[int, float]] = [(-1, -1)] * node_cnt #predecessors
        dist = SortedDict() #distances to all nodes
        open_dist = SortedDict() #distances to open nodes

        for i in range(node_cnt):
            dist[i] = float('inf')

        dist[start_id] = 0
        open_dist[start_id] = 0
        open_nodes.add(start_id)

        while len(open_nodes) > 0:
            current_id: int = open_dist.popitem(0)[0]
            if current_id == -1: # -1 means it's a tmp node, which can only be start
                neighbours = start.neighbours
            else:
                neighbours = self._nodes[current_id].neighbours
            for neighbour_id, weight in neighbours:
                new_dist = dist[current_id] + weight
                if dist[neighbour_id] > new_dist: #what if neighbour is predecessor of current
                    dist[neighbour_id] = new_dist
                    prev[neighbour_id] = (current_id, weight)
                    open_dist[neighbour_id] = new_dist
                    if neighbour_id not in open_nodes:
                        open_nodes.add(neighbour_id)
            open_nodes.remove(current_id)

        return self.__retrace_path__(start_id, end_id, prev)

    def max_distance(self) -> float:
        if self._max_distance is not None:
            return self._max_distance
        else: #probably about the slowest way of doing this, but it's only gonna be run once
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