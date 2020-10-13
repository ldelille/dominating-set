# DominatingSet
Approximation Algorithms to find smallest dominating set in a non oriented graph

First Approach is a approximation algorithm. We define sets for the remaining vertices to cover and add one vertices to the current dominating at each step. 

To iterate we choose the next vertice v to add in V-D which maximizes T(v) inter remainingNodes where T(v) contains the neigbors of v.

Second approach uses a K-centers algorithm to find an heuristic. We compute the maximum distance of a node to one of the centers. We start with one center and add centers until this distance is equal to 1(ie we found a dominating set).