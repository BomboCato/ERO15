#
# drone/analyze.py
#

from data.districts import load_district
from drone.snow import gen_random_snow

import osmnx as ox


def analyze(dist_name: str) -> None:
    """
    Analyze a district and return a circuit.
    """

    district = load_district(dist_name)

    snow_dist = gen_random_snow(district)

    edge_colors = [
        "r" if (snow_dist.graph[u][v][k]["snow"] >= 2.5 and snow_dist.graph[u][v][k]["snow"] <= 15)
        else "b" for u, v, k in snow_dist.graph.edges(keys=True)
    ]

    ox.plot_graph(snow_dist.graph, edge_color=edge_colors)
