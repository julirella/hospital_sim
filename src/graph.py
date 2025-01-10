from node import Node
from sortedcontainers import SortedDict

class Graph:
    def __init__(self, nodes: list[Node], edges: list[list[tuple[Node, int]]]) -> None:
        self.nodes = nodes
        self.edges = edges
        pass
    
    def find_path(self, start: Node, end: Node) -> list[Node]:
        start_id = start.id
        end_id = end.id
        node_cnt = len(self.nodes)
        
        path = []
        prev = [None] * node_cnt
        dist = SortedDict()
        for i in range(node_cnt):
            dist[i] = float('inf')
