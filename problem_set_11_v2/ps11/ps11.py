
# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import Digraph, Edge, Node, weightedEdge

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#
# Each building will be a node, each route between will be a weighted edge with two weight factors (total distance
# and outdoors distance)
#
# Then we can do the minimisation functions on these weight factors.

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """

    print "Loading map from file..."

    with open(mapFilename, mode='r') as f:
        lines = f.read().splitlines()

    loc_list = []
    for l in lines:
        loc_list.append(l.split(" "))

    # now lets build the graph using this list
    mit_map = Digraph()
    for l in loc_list:
        # instantiate nodes
        src_node = Node(l[0])
        dest_node = Node(l[1])

        # instantiate edge
        edge = weightedEdge(src_node, dest_node, l[2], l[3])

        try:
            # add source to map
            mit_map.addNode(src_node)

        except ValueError:
            pass

        try:
            # add dest to map
            mit_map.addNode(dest_node)

        except ValueError:
            pass

        mit_map.addEdge(edge)
#
    return mit_map


# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#

def bruteForceSearch_rec(digraph, start, end, maxTotalDist, maxDistOutdoors, visited = []):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """

    ## recursive pseudocode:
    # procedure
    # DFS(G, v):
    # label v as discovered
    #   for all edges from v to w in G.adjacentEdges(v) do
    #       if vertex w is not labeled as discovered
    # then recursively call DFS(G, w)
    # pass


    # we don't need to keep track of discovered because we have a constraint for the longest dist
    # see if we are at the end node (this is the base case)
    path = [str(start)]
    shortestPath = None
    visited = visited + [start]
    if start == end:
        # print "Base case. End of search tree."
        return path

    # print "Start of loop, current node is: " + str(path)
    # we are not at the end node, so look at all the edges we could traverse
    for e in digraph.childrenOf(start):
        # print "Our current shortest path is: " + str(shortestPath)
        # print "Inspect edge: " + str(e)
        # have we visited this node already?
        if e.getDestination() not in visited:
            # print "We haven't visited the destination: " + str(e.getDestination())
            # # print visited
            # lets check if we have distance left to explore

            if maxTotalDist >= e.getTotalDistance() and maxDistOutdoors >= e.getOutdoorsDistance():
                # print "We haven't gotten tired yet, so lets go into the next recursion loop."
                # we still do so lets go to the each of the next nodes and explore
                newpath = bruteForceSearch_rec(digraph, start=e.getDestination(), end=end,
                                 maxTotalDist=maxTotalDist-e.getTotalDistance(),
                                 maxDistOutdoors=maxDistOutdoors-e.getOutdoorsDistance(), visited=visited)

                # print "Our new path is: " + str(newpath)
                if newpath is not None:
                    # now lets check if the new path we found was the shortest
                    if shortestPath is None or getPathLength(digraph, newpath) < getPathLength(digraph, shortestPath):
                        shortestPath = newpath
                        # print "Our new shortestPath is: " + str(shortestPath)


        # else:
            # print "Already visited, ignoring."

    if shortestPath is None:
        path = None
    else:
        path = path + shortestPath

    # print "Returning current shortestPath: " + str(shortestPath)
    return path


def getPathLength(digraph, path):
    """
    A helper function which takes in a digraph and a list of nodes and calculates the total distance
    :param digraph:
    :param path:
    :return:
    """

    distance = 0
    outdoors = 0
    try:
        for n in range(len(path) - 1):

            tmp_td, tmp_od = digraph.getDistance(Node(path[n]), Node(path[n+1]))

            distance += tmp_td
            outdoors += tmp_od

        return distance

    except TypeError:

        return distance

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    the govenring function for the bruteForceSearch
    :param digraph:
    :param start:
    :param end:
    :param maxTotalDist:
    :param maxDistOutdoors:
    :return:
    """
    start_node = Node(start)
    end_node = Node(end)
    shortestPath = bruteForceSearch_rec(digraph, start_node, end_node, maxTotalDist, maxDistOutdoors)

    if shortestPath is None:
        raise ValueError
    else:
        return shortestPath

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS_rec(digraph, start, end, maxTotalDist, maxDistOutdoors, visited = [], memo = {}):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    path = [str(start)]
    shortestPath = None
    visited = visited + [start]
    if start == end:
        # print "Base case. End of search tree."
        return path

    # print "Start of loop, current node is: " + str(path)
    # we are not at the end node, so look at all the edges we could traverse
    for e in digraph.childrenOf(start):
        # print "Our current shortest path is: " + str(shortestPath)
        # print "Inspect next node: " + str(e)
        # have we visited this node already?
        if e.getDestination() not in visited:

            if maxTotalDist >= e.getTotalDistance() and maxDistOutdoors >= e.getOutdoorsDistance():

                try:

                    # see if our path is already in the memo
                    newpath = memo[e.getDestination(), end]
                    # print "Path in memo, end of search tree. " + str(newpath)

                except:

                    # its not, so we have to iterate
                    #     print "Max Outdoors Distance: " + str(maxDistOutdoors)
                    #     print "Outdoors distance: " + str(e.getOutdoorsDistance())
                        # we still do so lets go to the each of the next nodes and explore
                        newpath = directedDFS_rec(digraph, start=e.getDestination(), end=end,
                                                   maxTotalDist=maxTotalDist - e.getTotalDistance(),
                                                   maxDistOutdoors=maxDistOutdoors - e.getOutdoorsDistance(),
                                                    visited=visited, memo=memo)


                # print "Our newpath is: " + str(newpath)
                # now lets check if the new path we found was the shortest
                if newpath is not None:
                    if (shortestPath is None) or (getPathLength(digraph, newpath) < getPathLength(digraph, shortestPath)):
                        # print "Newpath length: " + str(getPathLength(digraph, newpath))
                        # print "Shortest path length: " + str(getPathLength(digraph, shortestPath))
                        shortestPath = newpath
                        memo[e.getDestination(), end] = newpath
                        # print "New shortest path: " + str(shortestPath)

            else:
                # print "Too much outdoors distance! Not a valid path."
                newpath = None

        else:
            pass
            # print "Already visited, ignore."

    if shortestPath is None:
        path = None
    else:
        path = path + shortestPath

    # print "Returned path from this recursion is: " + str(path)
    return path


def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Parent function for directedDFS
    :param digraph:
    :param start:
    :param end:
    :param maxTotalDist:
    :param maxDistOutdoors:
    :param visited:
    :param memo:
    :return:
    """

    start_node = Node(start)
    end_node = Node(end)
    new_memo = {}
    shortestPath = directedDFS_rec(digraph, start_node, end_node, maxTotalDist, maxDistOutdoors, memo=new_memo)

    if shortestPath is None:
        raise ValueError
    else:
        return shortestPath

