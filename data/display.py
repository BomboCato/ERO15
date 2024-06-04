#
# data/display.py
#

from data.districts import District

import osmnx as ox
import cli.log as log
from data.route import Route


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
