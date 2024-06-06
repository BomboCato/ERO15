#
# data/snow.py
#

import data.lib as lib


class Snow:
    def __init__(
        self, snow_data: list, related_district: str, id: int = -1
    ) -> None:
        self.id = id
        self.data = snow_data
        self.related_district = related_district

    def __str__(self) -> str:
        return f"Snow for '{self.related_district} with id {self.id}'"

    def __repr__(self) -> str:
        return self.__str__()


def create_snow(snow_data: list, related_district: str) -> Snow:
    """
    Create a new snow object and save it to the local storage.
    """
    snows: dict[int, Snow] = lib.get_data("snow.pkl")
    indexes = list(snows.keys())
    max_ind = max(indexes) + 1 if len(indexes) != 0 else 0

    snow = Snow(snow_data, related_district, max_ind)

    snows[max_ind] = snow

    lib.save_data("snow.pkl", snows)

    return snow


def load_snow(id: int) -> Snow | None:
    """
    Return a drone analyze from the local storage or None if not found.
    """
    snow_data = lib.get_data("snow.pkl")

    return snow_data.get(id, None)
