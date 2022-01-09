import json
import math
import random
import sys
from heapq import heappop, heappush
import queue
from types import SimpleNamespace
from typing import List

from src.API.GraphInterface import GraphInterface
from src.API.GraphAlgoInterface import GraphAlgoInterface
from src.API.DiGraph import DiGraph
from src.API.GraphInterface import GraphInterface
import matplotlib.pyplot as plt

from src.API.Node import Node


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph: DiGraph = None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
       """
        # dictionary
        g = DiGraph()
        text_file = json.loads(file_name, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        for node in text_file.Nodes:
            curr_pos = []
            posS = node.pos.split(',')
            for i in posS:
                curr_pos.append(float(i))
            g.add_node(node.id, tuple(curr_pos))
        for edge in text_file.Edges:
            g.add_edge(edge.src, edge.dest, edge.w)
        self.graph = g
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            dict = {'Edges': [], 'Nodes': []}
            for key, node in self.graph.get_all_v().items():
                dict['Nodes'].append({'pos': str(
                    str(node.getLocation()[0]) + ',' + str(node.getLocation()[1]) + ',' + str(node.getLocation()[2])),
                    'id': key})

            for src in self.graph.get_all_v().keys():
                for dest, w in self.graph.all_out_edges_of_node(src).items():
                    dict['Edges'].append({'src': src, 'w': w, 'dest': dest})

            with open(file_name, 'w') as file:
                json.dump(dict, fp=file, indent=4)
                return True
        except Exception as e:
            print(e)
        return False

    def nodes_data_pos(self, node_num):
        """
        This function return the geolocation of a specific node.
        :param node_num:
        :return:
        """
        for i, n in self.graph.get_all_v().items():
            if i == node_num:
                return n.getLocation()

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Example:
    #      >>> from GraphAlgo import GraphAlgo
    #       >>> g_algo = GraphAlgo()
    #        >>> g_algo.addNode(0)
    #        >>> g_algo.addNode(1)
    #        >>> g_algo.addNode(2)
    #        >>> g_algo.addEdge(0,1,1)
    #        >>> g_algo.addEdge(1,2,4)
    #        >>> g_algo.shortestPath(0,1)
    #        (1, [0, 1])
    #        >>> g_algo.shortestPath(0,2)
    #        (5, [0, 1, 2])
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        queue = []  # this heapq will have 2 values in index: (distance, node)

        the_list = {id1: [id1]}
        visited = {}
        value = {}

        # if the vertex does not exists in the list of nodes in current graph
        if id1 not in self.graph.get_all_v().keys():
            return float('inf'), []

        heappush(queue, (0, id1))
        while queue:
            (dist, ver) = heappop(queue)
            value[ver] = dist
            if ver == id2:
                break

            for key, edge in self.graph.all_out_edges_of_node(ver).items():
                curr = value[ver] + edge
                if key not in visited or curr < visited[key]:
                    visited[key] = curr
                    heappush(queue, (curr, key))
                    if ver not in the_list:
                        the_list[ver] = [ver]
                    the_list[key] = the_list[ver] + [key]

        visited[id1] = 0
        if id2 not in value and id2 not in the_list:
            return float('inf'), []

        return value[id2], the_list[id2]

    def algorithm_of_Dijkstra(self, src: Node):
        """
           This function representing the Dijkstra's algorithm.
           Solves the problem of finding the easiest route from point in graph to destination in weighted graph.
           It is possible to find using this algorithm, at this time, the fast paths to all the points in the graph.
           The algorithm calculates the weights of the nodes with the desired edges each time and compares them.
           According to the algorithm we get the path with the lowest weight, we used it in TSP function
           Link: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
           Complexity: (O(V+E)), |V|=number of nodes, |E|=number of edges.
            :param src: src the source node
        """
        visited = {}
        q = queue.PriorityQueue()
        for node in self.get_graph().get_all_v().values():
            node.setWeight(sys.maxsize)
            visited[node.key] = False

        src.setWeight(0)
        q.put(src)

        while q.qsize() != 0:
            current = q.get()
            if visited.get(current.key) is False:
                for id, w in self.graph.all_out_edges_of_node(current.key).items():
                    node = self.graph.nodes.get(id)
                    dist = w + current.weight
                    if dist < node.weight:
                        node.setWeight(dist)
                        q.put(Priority(node.weight, node.key))
            visited[current.key] = True

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
            Finds the shortest path that visits all the nodes in the list
            we used with dijkstra algorithm
            :param node_lst: A list of nodes id's
            :return: A list of the nodes id's in the path, and the overall distance
        """
        TSP = []
        node_lst_copy = []
        minDist = sys.maxsize
        TSP_temp = []
        minNode = 0
        stop = True

        for node in range(len(node_lst)):
            node_lst_copy.extend(node_lst)
            curr = node_lst_copy[node]
            pos = node
            new = True
            while len(node_lst_copy) > 1:

                minVal = sys.maxsize
                key = node_lst_copy[pos]
                node_lst_copy.remove(key)
                self.algorithm_of_Dijkstra(self.graph.get_all_v()[key])

                # find the minimum value of the path's weight using with dijkstra algorithm
                for copy in range(len(node_lst_copy)):
                    temp = self.graph.get_all_v()[node_lst_copy[copy]].getWeight()
                    if minVal > temp:
                        minVal = temp
                        curr = node_lst_copy[copy]
                        pos = copy

                path = self.shortest_path(key, curr)[1]  # take the shortest path

                # put just one node in the path's list
                if not new:
                    path.pop(0)
                new = False

                if minVal == sys.maxsize:
                    stop = False
                    break

                # add all the min
                minNode += minVal
                TSP_temp.extend(path)  # put the TSP path

            if stop:

                if minDist > minNode:
                    minDist = minNode
                    TSP.extend(TSP_temp)

        return TSP, minDist

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """

        center_path = sys.maxsize
        center = None

        for i in range(self.graph.sizeNodes):
            temp = self.findTheLongestPath(i)
            if temp == float('inf'):
                return None, float('inf')
            if temp < center_path:
                center_path = temp
                center = self.graph.get_all_v()[i]

        return center.getkey(), center_path

    def findTheLongestPath(self, id1) -> float:
        temp = 0
        for j in range(self.graph.sizeNodes):
            path = self.shortest_path(id1, j)[0]

            if path == math.inf:
                return float('inf')
            if temp < path:
                temp = path

        return temp


class Priority:
    # This class aims to put in the queue the vertices in relation to their weight

    def __init__(self, weight, key):
        self.weight = weight
        self.key = key

    def __lt__(self, other):
        return self.weight < other.weight
