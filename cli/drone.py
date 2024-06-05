#
# cli/drone.py
#

from typing import Annotated, Optional
from rich.console import Console
from rich.table import Table
from data.display import route_video

import typer
from data.snow import create_snow
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

    dist_snow, route, snow, distance = drone.analyze.analyze_snow(district)
    table = Table(title="Results")

    table.add_column("District")
    table.add_column("Distance")
    table.add_column("Speed")
    table.add_column("Time")
    table.add_column("Cost")

    table.add_row(
        district,
        f"{round(distance, 2)}m",
        "60km/h",
        f"{round(distance / 1000 / 60, 2)}h",
        f"{100 + round(0.01 * (distance / 1000), 2)}€",
    )

    if video:
        log.info("Generating video")
        route_video(dist_snow, route, "red", video, nb_threads)

    console.print(table)

    snow = create_snow(snow.data, snow.related_district)

    log.info(f"Generated snow data for {district} with id {snow.id}")

