# 6.00x Problem Set 10
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# 1.load the campus map datas from file .
# 2.parse datas from file to build a graph.


# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

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
    # TODO
    print "Loading map from file..."
    infile = open('mit_map.txt', 'r')
    graph = WeightedDigraph() 
    # parse data
    for line in infile:
        datas = line.split()
        src , dest, totalDistance, distanceOutdoors = datas
        src_node = Node(src)
        dest_node = Node(dest)
        src_in_graph = False
        dest_in_graph = False

        for n in graph.nodes:
            node_name = n.getName()
            if src == node_name:
                src_node = n
                src_in_graph = True
            if dest == node_name:
                dest_node = n
                dest_in_graph = True

        if not src_in_graph:
            graph.addNode(src_node)
        if not dest_in_graph:
            graph.addNode(dest_node)
        edge = WeightedEdge(src_node, dest_node, int(totalDistance), int(distanceOutdoors))
        graph.addEdge(edge)

    return graph


#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def get_node_from(digraph, *node_name):
    """(graph, str1,...) -> (Node1, ...)

    return node object from digraph according to node name
    """
    nodes = []
    node_number = len(node_name)

    for name in node_name:
        for n in digraph.nodes:
            if name == n.getName():
                nodes.append(n)
    return nodes

def dfs(digraph, start, end, path=[]):
    """
    (graph, node, node, int, int, list) -> list of path
    reutrn all path from start to end in graph
    """
    path = path + [start]
    if start == end:
        return [path]
    # if not graph.has_key(start):
    #     return []
    paths = []
    for node in digraph.childrenOf(start):
        if node not in path:
            newpaths = dfs(digraph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def compute_weight(graph, path):
    """
    (nodes of list, int, int) -> float
    return the weight of path
    """    
    total_dist = 0
    dis_outdoor = 0
    for i in range(len(path) - 1):
        src = path[i]
        next = path[i + 1]
        for dest, (dis, out) in graph.edges[src]:
            if dest == next:
                total_dist += dis
                dis_outdoor += out

    return total_dist, dis_outdoor

def filter_(paths, maxTotalDist, maxDistOutdoors, graph):
    """
    get path(s) that satisfy constraint.
    """
    after_outdoors_paths = []
    # first, filter path according to maxDistOutdoors
    for path in paths:
        total_dist, dis_outdoor = compute_weight(graph, path)
        if dis_outdoor <= maxDistOutdoors:
            after_outdoors_paths.append(path)

    after_total_paths = []

    if after_outdoors_paths:
        for path in after_outdoors_paths:
            total_dist, dis_outdoor = compute_weight(graph, path)
            if total_dist <= maxTotalDist:
                after_total_paths.append(path)

    if after_total_paths:
        shortest_path = after_total_paths[0]
        for path in after_total_paths:
            shortest_path_dist, shortest_path_ourdoor = compute_weight(graph, shortest_path)
            total_dist, dis_outdoor = compute_weight(graph, path)
            if shortest_path_dist > total_dist:
                shortest_path = path
        return shortest_path

    return after_total_paths

def translate(path):
    return [node.getName() for node in path]


def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

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
    #TODO

    # get the start_node and end_node from digraph.nodes.
    start_node, end_node = get_node_from(digraph, start, end)

    # find all path from start to end
    paths = dfs(digraph, start_node, end_node)

    # find the shortest path in paths.
    shortest_path = filter_(paths, maxTotalDist, maxDistOutdoors, digraph)

    if not shortest_path:
        raise ValueError()

    # translate Node to str
    shortest_path = translate(shortest_path)

    return  shortest_path

    




#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

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
    #TODO
    pass

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    # Test cases
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges
    
    print "--------------"
    path1 = get_node_from(mitMap, '32', '36', '26', '16', '56')
    path2 = get_node_from(mitMap, '32', '36', '34', '38', '39', '37',
                          '35', '33', '9', '7', '3', '10', '4', '2',
                          '6', '8', '16', '56')
    print compute_weight(mitMap, path1)
    print compute_weight(mitMap, path2)

    LARGE_DIST = 1000000

    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr
