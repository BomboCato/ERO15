#
# drone/analyze.py
#

from typing import Tuple
from data.districts import load_district
from drone.snow import gen_random_snow

import networkx as nx
import drone.lib as lib
import cli.log as log


def analyze(dist_name: str) -> Tuple[nx.MultiGraph, list]:
    """
    Analyze a district and return a circuit.
    """

    district = load_district(dist_name)

    snow_dist = gen_random_snow(district)
    snow_dist_un = snow_dist.graph.to_undirected()

    snow_conn = lib.connect(snow_dist_un, "virtual")

    snow_eul = lib.eulerize(snow_conn, "virtual")

    circuit = list(nx.eulerian_circuit(snow_eul))

    return snow_eul, circuit

