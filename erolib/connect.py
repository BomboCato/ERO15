#
# erolib/connect.py
#
# Transform a graph to a (strongly) connected one

import networkx as nx
import matplotlib.pyplot as plt


def connect(graph: nx.Graph, mark):
    """
    Return a connected graph by adding edges
    with @mark as an attribute (snow is set to 0)
    """

    res_graph = graph.copy()
    comp = list(nx.connected_components(graph))
    comp_graph = nx.Graph()

    for i in range(len(comp)):
        comp_graph.add_node(i)

    l = len(comp)
    for i in range(l):
        for j in range(i + 1, l):
            comp_graph.add_edge(i, j, weight=1)

    mst = nx.minimum_spanning_tree(comp_graph)

    for u, v in mst.edges():
        c_u = next(iter(comp[u]))
        c_v = next(iter(comp[v]))

        res_graph.add_edge(c_u, c_v, mark=mark, snow=0)

    assert nx.is_connected(res_graph)

    return res_graph

def strong_connect(graph: nx.DiGraph, mark):
    """
    Return a strongly connected graph by adding edges
    with @mark as an attribute
    """

    res_graph = graph.copy()
    cond_graph = nx.condensation(graph)

    sinks = [node[0] for node in cond_graph.out_degree if node[1] == 0]
    sources = [node[0] for node in cond_graph.in_degree if node[1] == 0]

    for source in sources:
        for sink in sinks:
            if sink != source:
                src = next(iter(cond_graph.nodes[source]["members"]))
                sik = next(iter(cond_graph.nodes[sink]["members"]))

                res_graph.add_edge(sik, src, mark=mark)

    assert nx.is_strongly_connected(res_graph)

    nx.draw_networkx(res_graph, with_labels=True)
    plt.show()

    return res_graph
