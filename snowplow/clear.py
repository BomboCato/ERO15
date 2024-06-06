#
# snowplow/snowplow.py
#

from threading import Thread
from typing import Tuple
from data.districts import District, load_district
from data.route import Route
from data.snow import Snow, load_snow
from data.display import route_video, route_image
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.console import Console
from geopy.distance import geodesic

import osmnx as ox
import networkx as nx
import snowplow.lib as lib
import cli.log as log
import math
import drone.analyze as analyze

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


def clear(id):
    """ """
    snow = load_snow(id)
    if snow == None:
        return

    dist_all = load_district("Montreal")
    G_all = dist_all.graph
    G_di = load_district(snow.related_district).graph

    console.print(snow.data)
    list_snow = [
        (u, v, k)
        for u, v, k, data in snow.data
        if data >= 2.5 and data <= 15
    ]
    snow_graph = nx.edge_subgraph(G_di, list_snow)

    ox.plot_graph(snow_graph)
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

    route = Route(real_circuit, snow.related_district)
    route_video(
        District("Verdun, Montreal", G_di), route, "red", "test", 16, 64
    )
    route_image(District("Verdun, Montreal", G_di), route, "red", "test")
