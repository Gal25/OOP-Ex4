import math
import sys


class Node:

    def __init__(self, key : int , location : tuple= None, tag: int= 0, weight: float = sys.maxsize ):
        self.key = key
        self.location = location
        self.tag = tag
        self.weight = weight
        self.e_out = 0
        self.e_in = 0

    def getOut(self):
        return self.e_out

    def setOut(self, edge_out):
        self.e_out = edge_out

    def getIn(self):
        return self.e_in

    def setIn(self, edge_in):
        self.e_in = edge_in

    def getkey(self):
        return self.key

    def setKey(self, key: int):
        self.key = key

    def getTag(self):
        return self.tag

    def setTag(self, tag: int):
        self.tag = tag

    def getWeight(self):
        return self.weight

    def setWeight(self, w: int):
        self.weight = w

    def getLocation(self):
        return self.location

    def setLocation(self, l):
        self.location = l

    def __repr__(self):
        return f"{self.key}: |edges out| {self.e_out} |edges in| {self.e_in}"