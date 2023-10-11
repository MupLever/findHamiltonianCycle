from typing import List
from queue import Queue
# from random import choice


class Graph:
    """an undirected graph class implemented through a dictionary"""

    class Node:
        """node class storing node value and incident edges"""

        def __init__(self, value: int):
            self.value = value
            self.edges = set()
            # self.parents = {}

        def __ne__(self, other):
            return self.value != other.value

        def __eq__(self, other):
            return self.value == other.value

    class Edge:
        """edge class storing the incident node"""

        def __init__(self, adjacent_node, weight: int):
            self.adjacent_node = adjacent_node
            self.weight = weight

        def __lt__(self, other):
            return self.weight < other.weight

    def __init__(self, data_input: List[list]):
        self.graph = {}
        self.n_vertex = 0

        for from_, to_, weight in data_input:
            node = self.add_or_get_node(from_)
            adjacent_node = self.add_or_get_node(to_)
            self.add_node(node, adjacent_node, weight)

    def add_or_get_node(self, value: int) -> Node:
        """adding and returning a node"""

        if value not in self.graph:
            self.graph[value] = self.Node(value)
            self.n_vertex += 1
        return self.graph[value]

    def add_node(self, from_node: int, to_node: int, weight: int) -> None:
        """adding an edge between from_node and to_node"""

        edge = self.Edge(from_node, weight)
        to_node.edges.add(edge)

        edge = self.Edge(to_node, weight)
        from_node.edges.add(edge)

    def traverse(self, *, how="dfs") -> None:
        """
        depth-first traversal of all nodes
        :type how: str
        :values how: 'bfs', 'dfs', 'rdfs'
        """

        if how == "bfs":
            traverse_ = self._bfs
        elif how == "dfs":
            traverse_ = self._dfs_with_recur
        elif how == "rdfs":
            traverse_ = self._dfs_without_recur
        else:
            raise ValueError("invalid argument value")

        passed = set()
        for value, node in self.graph.items():
            if value not in passed:
                traverse_(node, passed)

    def _bfs(self, node: Node, passed: set):
        """breadth-first traversal with queue"""

        queue = Queue()
        queue.put(node.value)
        while not queue.empty():
            node_value = queue.get()
            passed.add(node_value)
            print(node_value)
            for edge in self.graph[node_value].edges:
                if edge.adjacent_node.value not in passed:
                    queue.put(edge.adjacent_node.value)
                    passed.add(edge.adjacent_node.value)

    def _dfs_without_recur(self, node: Node, passed: set) -> None:
        """depth-first traversal without recursion"""

        stack = [node.value]
        while stack:
            node_value = stack[-1]
            if node_value not in passed:
                print(node_value)
                passed.add(node_value)
            has_children = False
            for edge in self.graph[node_value].edges:
                if edge.adjacent_node.value not in passed:
                    stack.append(edge.adjacent_node.value)
                    has_children = True
                    break
            if not has_children:
                stack.pop()

    def _dfs_with_recur(self, node: Node, passed: set) -> None:
        """depth-first traversal with recursion"""

        print(node.value)
        passed.add(node.value)
        for edge in node.edges:
            if edge.adjacent_node.value not in passed:
                self._dfs_with_recur(edge.adjacent_node, passed)

    def _dirac_theorem(self) -> bool:
        """verifies Dirac's theorem"""

        if self.n_vertex < 3:
            return False

        for value1, node1 in self.graph.items():
            for value2, node2 in self.graph.items():
                if value1 != value2:
                    incidental_nodes = map(lambda edge: edge.adjacent_node,
                                           node2.edges)
                    if node1 not in incidental_nodes:
                        if len(node1.edges) + len(node2.edges) < self.n_vertex:
                            return False

        return True

    def _weight_between_nodes(self, node: Node, adjacent_node: Node) -> int:
        """return weight between adjacent nodes"""

        for edge in node.edges:
            if edge.adjacent_node == adjacent_node:
                return edge.weight

        raise ValueError("nodes are not adjacent")

    def find_hamiltonian_cycle(self) -> int:
        """finds a suboptimal Hamiltonian cycle"""

        if not self._dirac_theorem():
            return 0

        # start_node = choice(self.graph.values())
        start_node_value = 'D'
        route = f"{start_node_value}"
        route_len = 0
        cur_node_value = start_node_value
        passed = set(cur_node_value)
        while len(passed) != self.n_vertex:
            edges_to_not_passed_nodes = filter(
                lambda edge: edge.adjacent_node.value not in passed,
                self.graph[cur_node_value].edges)

            edge_to_nearest_node = min(edges_to_not_passed_nodes)
            route_len += edge_to_nearest_node.weight
            nearest_node_value = edge_to_nearest_node.adjacent_node.value
            route += f"-> {nearest_node_value}"
            passed.add(nearest_node_value)
            cur_node_value = nearest_node_value
        route += f"-> {start_node_value}"
        route_len += self._weight_between_nodes(self.graph[start_node_value],
                                                self.graph[cur_node_value])
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
    ['A', 'C', 6],
    ['A', 'D', 8],
    ['B', 'C', 7],
    ['B', 'D', 10],
    ['C', 'D', 3]
]

graph = Graph(data)
# graph.traverse(how="bfs")
print(graph.find_hamiltonian_cycle())
