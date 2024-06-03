#
# data/districts.py
#

import networkx as nx
import osmnx as ox
import data.lib as lib


class District:
    def __init__(self, name: str, graph: nx.MultiDiGraph) -> None:
        self.name = name
        self.graph = graph

    def __str__(self) -> str:
        return f"District {self.name}"

    def __repr__(self) -> str:
        return self.__str__()


def create_district(name: str, graph: nx.MultiDiGraph) -> District:
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
        print("District already downloaded")
        return districts[name]

    print("Downloading district...")
    graph = ox.graph_from_place(name, network_type="drive")

    dist = create_district(name, graph)

    return dist
