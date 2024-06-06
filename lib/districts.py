#
# lib/districts.py
#

import networkx as nx
import osmnx as ox
import lib.lib as lib
import lib.log as log


class District:
    def __init__(
        self, name: str, graph: nx.MultiDiGraph | nx.MultiGraph
    ) -> None:
        self.name = name
        self.graph = graph

    def copy(self):
        return District(self.name, self.graph.copy())

    def __str__(self) -> str:
        return f"District {self.name}"

    def __repr__(self) -> str:
        return self.__str__()


def save_district(
    name: str, graph: nx.MultiDiGraph | nx.MultiGraph
) -> District:
    """
    Create a new district object and save it to local storage.
    Does not check if district already exist !
    """
    districts: dict[str, District] = lib.get_data("districts.pkl")

    dist = District(name, graph)

    districts[name] = dist

    lib.save_data("districts.pkl", districts)

    return dist


def load_district(name: str) -> District:
    """
    Load a district from local storage. If district does not exist, download it and save it to local storage.
    """

    districts: dict[str, District] = lib.get_data("districts.pkl")

    if name in districts:
        log.info(f"District {name} already downloaded")
        return districts[name]

    log.info(f"Downloading district '{name}'")
    graph = ox.graph_from_place(name, network_type="drive")

    dist = save_district(name, graph)

    return dist
