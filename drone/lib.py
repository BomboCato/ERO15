#
# drone/lib.py
#


import networkx as nx


def connect(graph: nx.MultiGraph, mark) -> nx.MultiGraph:
    """
    Return a connected graph by adding edges
    with @mark as an attribute (snow is set to 0)
    """

    res_graph = graph.copy()
    comp = list(nx.connected_components(graph))
    comp_graph = nx.Graph()

    l = len(comp)
    for i in range(l):
        for j in range(i + 1, l):
            comp_graph.add_edge(i, j, weight=1)

    mst = nx.minimum_spanning_tree(comp_graph)

    for u, v in mst.edges():
        # next(iter(set())) takes the first element of the set
        c_u = next(iter(comp[u]))
        c_v = next(iter(comp[v]))

        res_graph.add_edge(c_u, c_v, mark=mark, snow=0)

    assert nx.is_connected(res_graph)

    return res_graph


def eulerize(graph: nx.MultiGraph, mark) -> nx.MultiGraph:
    """
    Return an semieularian graph by adding edges
    with @mark as an attribute to the @graph
    """

    res_graph = graph.copy()
    odd_vertex = [node for node, degree in graph.degree if degree % 2 != 0]
    comp_odd = nx.complete_graph(odd_vertex)

    for u, v in comp_odd.edges:
        comp_odd[u][v]["weight"] = nx.shortest_path_length(
            graph, source=u, target=v
        )

    matching = nx.algorithms.min_weight_matching(comp_odd)

    for u, v in matching:
        res_graph.add_edge(u, v, mark=mark)

    assert nx.is_semieulerian(res_graph)

    return res_graph
