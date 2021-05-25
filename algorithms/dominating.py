import sys, os, time
import networkx as nx


# find a node to add to the current dominating set. We take c in V-D which maximizes T(v) inter remainingNodes where T(v) contains the neigbors of v.
def findBestNext(g, totalNodes, remainingNodes, currentDominating):
    maxneighborhood = 0
    candidate = None
    for x in totalNodes - currentDominating:
        currentLen = len(set(g[x]).intersection(remainingNodes))
        if currentLen > maxneighborhood:
            candidate = x
            maxneighborhood = currentLen
    return candidate or remainingNodes.pop()


# calculate the dominating set, add the next one until remaingNodes is empty
def dominant(g):
    totalNodes = set(g)
    currentDominating = set()
    remainingNodes = totalNodes
    while remainingNodes:
        v = findBestNext(g, totalNodes, remainingNodes, currentDominating)
        currentDominating.add(v)
        remainingNodes -= set(g[v]) - {v}

    new_graph = nx.Graph()
    for x in currentDominating:
        new_graph.add_node(x)
    return new_graph.nodes


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
