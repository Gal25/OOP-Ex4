from src.API.GraphInterface import GraphInterface
from src.API.Node import Node
# from src.Node import Node


class DiGraph(GraphInterface):

    def __init__(self):
        self.sizeEdges = 0
        self.sizeNodes = 0
        self.nodes = {}
        self.edges = {}
        self.mc = 0


    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return self.sizeNodes

    def e_size(self) -> int:

       return self.sizeEdges

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        if id1 not in self.nodes:
            return {}
        in_dict = {}
        for i, j in self.edges.items():
            if id1 in j:
                in_dict[i] = j[id1]
        return in_dict


    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        if id1 not in self.nodes:
            return {}
        return self.edges[id1]


    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 in self.nodes and id2 in self.nodes:
            if id2 not in self.edges[id1]:
                if self.edges[id1] is None:
                    self.edges[id1] = {}
                    self.edges[id1][id2] = weight
                else:
                    self.edges[id1][id2] = weight
                    self.sizeEdges += 1
                    self.mc += 1
                    self.nodes[id1].e_out += 1
                    self.nodes[id2].e_in += 1
                    return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id in self.nodes:
            return False
        n = Node(key=node_id, location=pos)
        self.nodes[node_id] = n
        self.edges[node_id] = {}
        self.mc += 1
        self.sizeNodes += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id not in self.nodes:
            return False
        else:
            self.sizeEdges -= len(self.edges[node_id])
            self.mc += len(self.edges[node_id])
            del (self.edges[node_id])
            for k in self.all_in_edges_of_node(node_id).keys():
                self.remove_edge(k, node_id)
            self.nodes.pop(node_id)
            self.sizeNodes -= 1
            self.mc += 1
            return True


    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 in self.nodes and node_id2 in self.nodes:
            if node_id2 in self.edges[node_id1]:
                self.edges[node_id1].pop(node_id2)
                self.sizeEdges -= 1
                self.mc += 1
                self.nodes[node_id1].e_out -= 1
                self.nodes[node_id2].e_in -= 1
                return True
        return False

    def getNode(self, node_id: int) -> Node:
        """
        :param node_id:
        :return: the node with the node_id
        """
        return self.nodes[node_id]

    def __repr__(self):
        return f"Graph: |V| = {self.v_size()}, |E| = {self.e_size()}"