#
# data/display.py
#

from data.districts import District
from data.route import Route
from rich.progress import Progress

import osmnx as ox
import cli.log as log
import tempfile
import os
import matplotlib.pyplot as plt
import matplotlib
import threading


def district_image(district: District, filename: str) -> None:
    """
    Save the @district as a png image in @filename
    """
    output_file = filename + ".png"

    log.info(f"Saving district '{district.name}' in file '{output_file}'")

    ox.plot_graph(
        district.graph,
        save=True,
        filepath=output_file,
        node_size=1,
        show=False,
    )


def route_image(
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
            if (u, v) in route.route or (v, u) in route.route
            else "w"
        )
        for u, v in district.graph.edges()
    ]

    log.info(
        f"Saving district '{district.name}' with route in file '{output_file}'"
    )

    ox.plot_graph(
        district.graph,
        save=True,
        filepath=output_file,
        node_size=1,
        show=False,
        edge_color=edge_colors,
    )


def _update_edge_colors(
    edge_colors: list[str], u: int, v: int, edges: list, route_color: str
) -> None:
    if (u, v) in edges:
        ind = edges.index((u, v))
        while edge_colors[ind] == route_color:
            ind = edges.index((u, v), ind + 1)
        edge_colors[ind] = route_color
    else:
        ind = edges.index((v, u))
        while edge_colors[ind] == route_color:
            ind = edges.index((v, u), ind + 1)
        edge_colors[ind] = route_color


def _route_video_thread(
    district: District,
    route: Route,
    route_color: str,
    tmp_dir: str,
    begin: int,
    nb_per_threads: int,
    progress: Progress,
) -> None:

    edges = list(district.graph.edges())

    edge_colors = ["w" for _ in route.route]
    for u, v in route.route[:begin]:
        _update_edge_colors(edge_colors, u, v, edges, route_color)

    img_nb = begin

    task = progress.add_task(
        f"Generating images {begin}-{begin + nb_per_threads - 1}",
        total=min(begin + nb_per_threads, len(route.route)) - begin,
    )

    for u, v in route.route[begin : begin + nb_per_threads]:
        _update_edge_colors(edge_colors, u, v, edges, route_color)

        ox.plot_graph(
            district.graph,
            save=True,
            filepath=tmp_dir + "/" + str(img_nb) + ".png",
            node_size=1,
            show=False,
            edge_color=edge_colors,
        )

        plt.close()

        img_nb += 1

        progress.update(task, advance=1)


def route_video(
    district: District,
    route: Route,
    route_color: str,
    filename: str,
    nb_threads: int,
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

        threads: list[threading.Thread] = []
        beg = 0
        l = len(route.route)
        nb_per_threads = (l // nb_threads) + (l % nb_threads != 0)

        with Progress() as progress:
            for _ in range(nb_threads):
                threads.append(
                    threading.Thread(
                        target=_route_video_thread,
                        args=(
                            district,
                            route,
                            route_color,
                            tmp_dir,
                            beg,
                            nb_per_threads,
                            progress,
                        ),
                    )
                )

                beg += nb_per_threads

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        log.info("Calling ffmpeg on generated images")
        os.system(
            f"ffmpeg -r 16 -i {tmp_dir}/%01d.png -vcodec mpeg4 -y {output_file}"
        )
