import sys, os, time
import networkx as nx
from networkx.utils import arbitrary_element


# Given a graph G and a integer i, we find i centers that minimize the maximum distance of a node to one center
# Returns the i centers and the max distance
def findKCenters(G, k, shortestPaths):
    allNodes = set(G)
    kCenters = set()
    start_with = arbitrary_element(allNodes)
    kCenters.add(start_with)
    nodeDict = {}
    for x in allNodes:
        nodeDict[x] = float("inf")
    k = k - 1
    nodeDict[start_with] = 0
    while k != 0:
        for node in allNodes - kCenters:
            for center in kCenters:
                if nodeDict[node] > shortestPaths[node][center]:
                    nodeDict[node] = shortestPaths[node][center]
        newCenter = max(nodeDict, key=lambda i: nodeDict[i])
        nodeDict[newCenter] = 0
        kCenters.add(newCenter)
        k -= 1
    return kCenters, max(nodeDict.values())


# for each graph, we calculate the min distance for i centers, if the min distance is equal to 1, we found a dominating set
def dominant(g):
    n = len(g.nodes)
    shortestPaths = dict(nx.all_pairs_shortest_path_length(g))
    for i in range(1, n):
        kCenters, d = findKCenters(g, i, shortestPaths)
        if d == 1:
            return kCenters


if __name__ == "__main__":
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
