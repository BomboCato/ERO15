#
# cli/drone.py
#

from typing import Annotated
from rich.console import Console

import typer
import drone.analyze


app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Drone related computing.",
)

console = Console()
err_console = Console(stderr=True)


@app.command()
def analyze(
    place: Annotated[
        str, typer.Argument(help="The district/city to analyze.")
    ] = "Montreal",
):
    """
    Launch the drone and analyze the distict/city.
    """
    console.print(f"Analyzing {place}...")

    snow_eul, circuit = drone.analyze.analyze(place)
