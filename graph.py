from typing import List


class Node:
    def __init__(self, value: int):
        self.value = value
        self.edges = set()
        self.parents = {}

class Edge:
    def __init__(self, adjacentNode: Node, weight: int):
        self.adjacentNode = adjacentNode
        self.weight = weight


class Graph:
    def __init__(self, input: List[List[int]]):
        for from_, to_, weight in input:
            pass

    def add_edge(self, value: int):
        Node(value)
        pass
    
    def add_node(self):
        pass
