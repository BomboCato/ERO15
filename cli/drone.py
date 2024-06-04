#
# cli/drone.py
#

from typing import Annotated
from rich.console import Console

import typer
from data.display import route_image
from data.districts import District
from data.route import Route
import drone.analyze
import cli.log as log


app = typer.Typer(
    no_args_is_help=True,
    help="Drone related computing.",
)

console = Console()
err_console = Console(stderr=True)


@app.command()
def analyze(
    district: Annotated[
        str, typer.Argument(help="The district/city to analyze.")
    ] = "Montreal",
):
    """
    Launch the drone and analyze the distict/city.
    """

    log.info(f"CMD: analyze '{district}'")

    snow_eul, circuit = drone.analyze.analyze_snow(district)

    dist = District("snow_eul", snow_eul)
    route = Route(circuit, "snow_eul")

    route_image(dist, route, "red", "save")
