from typing import List
from collections import defaultdict

class Node:
    def __init__(self, value: tuple):
        self.value = value
        self.edges = set()
        # self.parents = {}


class Edge:
    def __init__(self, adjacentNode: Node, weight: int):
        self.adjacentNode = adjacentNode
        self.weight = weight


class Graph:
    def __init__(self, input: List[list]):
        self.graph = {}

        for from_, to_, weight in input:
            node = self.add_or_get_node(from_)
            adjacentNode = self.add_or_get_node(to_)

            edge = Edge(adjacentNode, weight)
            node.edges.add(edge)

            edge = Edge(node, weight)
            adjacentNode.edges.add(edge)

    def add_or_get_node(self, value):
        if value not in self.graph:
            self.graph[value] = Node(value)
        return self.graph[value]

    def dfs(self):
        passed = set()
        for node_value in self.graph:
            if node_value not in passed:
                self._dfs_without_recur(self.graph[node_value], passed)

    def _dfs_without_recur(self, node: Node, passed: set):
        stack = [node.value]
        while stack:
            node_value = stack[-1]
            if node_value not in passed:
                print(node_value)
                passed.add(node_value)
            hasChildren = False
            for edge in self.graph[node_value].edges:
                if edge.adjacentNode.value not in passed:
                    stack.append(edge.adjacentNode.value)
                    hasChildren = True
                    break
            if not hasChildren:
                stack.pop()

    def _dfs_with_recur(self, node: Node, passed: set):
        print(node.value)
        passed.add(node.value)
        for edge in node.edges:
            if edge.adjacentNode.value not in passed:
                self._dfs_with_recur(edge.adjacentNode, passed)

data = \
[
    [7, 6, 1],
    [7, 2, 1],
    [7, 5, 1],
    [6, 4, 1],
    [2, 1, 1],
    [5, 9, 1],
    [8, 10, 1]
]

graph = Graph(data)
graph.dfs()
