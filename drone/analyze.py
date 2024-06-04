#
# drone/analyze.py
#

from typing import Tuple
from data.districts import load_district
from drone.snow import gen_random_snow
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

import networkx as nx
import drone.lib as lib
import cli.log as log


def analyze_snow(dist_name: str) -> Tuple[nx.MultiGraph, list]:
    """
    Analyze a district and return a circuit.
    """

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as progress:
        district = load_district(dist_name)

        log.info("Generating random snow")
        snow_dist = gen_random_snow(district)
        snow_dist_un = snow_dist.graph.to_undirected()

        task_id = progress.add_task(
            description="Connecting graph...", total=None
        )
        snow_conn = lib.connect(snow_dist_un, "virtual")
        progress.remove_task(task_id)
        log.info(
            f"Connect: Added {snow_conn.number_of_edges() - snow_dist_un.number_of_edges()} edge(s)"
        )

        task_id = progress.add_task(
            description="Eulerizing graph...", total=None
        )
        snow_eul = lib.eulerize(snow_conn, "virtual")
        progress.remove_task(task_id)
        log.info(
            f"Eulerize: Added {snow_eul.number_of_edges() - snow_conn.number_of_edges()} edge(s)"
        )

        task_id = progress.add_task(
            description="Getting eulerian circuit...", total=None
        )
        circuit = list(nx.eulerian_circuit(snow_eul))
        progress.remove_task(task_id)

        return snow_eul, circuit
