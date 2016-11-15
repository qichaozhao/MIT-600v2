# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)


class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    def __str__(self):
        return str(self.src) + '->' + str(self.dest)


class weightedEdge(Edge):
    """
    Adding weights to our graph
    """

    def __init__(self, src, dest, tot_dist, out_dist):
        Edge.__init__(self, src, dest)

        self.tot_dist = int(tot_dist)
        self.out_dist = int(out_dist)

    def getTotalDistance(self):
        return self.tot_dist

    def getOutdoorsDistance(self):
        return self.out_dist

    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + ' :: Weights :: Total: ' + str(
            self.tot_dist) + ' :: Outside: ' + str(self.out_dist)


class Digraph(object):
    """
    A directed graph
    """

    def __init__(self):
        self.nodes = set([])
        self.edges = {}

    def addNode(self, node):

        # print "Existing nodes: " + str(self.nodes)
        # print "Trying to add node: " + str(node)

        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []

        # print "New set of nodes: " + str(self.nodes)

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()

        # print self.nodes

        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(edge)
        # print self.edges[src]

    def childrenOf(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.nodes

    def getDistance(self, node1, node2):

        for edge in self.edges[node1]:
            if edge.getDestination() == node2:

                return edge.getTotalDistance(), edge.getOutdoorsDistance()

        raise ValueError("Could not get distance")

    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(d.getSource()) + '->' + str(d.getDestination()) + ' :: Weights :: Total: ' + str(
                    d.getTotalDistance()) + ' :: Outside: ' + str(d.getOutdoorsDistance()) + '\n'
        return res[:-1]
