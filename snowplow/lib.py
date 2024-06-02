#
# snowplow/lib.py
#

import networkx as nx


def strong_connect(graph: nx.MultiDiGraph, mark) -> nx.MultiDiGraph:
    """
    Return a strongly connected graph by adding arcs
    with @mark as an attribute
    """

    res_graph = graph.copy()
    cond_graph = nx.condensation(graph)

    sinks = [node for node, degree in cond_graph.out_degree if degree == 0]
    sources = [
        node for node, degree in cond_graph.in_degree if degree == 0
    ]

    for source in sources:
        for sink in sinks:
            if sink != source:
                src = next(iter(cond_graph.nodes[source]["members"]))
                sik = next(iter(cond_graph.nodes[sink]["members"]))

                res_graph.add_edge(sik, src, mark=mark)

    assert nx.is_strongly_connected(res_graph)

    return res_graph


def diEulerize(graph: nx.MultiDiGraph, mark) -> nx.MultiDiGraph:
    """
    Return an Eularian digraph by adding arcs
    with @mark as an attribute to the @graph
    """

    res_graph = graph.copy()
    in_degrees = dict(graph.in_degree())
    out_degrees = dict(graph.out_degree())

    deficit = []
    surplus = []

    for node in graph.nodes():
        if in_degrees[node] < out_degrees[node]:
            surplus.extend([node for _ in range(round(out_degrees[node] - in_degrees[node]))])
        elif in_degrees[node] > out_degrees[node]:
            deficit.extend([node for _ in range(round(in_degrees[node] - out_degrees[node]))])

    while surplus and deficit:
        u = surplus.pop()
        v = deficit.pop()
        res_graph.add_edge(u, v, mark=mark)

    assert nx.is_semieulerian(res_graph)

    return res_graph