# Uncomment below when ready to test
if __name__ == '__main__':
   # Test cases
   digraph = load_map("mit_map.txt")

   LARGE_DIST = 1000000

   print digraph
   #
   # # Test case 1
   print "---------------"
   print "Test case 1:"
   print "Find the shortest-path from Building 32 to 56"
   expectedPath1 = ['32', '56']
   brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
   dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
   print "Expected: ", expectedPath1
   print "DFS: ", dfsPath1
   print "Brute-force: ", brutePath1

   # Test case 2
   print "---------------"
   print "Test case 2:"
   print "Find the shortest-path from Building 32 to 56 without going outdoors"
   expectedPath2 = ['32', '36', '26', '16', '56']
   brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
   dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
   print "Expected: ", expectedPath2
   print "Brute-force: ", brutePath2
   print "DFS: ", dfsPath2
   #
   # Test case 3
   print "---------------"
   print "Test case 3:"
   print "Find the shortest-path from Building 2 to 9"
   expectedPath3 = ['2', '3', '7', '9']
   brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
   dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
   print "Expected: ", expectedPath3
   print "Brute-force: ", brutePath3
   print "DFS: ", dfsPath3

   # # Test case 4
   print "---------------"
   print "Test case 4:"
   print "Find the shortest-path from Building 2 to 9 without going outdoors"
   expectedPath4 = ['2', '4', '10', '13', '9']
   brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
   dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
   print "Expected: ", expectedPath4
   print "Brute-force: ", brutePath4
   print "DFS: ", dfsPath4
   #
   ## Test case 5
   print "---------------"
   print "Test case 5:"
   print "Find the shortest-path from Building 1 to 32"
   expectedPath5 = ['1', '4', '12', '32']
   brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
   dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
   print "Expected: ", expectedPath5
   print "Brute-force: ", brutePath5
   print "DFS: ", dfsPath5
   # #
   # # Test case 6
   print "---------------"
   print "Test case 6:"
   print "Find the shortest-path from Building 1 to 32 without going outdoors"
   expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
   brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
   dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
   print "Expected: ", expectedPath6
   print "Brute-force: ", brutePath6
   print "DFS: ", dfsPath6
   #
   # # # Test case 7
   print "---------------"
   print "Test case 7:"
   print "Find the shortest-path from Building 8 to 50 without going outdoors"
   bruteRaisedErr = 'No'
   dfsRaisedErr = 'No'
   try:
       bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
   except ValueError:
       bruteRaisedErr = 'Yes'

   try:
       directedDFS(digraph, '8', '50', LARGE_DIST, 0)
   except ValueError:
       dfsRaisedErr = 'Yes'

   print "Expected: No such path! Should throw a value error."
   print "Did brute force search raise an error?", bruteRaisedErr
   print "Did DFS search raise an error?", dfsRaisedErr

   # Test case 8
   print "---------------"
   print "Test case 8:"
   print "Find the shortest-path from Building 10 to 32 without walking"
   print "more than 100 meters in total"
   bruteRaisedErr = 'No'
   dfsRaisedErr = 'No'
   try:
       bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
   except ValueError:
       bruteRaisedErr = 'Yes'

   try:
       directedDFS(digraph, '10', '32', 100, LARGE_DIST)
   except ValueError:
       dfsRaisedErr = 'Yes'

   print "Expected: No such path! Should throw a value error."
   print "Did brute force search raise an error?", bruteRaisedErr
   print "Did DFS search raise an error?", dfsRaisedErr