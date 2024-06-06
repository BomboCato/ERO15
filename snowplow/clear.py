#
# snowplow/snowplow.py
#

from threading import Thread
from typing import Tuple
from data.districts import District, load_district
from data.route import Route
from data.snow import Snow
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

def transferAttributes(G, G2):
    """
    It transfers the attributes of the edges in G2 to G.
    """
    for u, v, k, data in G2.edges(keys=True, data=True):
        if G.has_edge(u, v, k):
            G[u][v][k].update(data)
        if G.has_edge(v, u, k):
            G[v][u][k].update(data)

def clear(dist_name):
    """
    """
    DiG = load_district(dist_name).graph
    (dist, _, snow, _) = analyze.analyze_snow(dist_name)
    transferAttributes(DiG, dist.graph)

    snow_graph = DiG.copy()
    for u, v, k, data in DiG.edges(keys=True, data=True):
        snow = DiG[u][v][k]["snow"]
        if snow < 2.5 or snow > 15:
            snow_graph.remove_edge(u, v)

    ox.plot_graph(DiG)
    ox.plot_graph(snow_graph)
    G_conn = lib.strong_connect(snow_graph, "virtual")
    ox.plot_graph(G_conn)
    G_eul = lib.diEulerize(G_conn, "virtual")
    ox.plot_graph(G_eul)
    circuit = list(nx.eulerian_circuit(G_eul, source=G_eul.edges[0, 0, 0], keys=True))
    print(circuit)
    # for u, v, k in circuit:
    #     if "virtual" in :
    #         path = nx.shortest_path(G_eul, circuit[u][v])