#
# drone/analyze.py
#

import math
from multiprocessing.pool import AsyncResult, Pool
from typing import Tuple

import networkx as nx
from geopy.distance import geodesic
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

import drone.lib as lib
import lib.log as log
from drone.snow import gen_random_snow
from lib.districts import District, load_district
from lib.route import Route, RouteType
from lib.snow import Snow

console = Console()


def eucl_dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def getDistrictGraphSnow(
    i, G_all: nx.MultiGraph, l: list[nx.MultiGraph]
) -> nx.MultiGraph:
    """
    Allows retrieval of each district's graph while keeping the attribute 'snow' generated in the graph of the entire city
    """
    R = G_all.copy()
    R.remove_nodes_from(n for n in G_all if n not in l[i])
    R.remove_edges_from(e for e in G_all.edges if e not in l[i].edges)
    return R


def alldistrictsSnow(
    G_all: nx.MultiGraph, l: list[nx.MultiGraph]
) -> list[nx.MultiGraph]:
    res = []
    for i in range(19):
        res.append(getDistrictGraphSnow(i, G_all, l))
    return res


def retrieveDistrictsGraph() -> list[District]:
    districts = [
        "Ahuntsic-Cartierville, Montreal",
        "Anjou, Montreal",
        "Côte-des-Neiges–Notre-Dame-de-Grâce, Montreal",
        "Lachine, Montreal",
        "LaSalle, Montreal",
        "Plateau Mont-Royal, Montreal",
        "Le Sud-Ouest, Montreal",
        "Île-Bizard–Sainte-Geneviève, Montreal",
        "Mercier–Hochelaga-Maisonneuve, Montreal",
        "Montréal-Nord, Montreal",
        "Outremont, Montreal",
        "Pierrefonds-Roxboro, Montreal",
        "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal",
        "Rosemont–La Petite-Patrie, Montreal",
        "Saint-Laurent, Montreal",
        "Saint-Léonard, Montreal",
        "Verdun, Montreal",
        "Ville-Marie, Montreal",
        "Villeray–Saint-Michel–Parc-Extension, Montreal",
    ]

    res: list[District] = []

    for district in districts:
        d = load_district(district)
        d.graph = d.graph.to_undirected()
        res.append(d)

    return res


# PARCOURS DRONE SUR G (AJOUTER UN ATTRIBUT POUR DIRE SI IL FAUT DENEIGER)
def drone(
    G,
    src=None,
) -> tuple:
    """
    Returns a tuple (G, circuit) where G is the graph with attribute 'need_clear' added and circuit is path taken by the drone
    """

    G_conn = lib.connect(G, False)

    G_eul = lib.eulerize(G_conn, False)

    for u, v, k, data in G_eul.edges(keys=True, data=True):
        snow = data.get(
            "snow", 0
        )  # tries to get value of attribute 'snow', if not found returns 0
        if snow >= 2.5 and snow <= 15:
            G_eul[u][v][k]["need_clear"] = True
        else:
            G_eul[u][v][k]["need_clear"] = False
    circuit = nx.eulerian_circuit(G_eul, source=src, keys=True)

    return list(circuit), G_eul


