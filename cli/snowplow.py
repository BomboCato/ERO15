#
# cli/snowplow.py
#

from typing import Annotated
from rich.console import Console

import typer
import snowplow.clear


app = typer.Typer(
    no_args_is_help=True,
    help="Snowplow related computing.",
)

console = Console()
err_console = Console(stderr=True)


@app.command()
def clear(
    id: Annotated[
        int,
        typer.Argument(
            help="The id of the snow data generated by the drone."
        ),
    ] = 0
) -> None:
    """
    Start the snowplows.
    """
    snowplow.clear.clear(id)
