from .node import Node
from sortedcontainers import SortedDict

class Graph:
    def __init__(self, nodes: list[Node], edges: list[list[tuple[Node, int]]]) -> None:
        self.nodes = nodes
        self.edges = edges
        pass
    
    def __retrace_path(self, start_id: int, end_id: int, prev: list[int]) -> list[Node]:
        path = []
        current_id = end_id
        while current_id != start_id:
            path.append(self.nodes[current_id]) 
            current_id = prev[current_id]
        path.append(self.nodes[start_id])
        path.reverse()
        return path
    
    def find_path(self, start: Node, end: Node) -> list[Node]:
        #dijkstra, source: https://courses.fit.cvut.cz/BI-AG1/lectures/media/bi-ag1-p12-handout.pdf
        start_id = start.node_id
        end_id = end.node_id
        node_cnt = len(self.nodes)
        
        open_nodes = set()
        prev: list[int] = [-1] * node_cnt #predecessors
        dist = SortedDict() #distances to all nodes
        open_dist = SortedDict() #distances to open nodes

        for i in range(node_cnt):
            dist[i] = float('inf')

        dist[start_id] = 0
        open_dist[start_id] = 0
        open_nodes.add(start_id)

        while len(open_nodes) > 0:
            current_id = open_dist.popitem(0)[0]
            for neighbour, weight in self.edges[current_id]:
                neighbour_id = neighbour.node_id
                new_dist = dist[current_id] + weight
                if dist[neighbour_id] > new_dist: #what if neighbour is predecessor of current
                    dist[neighbour_id] = new_dist
                    prev[neighbour_id] = current_id
                    open_dist[neighbour_id] = new_dist
                    if neighbour_id not in open_nodes:
                        open_nodes.add(neighbour_id)
            open_nodes.remove(current_id) 
        
        return self.__retrace_path(start_id, end_id, prev)