def analyze_snow_montreal(
    progress: Progress, min_snow: float, max_snow: float
) -> Tuple[District, Route, Snow, float]:
    l = retrieveDistrictsGraph()
    G_all = nx.compose_all([d.graph for d in l])
    G_all = gen_random_snow(District("G_all", G_all), min_snow, max_snow)

    l = alldistrictsSnow(G_all.graph, [d.graph for d in l])

    total_distance = 0
    list_of_nodes = []
    list_circuit: list[tuple] = []
    list_eul: list[nx.MultiGraph] = []
    res_circuit = []

    results: list[AsyncResult] = []
    tasks: list[TaskID] = []

    with Pool(19) as pool:
        for i in range(19):
            tasks.append(
                progress.add_task(
                    f"Eulerize and Connect graph {i}...", total=None
                )
            )
            results.append(
                pool.apply_async(
                    drone,
                    (l[i],),
                )
            )

        for i in range(len(results)):
            circuit, g_eul = results[i].get()
            list_circuit.append(circuit)
            list_eul.append(g_eul)
            progress.stop_task(tasks[i])

    for i in range(19):
        log.info(
            f"Eulerize and Connect: Added {list_eul[i].number_of_edges() - l[i].number_of_edges()} edge(s)"
        )

    for i in range(19):
        # if i in [1, 5, 10, 12, 16]:
        G_eul = list_eul[i]
        for u, v, k in list_circuit[i]:
            if (u, v, k) in G_eul.edges(keys=True):
                if "length" in G_eul[u][v][k]:
                    total_distance += G_eul[u][v][k]["length"]
                elif "mark" in G_eul[u][v][k]:
                    lat1, lon1 = G_eul.nodes[u]["y"], G_eul.nodes[u]["x"]
                    lat2, lon2 = G_eul.nodes[v]["y"], G_eul.nodes[v]["x"]
                    length = geodesic((lat1, lon1), (lat2, lon2)).meters
                    total_distance += length
            elif (v, u, k) in G_eul.edges(keys=True):
                if "length" in G_eul[v][u][k]:
                    total_distance += G_eul[v][u][k]["length"]
                elif "mark" in G_eul[v][u][k]:
                    lat1, lon1 = G_eul.nodes[u]["y"], G_eul.nodes[u]["x"]
                    lat2, lon2 = G_eul.nodes[v]["y"], G_eul.nodes[v]["x"]
                    length = geodesic((lat1, lon1), (lat2, lon2)).meters
                    total_distance += length
        node, _, k = list_circuit[i][0]
        list_of_nodes.append(node)

    # TODO: Hardcoder les quartiers ou remplacer nx.shortest path par une fonction qui calcule la distance en fonction de weight et pas en fonction du NB de noeuds
    while len(list_of_nodes) > 1:
        min_distance = float("inf")
        current_node = list_of_nodes[0]
        closest_node = None
        min_length = 0

        for node in list_of_nodes:
            if node == current_node:
                continue
            lat1, lon1 = (
                G_all.graph.nodes[node]["y"],
                G_all.graph.nodes[node]["x"],
            )
            lat2, lon2 = (
                G_all.graph.nodes[current_node]["y"],
                G_all.graph.nodes[current_node]["x"],
            )
            length = geodesic((lat1, lon1), (lat2, lon2)).meters
            G_all.graph.add_edge(current_node, node, length=length)
            distance = nx.shortest_path_length(
                G_all.graph, current_node, node, weight="length"
            )
            G_all.graph.remove_edge(current_node, node)
            if distance < min_distance:
                min_distance = distance
                closest_node = node
                min_length = length

        total_distance += min_length
        c1 = [
            c
            for c in list_circuit
            if c != None and c[0][0] == current_node
        ][0]
        c2 = [
            c
            for c in list_circuit
            if c != None and c[0][0] == closest_node
        ][0]
        res_circuit.extend(c1)
        res_circuit.append((current_node, closest_node))
        res_circuit.extend(c2)
        G_all.graph.add_edge(current_node, closest_node)
        list_of_nodes.remove(current_node)
        current_node = closest_node
    snow_list = [
        (u, v, k, data["snow"])
        for u, v, k, data in G_all.graph.edges(data=True, keys=True)
        if "snow" in data
    ]
    return (
        District("Montreal", G_all.graph),
        Route(res_circuit, "Montreal", RouteType.DRONE),
        Snow(snow_list, "Montreal"),
        total_distance,
    )


def analyze_snow(
    dist_name: str, min_snow: float, max_snow: float
) -> Tuple[District, Route, Snow, float]:
    """
    Analyze a district and return a circuit.
    """

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as progress:
        if dist_name == "Montreal":
            return analyze_snow_montreal(progress, min_snow, max_snow)

        district = load_district(dist_name)

        log.info("Generating random snow")
        snow_dist = gen_random_snow(district, min_snow, max_snow)
        snow_dist_un = snow_dist.graph.to_undirected()

        task_id = progress.add_task(
            description="Connecting graph...", total=None
        )
        snow_conn = lib.connect(snow_dist_un, "virtual")
        progress.remove_task(task_id)
        log.info(
            f"Connect: Added {snow_conn.number_of_edges() - snow_dist_un.number_of_edges()} edge(s)"
        )

        task_id = progress.add_task(
            description="Eulerizing graph...", total=None
        )
        snow_eul = lib.eulerize(snow_conn, "virtual")
        progress.remove_task(task_id)
        log.info(
            f"Eulerize: Added {snow_eul.number_of_edges() - snow_conn.number_of_edges()} edge(s)"
        )

        task_id = progress.add_task(
            description="Getting eulerian circuit...", total=None
        )
        circuit = list(nx.eulerian_circuit(snow_eul, keys=True))
        progress.remove_task(task_id)

        distance = 0
        for u, v, length in snow_eul.edges.data("length", -1):
            if length == -1:
                x1 = snow_eul.nodes[u]["x"]
                y1 = snow_eul.nodes[u]["y"]
                x2 = snow_eul.nodes[v]["x"]
                y2 = snow_eul.nodes[v]["y"]
                distance += geodesic((x1, y1), (x2, y2)).meters
            else:
                distance += length

        snow_list = [
            (u, v, k, data["snow"])
            for u, v, k, data in snow_dist_un.edges(data=True, keys=True)
            if "snow" in data and 2.5 <= data["snow"] <= 15
        ]

        return (
            District(f"{dist_name}_snow", snow_eul),
            Route(circuit, f"{dist_name}", RouteType.DRONE),
            Snow(snow_list, f"{dist_name}"),
            distance,
        )
