#
# cli/snowplow.py
#

import typer

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Snowplow related computing.",
)
