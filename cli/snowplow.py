#
# cli/snowplow.py
#

import typer

app = typer.Typer(
    no_args_is_help=True,
    help="Snowplow related computing.",
)

from typing import Annotated, Optional
from rich.console import Console
from rich.table import Table

import snowplow.clear
import cli.log as log

console = Console()
err_console = Console(stderr=True)

@app.command()
def clear(
    district: Annotated[
        str, typer.Argument(help="The district/city to analyze.")
    ] = "Montreal"
) -> None:
    """
    Start the snowplows in the distict/city.
    """
    dist_snow, route, snow, distance = snowplow.clear.clear(district)
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

    console.print(table)
