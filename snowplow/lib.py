#
# snowplow/lib.py
#

import networkx as nx
import cli.log as log

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

    for i in range(len(sources) - 1):
        src1 = next(iter(cond_graph.nodes[sources[i]]["members"]))
        src2 = next(iter(cond_graph.nodes[sources[i + 1]]["members"]))

        res_graph.add_edge(src1, src2, mark=mark)

    for i in range(len(sinks) - 1):
        sink1 = next(iter(cond_graph.nodes[sinks[i]]["members"]))
        sink2 = next(iter(cond_graph.nodes[sinks[i + 1]]["members"]))

        res_graph.add_edge(sink1, sink2, mark=mark)

    if len(sources) != 0 and len(sinks) != 0:
        src = next(iter(cond_graph.nodes[sources[0]]["members"]))
        sink = next(iter(cond_graph.nodes[sinks[0]]["members"]))

        res_graph.add_edge(src, sink, mark=mark)

    if not nx.is_strongly_connected(res_graph):
        log.warn("Could not return connected graph")

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
            surplus.extend(
                [
                    node
                    for _ in range(
                        round(out_degrees[node] - in_degrees[node])
                    )
                ]
            )
        elif in_degrees[node] > out_degrees[node]:
            deficit.extend(
                [
                    node
                    for _ in range(
                        round(in_degrees[node] - out_degrees[node])
                    )
                ]
            )

    while surplus and deficit:
        u = surplus.pop()
        v = deficit.pop()
        res_graph.add_edge(u, v, mark=mark)

    if not nx.is_eulerian(res_graph):
        log.warn("Could not return eulerian graph")

    return res_graph
