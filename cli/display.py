#
# cli/display.py
#

from typing_extensions import Annotated
from data.districts import load_district

import typer
import osmnx as ox


app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Display graphs, routes and data.",
)


@app.command()
def district(
    name: Annotated[
        str, typer.Argument(help="The district name to display.")
    ],
    output_file: Annotated[
        str, typer.Option(help="File name to save the graph image.")
    ] = "",
) -> None:
    """
    Display a specific district.
    If --output-file [FILEPATH] is provided, store the graph in FILEPATH.
    """
    dist = load_district(name)

    if output_file != "":
        ox.plot_graph(dist.graph, save=True, filepath=output_file, node_size=1)
    else:
        ox.plot_graph(dist.graph)
