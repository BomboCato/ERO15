#
# lib/display.py
#

from multiprocessing.pool import AsyncResult
from multiprocessing import Pool
from rich.console import Console
from lib.districts import District, load_district
from lib.route import Route
from lib.snow import load_snow, Snow
from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

import osmnx as ox
import lib.log as log
import tempfile
import os
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
import typer

console = Console()


def display_snow(snow: Snow, snow_color: str, road_color: str) -> None:
    """
    Display the @snow from the related district.
    @snow_color and @road_color should be different.
    """

    district, edge_colors = _main_snow(snow, snow_color, road_color)

    ox.plot_graph(district.graph, node_size=1, edge_color=edge_colors)


def save_snow(
    snow: Snow, snow_color: str, road_color: str, filename: str
) -> None:
    """
    Save the @snow from the related district in @filename.
    @snow_color and @road_color should be different.
    """

    district, edge_colors = _main_snow(snow, snow_color, road_color)

    ox.plot_graph(
        district.graph,
        save=True,
        show=False,
        filepath=filename,
        node_size=1,
        edge_color=edge_colors,
    )


def _main_snow(
    snow: Snow, snow_color: str, road_color: str
) -> tuple[District, list[str]]:

    if snow_color == road_color:
        log.warn("snow-color and road-color should be different.")

    district = load_district(snow.related_district)
    snow_tuples = [tup[:3] for tup in snow.data]

    edge_colors = [
        snow_color if (u, v, k) in snow_tuples else road_color
        for u, v, k in district.graph.edges(keys=True)
    ]

    return district, edge_colors


def save_image_district(district: District, filename: str) -> None:
    """
    Save the @district as a png image in @filename
    """
    ox.plot_graph(
        district.graph,
        save=True,
        filepath=filename,
        node_size=1,
        show=False,
    )


def save_image_route(
    district: District, route: Route, route_color: str, filename: str
) -> None:
    """
    Save the @district and the @route on top of it
    as a png image in @filename.
    @route will have @route_color as a color
    @route_color should not be white
    """

    if route_color == "w" or route_color == "white":
        log.warn("Using white as a route color makes the route invisible")

    output_file = filename + ".png"
    edge_colors = [
        (
            route_color
            if (u, v, k) in route.route or (v, u, k) in route.route
            else "w"
        )
        for u, v, k in district.graph.edges(keys=True)
    ]

    ox.plot_graph(
        district.graph,
        save=True,
        filepath=output_file,
        node_size=1,
        show=False,
        edge_color=edge_colors,
    )


def _update_edge_colors(
    edge_colors: list[str],
    u: int,
    v: int,
    k: int,
    edges: list,
    route_color: str,
) -> None:
    try:
        if (u, v, k) in edges:
            edge_colors[edges.index((u, v, k))] = route_color
        elif (v, u, k) in edges:
            edge_colors[edges.index((v, u, k))] = route_color
    except:
        pass


def _route_video_thread(
    graph: nx.MultiGraph,
    route: list,
    route_color: str,
    tmp_dir: str,
    begin: int,
    nb_per_threads: int,
) -> None:
    edges = list(graph.edges(keys=True))

    edge_colors = ["w" for _ in edges]
    for u, v, k in route[:begin]:
        _update_edge_colors(edge_colors, u, v, k, edges, route_color)

    img_nb = begin

    for u, v, k in route[begin : begin + nb_per_threads]:
        _update_edge_colors(edge_colors, u, v, k, edges, route_color)

        ox.plot_graph(
            graph,
            save=True,
            filepath=tmp_dir + "/" + str(img_nb) + ".png",
            node_size=1,
            show=False,
            edge_color=edge_colors,
        )

        plt.close()

        img_nb += 1


def save_video_route(
    district: District,
    route: Route,
    route_color: str,
    filename: str,
    nb_threads: int,
    img_per_second: int,
) -> None:
    """
    Generate a mp4 video from the @route and store it in @filename.mp4
    Each frame will consists of the coloration of a specific edge
    from @route in @district added to the previous colorations.
    Each edge will be visited in the @route.route order.
    """

    matplotlib.use("agg")

    if route_color == "w" or route_color == "white":
        log.warn("Using white as a route color makes the route invisible")

    if len(route.route) < nb_threads:
        log.warn(
            f"Number of threads is higher than the number of edges. Reducing number of threads to {len(route.route)}"
        )
        nb_threads = len(route.route)

    output_file = filename + ".mp4"

    with tempfile.TemporaryDirectory() as tmp_dir:

        results: list[AsyncResult] = []
        tasks: list[TaskID] = []
        beg = 0
        l = len(route.route)
        nb_per_threads = (l // nb_threads) + (l % nb_threads != 0)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
        ) as progress, Pool(nb_threads) as pool:
            for _ in range(nb_threads):
                tasks.append(
                    progress.add_task(
                        f"Generating images {beg}-{beg + nb_per_threads}",
                        total=min(beg + nb_per_threads, len(route.route))
                        - beg,
                    )
                )
                results.append(
                    pool.apply_async(
                        _route_video_thread,
                        (
                            district.graph,
                            route.route,
                            route_color,
                            tmp_dir,
                            beg,
                            nb_per_threads,
                        ),
                    )
                )

                beg += nb_per_threads

            for i in range(nb_threads):
                results[i].get()
                progress.stop_task(tasks[i])

        log.info("Calling ffmpeg on generated images")
        os.system(
            f"ffmpeg -r {img_per_second} -i {tmp_dir}/%01d.png -vcodec mpeg4 -y {output_file}"
        )
