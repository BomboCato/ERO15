#
# erolib/euler.py
#
# Eulerize a graph

import networkx as nx
import matplotlib.pyplot as plt

def eulerize(graph: nx.Graph, mark) -> nx.Graph:
    """
    Return an Eularian graph by adding edges
    with @mark as an attribute to the @graph
    """

    res_graph = graph.copy()
    odd_vertex = [node for node, degree in graph.degree if degree % 2 != 0]
    comp_odd = nx.complete_graph(odd_vertex)

    for u, v in comp_odd.edges:
        comp_odd[u][v]['weight'] = nx.shortest_path_length(graph, source=u, target=v)

    matching = nx.algorithms.min_weight_matching(comp_odd)

    for u, v in matching:
        res_graph.add_edge(u, v, mark=mark)

    assert nx.is_eulerian(res_graph)

    return res_graph

def diEulerize(graph: nx.DiGraph, mark) -> nx.DiGraph:
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
            for _ in range(out_degrees[node] - in_degrees[node]):
                surplus.append(node)
        elif in_degrees[node] > out_degrees[node]:
            for _ in range(in_degrees[node] - out_degrees[node]):
                deficit.append(node)

    while surplus and deficit:
        u = surplus.pop()
        v = deficit.pop()
        res_graph.add_edge(u, v, mark=mark)

    assert nx.is_semieulerian(res_graph)

    return res_graph
