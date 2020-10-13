import sys, os, time
import networkx as nx

#Given a graph G and a integer i, we find i centers that minimize the maximum distance of a node to one center 
#Returns the i centers and the max distance
def findKCenters(G, i, previousCenters):
    allNodes = set(G)
    if len(previousCenters) == 0: 
        randomCenter = allNodes.pop()
        kCenters = {randomCenter}
        i = i - 1
    else: 
        kCenters = previousCenters
        i = i -len(previousCenters)
    while i != 0: 
        nodeDict ={}
        for node in allNodes:
            minDist = float("inf")
            for center in kCenters:
                minDist = min(minDist, nx.shortest_path_length(G, node,center))
                nodeDict[node] = minDist
        newCenter =  max(nodeDict, key = lambda i:nodeDict[i])
        kCenters.add(newCenter)
        allNodes.remove(newCenter)
        i = i - 1
    finalDict = {}
    for node in allNodes:
        minDist = float("inf")
        for center in kCenters:
            minDist = min(minDist, nx.shortest_path_length(G, node, center))
            finalDict[node] = minDist
    return kCenters, max(finalDict.values())


#for each graph, we calculate the min distance for i centers, if the min distance is equal to 1, we found a dominating set
def dominant(g):
    n = len(g.nodes)
    previousCenters = set()
    for i in range(1, n):
        # print(previousCenters)
        # print(findKCenters(g, i, previousCenters))
        previousCenters, d = findKCenters(g, i, previousCenters)
        if d == 1: 
            return previousCenters



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
