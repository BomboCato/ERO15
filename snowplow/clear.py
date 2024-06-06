#
# snowplow/clear.py
#

from lib.districts import load_district
from lib.route import Route, RouteType
from lib.snow import load_snow
from rich.console import Console

import osmnx as ox
import networkx as nx
import snowplow.lib as lib

console = Console()


def transferAttributes(G, G2):
    """
    It transfers the attributes of the edges in G2 to G.
    """
    for u, v, k, data in G2.edges(keys=True, data=True):
        if G.has_edge(u, v, k):
            G[u][v][k].update(data)
        if G.has_edge(v, u, k):
            G[v][u][k].update(data)


def clear_path(id: int) -> Route | None:
    """
    Return the route that a snowplow should take to
    remove the snow with id @id.
    Does not eulerize the graph but use shortest_path
    to build the circuit.
    """

    snow = load_snow(id)
    if not snow:
        return None

    dist_snow = load_district(snow.related_district)

    ox.plot_graph(dist_snow.graph)


def clear_eul(id: int) -> list[Route] | None:
    """ """
    snow = load_snow(id)
    if not snow:
        return None

    dist_all = load_district("Montreal")
    G_all = dist_all.graph
    G_di = load_district(snow.related_district).graph

    list_snow = [
        (u, v, k)
        for u, v, k, data in snow.data
        if 2.5 <= data <= 15
    ]
    snow_graph = nx.edge_subgraph(G_di, list_snow)

    G_conn = lib.strong_connect(snow_graph, "virtual")
    G_eul = lib.diEulerize(G_conn, "virtual")

    circuit = list(nx.eulerian_circuit(G_eul, keys=True))
    real_circuit = []

    for u, v, k in circuit:
        if "mark" in G_eul[u][v][k]:
            path = nx.shortest_path(G_all, u, v, weight="length")
            edge_path = []
            for i in range(len(path) - 1):
                min_len = float("inf")
                k = float("inf")
                edges = G_all[path[i]][path[i + 1]]
                for value, edge in edges.items():
                    if edge["length"] < min_len:
                        min_len = edge["length"]
                        k = value
                edge_path.append((path[i], path[i + 1], k))
            real_circuit.extend(edge_path)
        else:
            real_circuit.append((u, v, k))

    route = Route(real_circuit, snow.related_district, RouteType.SNOWPLOW)

    return [route]
