#
# data/display.py
#

from data.districts import District
from data.route import Route
from rich.progress import track
from rich.console import Console

import osmnx as ox
import cli.log as log
import tempfile
import os
import matplotlib.pyplot as plt
import threading

console = Console()


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


def _route_video_thread(
    district: District,
    route: list,
    route_color: str,
    tmp_dir: str,
    img_nb: int,
    edge_colors: list[str],
) -> None:
    edges = list(district.graph.edges())

    for u, v in track(
        route, description=f"Generating images {img_nb}-{len(route)}"
    ):
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


def route_video(
    district: District, route: Route, route_color: str, filename: str
) -> None:
    """
    Generate a mp4 video from the @route and store it in @filename.mp4
    Each frame will consists of the coloration of a specific edge
    from @route in @district added to the previous colorations.
    Each edge will be visited in the @route.route order.
    """

    if route_color == "w" or route_color == "white":
        log.warn("Using white as a route color makes the route invisible")

    output_file = filename + ".mp4"
    img_nb = 0
    edges = list(district.graph.edges())
    edge_colors = ["w" for _ in edges]

    with tempfile.TemporaryDirectory() as tmp_dir:

        threads = []

        for i in range(5):
            threads.append(threading.Thread(target=_route_video_thread, args=(district, route)))

        log.info("Calling ffmpeg on generated images")
        os.system(
            f"ffmpeg -r 16 -i {tmp_dir}/%01d.png -vcodec mpeg4 -y {output_file}"
        )
