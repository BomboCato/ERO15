#
# erolib/connect.py
#
# Transform a graph to a (strongly) connected one

import networkx as nx


def connect(graph: nx.Graph, mark):
    """
    Return a connected graph by adding edges
    with @mark as an attribute
    """

    res_graph = graph.copy()
    components = list(nx.connected_components(graph))
    components_graph = nx.Graph()

    for i, _ in enumerate(components):
        components_graph.add_node(i)

    l = len(components)
    for i in range(l):
        for j in range(i + 1, l):
            components_graph.add_edge(i, j, weight=1)

    mst = nx.minimum_spanning_tree(components_graph)

    for u, v in mst.edges():
        c_u = next(iter(components[u]))
        c_v = next(iter(components[v]))

        res_graph.add_edge(c_u, c_v, mark=mark)

    return res_graph
