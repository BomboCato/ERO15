#
# data/data.py
#
# Optimizing loading times

from pathlib import Path

import networkx as nx
import pickle

data_path = Path(__file__).parent


class District:
    def __init__(self, name: str, graph: nx.MultiDiGraph) -> None:
        self.name = name
        self.graph = graph

    def __str__(self) -> str:
        return f"District {self.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Snow:
    def __init__(self, snow_data: list, related_district: str) -> None:
        self.data = snow_data
        self.related_district = related_district

    def __str__(self) -> str:
        return f"Snow for '{self.related_district}'"

    def __repr__(self) -> str:
        return self.__str__()


class Route:
    def __init__(self, route: list) -> None:
        self.id = id
        self.route = route

    def __str__(self) -> str:
        return "Route"

    def __repr__(self) -> str:
        return self.__str__()


def get_data(file_path: Path) -> dict:
    """
    Return the object contained in the @file_path file.
    Create the file if it does not exist.
    """
    pick = {}

    try:
        with open(file_path, "rb") as data:
            pick = pickle.load(data)
    except FileNotFoundError:
        Path(file_path).touch()

    return pick


def save_data(file_path: Path, data: dict) -> None:
    """
    Save @data in @file_path file.
    """
    with open(file_path, "wb") as data_file:
        pickle.dump(data, data_file, pickle.HIGHEST_PROTOCOL)


def load_district(name: str) -> District | None:
    """
    Return a district by either loading it from the local storage
    or by downloading it if not present and storing it in local storage.
    """
    pass


def load_snow(id: int) -> Snow | None:
    """
    Return a drone analyze from the local storage or None if not found.
    """
    snow_data = get_data(data_path / "snow/snow.pkl")

    return snow_data.get(id, None)


def load_route(id: int) -> Route | None:
    """
    Return a route in the local storage or None if not found.
    Used for snowplows.
    """
    pass


def save_district(district: District) -> None:
    """
    Save a district object to the local storage.
    """
    pass


def create_snow(snow_data: list, related_district: str) -> Snow:
    """
    Create a new snow object and save it to the local storage.
    """
    snows: dict[int, Snow] = get_data(data_path / "snow/snow.pkl")
    indexes = list(snows.keys())
    max_ind = max(indexes) if len(indexes) != 0 else 0

    snow = Snow(snow_data, related_district)

    snows[max_ind + 1] = snow

    save_data(data_path / "snow/snow.pkl", snows)

    return snow


def save_route(route: Route) -> None:
    """
    Save a route object to the local storage.
    """
    pass
