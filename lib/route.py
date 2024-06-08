#
# lib/route.py
#

from enum import Enum
import lib.lib as lib


class RouteType(Enum):
    """
    Enum for the type of route.
    """

    DRONE = 0
    SNOWPLOW = 1


class Route:
    def __init__(
        self,
        route: list,
        related_district: str,
        route_type: RouteType,
        route_id: int = -1,
    ) -> None:
        self.id = route_id
        self.route = route
        self.related_district = related_district
        self.type = route_type

    def __str__(self) -> str:
        return f"Route for {self.related_district}"

    def __repr__(self) -> str:
        return self.__str__()


def create_route(
    route_data: list, related_district: str, route_type: RouteType
) -> Route:
    """
    Create a new route object and save it to local storage.
    """

    routes: dict[int, Route] = lib.get_data("routes.pkl")
    indexes = list(routes.keys())
    max_ind = max(indexes) + 1 if len(indexes) != 0 else 0

    route = Route(route_data, related_district, route_type, max_ind)

    routes[max_ind] = route

    lib.save_data("routes.pkl", routes)

    return route


def load_route(route_id: int) -> Route:
    """
    Load a route object from local storage. Return None if not found.
    """

    routes: dict[int, Route] = lib.get_data("routes.pkl")

    return routes.get(route_id, None)
