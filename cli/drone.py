from typing import Annotated
import typer
from rich.console import Console


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
    snow_method: Annotated[
        str, typer.Argument(help="The snow generation method.")
    ] = "random",
    nb_thread: Annotated[
        int,
        typer.Argument(
            help="Number of threads to use when analyzing the graph."
        ),
    ] = 1,
):
    """
    Launch the drone and analyze the distict/city.
    """
    console.print(f"Snow method: {snow_method}")
    console.print(f"Number of threads: {nb_thread}")
    console.print(f"Analyzing {place}...")
