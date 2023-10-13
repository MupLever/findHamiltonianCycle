"""
The module allows you to create an arbitrary weighted graph,
has methods for traversing the graph in depth and width, a method
for searching for a Hamiltonian cycle
"""

from __future__ import annotations
from typing import Any, List
from queue import Queue
from random import choice


class Graph:
    """an undirected graph class implemented through a dictionary"""

    class Node:
        """node class storing node value and incident edges"""

        def __init__(self, value: Any):
            self.value = value
            self.edges = set()
            self.parents = {}

        def __ne__(self, other) -> bool:
            if not isinstance(other, type(self)):
                return True

            return self.value != other.value

        def __eq__(self, other) -> bool:
            if not isinstance(other, type(self)):
                return False

            return self.value == other.value

        def __hash__(self) -> int:
            return hash(self.value)

        def __repr__(self) -> str:
            return f"<Node: {self.value=}>"

    class Edge:
        """edge class storing the incident node"""

        def __init__(self, incident_node, weight: int):
            self.incident_node = incident_node
            self.weight = weight

        def __lt__(self, other) -> bool:
            return self.weight < other.weight

        def __repr__(self):
            return f"<Edge: {self.weight=}, {self.incident_node=}>"

    def __init__(self, data_input: List[Any, Any, int]):
        self.graph = {}
        self.n_vertex = 0

        for from_, to_, weight in data_input:
            node = self.add_or_get_node(from_)
            incident_node = self.add_or_get_node(to_)

            edge = self.Edge(incident_node, weight)

            node.edges.add(edge)
            incident_node.parents[node] = edge

    def add_or_get_node(self, value: Any) -> Node:
        """adding and returning a node"""

        if value not in self.graph:
            self.graph[value] = self.Node(value)
            self.n_vertex += 1

        return self.graph[value]

    def traverse(self, *, how="dfs") -> None:
        """
        wrapper for traversing all nodes of the graph

        :type how: str
        :values how: 'bfs', 'dfs', 'rdfs'
        """

        if how == "bfs":
            traverse_ = self._bfs
        elif how == "dfs":
            traverse_ = self._dfs_without_recur
        elif how == "rdfs":
            traverse_ = self._dfs_with_recur
        else:
            raise ValueError("invalid argument value")

        passed = set()
        for node in self.graph.values():
            if node not in passed:
                traverse_(node, passed)

    def _bfs(self, node: Node, passed: set) -> None:
        """breadth-first traversal with queue"""

        queue = Queue()
        queue.put(node)
        while not queue.empty():
            node = queue.get()
            passed.add(node)
            print(node)
            for edge in node.edges:
                if edge.incident_node not in passed:
                    queue.put(edge.incident_node)
                    passed.add(edge.incident_node)

    def _dfs_without_recur(self, node: Node, passed: set) -> None:
        """depth-first traversal without recursion"""

        stack = [node]
        while stack:
            node = stack[-1]
            if node not in passed:
                print(node)
                passed.add(node)
            has_children = False
            for edge in node.edges:
                if edge.incident_node not in passed:
                    stack.append(edge.incident_node)
                    has_children = True
                    break
            if not has_children:
                stack.pop()

    def _dfs_with_recur(self, node: Node, passed: set) -> None:
        """depth-first traversal with recursion"""

        print(node.value)
        passed.add(node)
        for edge in node.edges:
            if edge.incident_node not in passed:
                self._dfs_with_recur(edge.incident_node, passed)

    def _ore_theorem(self) -> bool:
        """verifies Ore's theorem"""

        if self.n_vertex < 3:
            return False

        for node1 in self.graph.values():
            for node2 in self.graph.values():
                if node1 != node2 and \
                    node2 not in node1.parents and \
                    node1 not in node2.parents and \
                        len(node1.edges) + len(node2.edges) < self.n_vertex:

                    return False

        return True

    def _weight_between_nodes(self, node: Node, adjacent_node: Node) -> int:
        """return weight between adjacent nodes"""

        if adjacent_node in node.parents:
            return node.parents[adjacent_node].weight

        if node in adjacent_node.parents:
            return node.parents[node].weight

        raise ValueError("nodes are not adjacent")

    def _nearest_not_passed_node(self, node: Node, passed: set) -> Node:
        """returns the nearest unmarked node"""

        edges_to_not_passed_nodes = filter(
            lambda edge: edge.incident_node not in passed,
            node.edges)

        edge_to_nearest_node = min(edges_to_not_passed_nodes)

        return edge_to_nearest_node.incident_node

    def find_hamiltonian_cycle(self, *, start_node=None) -> int:
        """finds a suboptimal Hamiltonian cycle"""

        if not self._ore_theorem():
            return 0

        if start_node is None:
            start_node = choice(list(self.graph.values()))

        route = f"{start_node}"
        route_len = 0

        cur_node = start_node
        passed = set()
        passed.add(cur_node)

        while len(passed) != self.n_vertex:
            nearest_node = self._nearest_not_passed_node(cur_node, passed)
            route_len += self._weight_between_nodes(nearest_node, cur_node)
            route += f" -> {nearest_node}"
            passed.add(nearest_node)
            cur_node = nearest_node

        route += f" -> {start_node}"
        route_len += self._weight_between_nodes(start_node, cur_node)
        print(route)
        return route_len


# data = [
#     [7, 6, 1],
#     [7, 2, 1],
#     [7, 5, 1],
#     [6, 4, 1],
#     [2, 1, 1],
#     [5, 9, 1],
#     [8, 10, 1]
# ]

# data = [
#     ['x1', 'x2', 1],
#     ['x1', 'x3', 1],
#     ['x1', 'x4', 1],
#     ['x2', 'x5', 1],
#     ['x3', 'x4', 1],
#     ['x3', 'x5', 1],
#     ['x4', 'x5', 1]
# ]
data = [
    ['A', 'B', 5],
    ['B', 'A', 5],
    ['A', 'C', 6],
    ['C', 'A', 6],
    ['A', 'D', 8],
    ['D', 'A', 8],
    ['B', 'C', 7],
    ['C', 'B', 7],
    ['B', 'D', 10],
    ['D', 'B', 10],
    ['C', 'D', 3],
    ['D', 'C', 3]
]

graph = Graph(data)
# graph.traverse(how="bfs")
print(graph.find_hamiltonian_cycle())
