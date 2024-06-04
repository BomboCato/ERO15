#
# cli/drone.py
#

from typing import Annotated, Optional
from rich.console import Console
from data.display import route_video
from data.districts import District
from data.route import Route

import typer
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
    video: Annotated[
        Optional[str],
        typer.Option(
            help="Generate a video that represents the drone route. Save it to [VIDEO].mp4"
        ),
    ] = None,
    nb_threads: Annotated[
        int,
        typer.Option(
            help="Number of threads to use when eulerizing or video generation"
        ),
    ] = 1,
) -> None:
    """
    Launch the drone and analyze the distict/city.
    """

    log.info(f"CMD: drone analyze '{district}' threads: '{nb_threads}'")

    snow_eul, circuit = drone.analyze.analyze_snow(district)

    dist = District("snow_eul", snow_eul)
    route = Route(circuit, "snow_eul")

    if video:
        log.info("Generating video")
        route_video(dist, route, "red", video, nb_threads)
