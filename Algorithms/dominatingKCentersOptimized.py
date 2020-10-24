import sys, os, time
import networkx as nx
import sys, os, time
import networkx as nx
from networkx.utils import arbitrary_element

import sys, os, time
import networkx as nx
from random import randrange
import operator



def findBestNextColor(g, totalNodes, blackNodes, whiteNodes, currentDominating):
    maxNeighborhood = 0
    candidate = None
    for x in totalNodes-currentDominating:
        currentLen = len(set(g[x]).intersection(blackNodes))
        if currentLen > maxNeighborhood: 
            candidate = x
            maxNeighborhood = currentLen
    return candidate or totalNodes.pop()






def findKCentersColors(G, k, shortestPaths, startWith):
    allNodes = set(G)
    kCenters = set()
    nodeDict = {}
    for x in allNodes: 
        nodeDict[x] = float("inf")
    k = k - 1
    nodeDict[startWith] = 0
    newCenter = startWith
    kCenters.add(newCenter)
    # print("newcenter", newCenter)
    blackNodes = set(G)
    whiteNodes = set()
    whiteNodes.add(newCenter)
    blackNodes -= set(g[newCenter])
    blackNodes -= {newCenter}
    for x in set(g[newCenter]):
        whiteNodes.add(x)
    while k != 0:
        for node in allNodes-kCenters:
            if nodeDict[node] > shortestPaths[node][newCenter]: 
                nodeDict[node] = shortestPaths[node][newCenter]
        newCenter = findBestNextColor(g, allNodes, blackNodes, whiteNodes, kCenters)
        if not newCenter: 
            return
        blackNodes -= set(g[newCenter]) 
        blackNodes -= {newCenter}
        for x in set(g[newCenter]):
            whiteNodes.add(x)
        whiteNodes.add(newCenter)
        nodeDict[newCenter] = 0
        kCenters.add(newCenter)
        k = k-1
    return kCenters, max(nodeDict.values())

def findKCentersColorsEdgeNodes(G, k, shortestPaths, edgeNodes):
    allNodes = set(G)
    kCenters = set()
    nodeDict = {}
    for x in allNodes: 
        nodeDict[x] = float("inf")
    k = k - 1
    blackNodes = set(G)
    whiteNodes = set()

    for y in edgeNodes:
        whiteNodes.add(y)
        blackNodes -= set(g[y])
        blackNodes -= {y}
        for x in set(g[y]):
            whiteNodes.add(x)
        kCenters.add(y)
        nodeDict[y] = 0
    for node in allNodes-kCenters:
        for center in kCenters:
            if nodeDict[node] > shortestPaths[node][center]: 
                nodeDict[node] = shortestPaths[node][center]

    k = k - len(edgeNodes)
    while k != 0:
        newCenter = findBestNextColor(g, allNodes, blackNodes, whiteNodes, kCenters)
        if not newCenter: 
            return
        for node in allNodes-kCenters:
            if nodeDict[node] > shortestPaths[node][newCenter]: 
                nodeDict[node] = shortestPaths[node][newCenter]
        blackNodes -= set(g[newCenter])
        blackNodes -= {newCenter}
        for x in set(g[newCenter]):
            whiteNodes.add(x)
        whiteNodes.add(newCenter)
        nodeDict[newCenter] = 0
        kCenters.add(newCenter)
        k = k-1
        print("allNodes", allNodes)
        print("kcenters", kCenters)
        print(nodeDict)
    return kCenters, max(nodeDict.values())


def getNodeWithMostNeighbors(g): 
    allNodes = set(g) 
    startWith =  None
    maxNeighborhood = 0
    for x in allNodes: 
        if len(g[x]) > maxNeighborhood:
            startWith = x
            maxNeighborhood = len(g[x])
    return startWith

def getRandomNode(g):
    allNodes = set(g) 
    n = len(g.nodes)
    l = randrange(n)
    j = 0
    startWith =  None
    for x in allNodes: 
        if j == l:
            startWith = x
            break
        j = j+1
    return startWith



def orderNodesByDegree(g, i):
    L = [val for (node, val) in g.degree()]
    minimum = min(L)
    nodes = [node for (node, val) in g.degree() if val == minimum]
    return nodes

def getEdgeNodes(g): 
    allNodes = set(g)
    edgeNodes = set()
    for y in allNodes:
        if len(g[y])==1:
            for x in g[y]: 
                edgeNodes.add(x)
    return edgeNodes or getRandomNode(g)


def callKcenters(g):
    n = len(g.nodes)
    shortestPaths = dict(nx.all_pairs_shortest_path_length(g))
    for i in range(1, n):
        kCenters, d = findKCentersColors(g, i, shortestPaths, getNodeWithMostNeighbors(g))
        if d == 1:
            print("findKCentersColors MOST NEIGHBORS")
            return kCenters
  


        # iterations = 10



def dominant(g):
    bestDominating = callKcenters(g)
    bestLenght = len(bestDominating)
    totalNodes = set(g)
    currentDominatingColors = set()
    blackNodes = totalNodes
    whiteNodes = set()
    while blackNodes:
        v = findBestNextColor(g, totalNodes, blackNodes, whiteNodes,currentDominatingColors)
        currentDominatingColors.add(v)
        blackNodes -= set(g[v])
        blackNodes -= {v}
        for x in set(g[v]):
            whiteNodes.add(x)
        whiteNodes.add(v)


    if len(currentDominatingColors) < bestLenght: 
        bestDominating = currentDominatingColors
        bestLenght = len(bestDominating)
        # print("choose Colors")

    


    # print(nx.is_dominating_set(g, bestDominating))
    return bestDominating






if __name__=="__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # input dir
    if not os.path.isdir(input_dir):
	    print(input_dir, "doesn't exist")
	    exit()

    # output dir
    if not os.path.isdir(output_dir):
	    print(input_dir, "doesn't exist")
	    exit()       
	
    # response file
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # importe graph
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))
        
        # calculate dominating graph
        D = sorted(dominant(g), key=lambda x: int(x))
        # add to response
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')
        
    output_file.close()
