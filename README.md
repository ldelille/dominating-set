# DominatingSet

This repo use [networkx](https://github.com/networkx/networkx) which is a great tool for graph representation that I use and contribute to.


Approximation Algorithms to find the **smallest dominating set in a non-oriented graph**

First Approach is an approximation algorithm. We define sets for the remaining vertices to cover and add one vertex to the current dominating at each step. 

To iterate we choose the next vertices v to add in V-D which maximizes T(v) inter remainingNodes where T(v) contains the neigbors of v.

Second approach uses a **K-centers algorithm to find a heuristic**. We compute the maximum distance of a node to one of the centers.
We start with one center and add centers until this distance is equal to 1 (ie we found a dominating set).


To launch on test dataset provided. 

```bash
python dominating.py ../test_dataset ../output_dir
```

