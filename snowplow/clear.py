#
# snowplow/clear.py
#
from networkx import NetworkXNoPath

from lib.districts import load_district, District
from lib.route import Route, RouteType
from lib.snow import load_snow, Snow
from rich.console import Console
from rich.progress import Progress, BarColumn, TaskID, TextColumn, TimeElapsedColumn

import typer
import networkx as nx
import snowplow.lib as lib
import lib.log as log

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


def clear_path(id: int) -> list[Route] | None:
    """
    Return the route that a snowplow should take to
    remove the snow with id @id.
    Does not eulerize the graph but use shortest_path
    to build the circuit.
    @param id: the id of the snow to clear
    @return: the route that a snowplow should take to remove the snow with id @id
    """

    snow = load_snow(id)
    if not snow:
        return None

    remain_edges = [(u, v, k) for u, v, k, _ in snow.data]

    if not remain_edges:
        return []

    district = load_district(snow.related_district)
    montreal = load_district("Montreal")
    montreal.graph = montreal.graph.to_undirected()
    current_edge = remain_edges[0]
    res_path = []

    try:

        with Progress() as progress:
            task = progress.add_task("Building snowplow route", total=len(remain_edges))

            while len(remain_edges) > 1:
                min_length = float("inf")
                closest_edge = None
                min_path = []
                for edge in remain_edges:
                    if edge == current_edge:
                        continue
                    path = nx.shortest_path(
                        montreal.graph, current_edge[1], edge[0], weight="length"
                    )
                    length = sum(
                        montreal.graph[path[i]][path[i + 1]][0]["length"]
                        for i in range(len(path) - 1)
                    )
                    if length < min_length:
                        min_length = length
                        closest_edge = edge
                        min_path = path

                min_path = [
                    (min_path[i], min_path[i + 1], 0)
                    for i in range(len(min_path) - 1)
                ]
                remain_edges.remove(current_edge)
                res_path.append(current_edge)
                res_path.extend(min_path)
                current_edge = closest_edge

                progress.update(task, advance=1)


        if current_edge:
            res_path.append(current_edge)

        route = Route(res_path, snow.related_district, RouteType.SNOWPLOW)

        previous = None
        for u, v, k in route.route:
            if not district.graph.has_edge(
                u, v, key=k
            ) and not district.graph.has_edge(v, u, key=k):
                log.warn(
                    f"Edge {u} -> {v} with key {k} not in district graph."
                )
            elif previous and previous[1] != u:
                log.warn(f"Previous edge {previous} does not connect to {u}.")

            previous = (u, v, k)

        return [route]

    except NetworkXNoPath:
        log.error("No path found between two nodes. You should use --method eul.")
        raise typer.Exit(code=1)


def clear_eul(id: int) -> list[Route] | None:
    """ """
    snow = load_snow(id)
    if not snow:
        return None

    dist_all = load_district("Montreal")
    G_all = dist_all.graph.to_undirected()
    G_di = load_district(snow.related_district).graph

    list_snow = [
        (u, v, k) for u, v, k, data in snow.data if 2.5 <= data <= 15
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
                    if "length" in edge and edge["length"] < min_len:
                        min_len = edge["length"]
                        k = value
                edge_path.append((path[i], path[i + 1], k))
            real_circuit.extend(edge_path)
        else:
            real_circuit.append((u, v, k))

    route = Route(real_circuit, snow.related_district, RouteType.SNOWPLOW)

    return [route]
