#
# data/route.py
#

import lib

class Route:
    def __init__(self, route: list, related_district: str) -> None:
        self.id = id
        self.route = route
        self.related_district = related_district

    def __str__(self) -> str:
        return f"Route for {self.related_district}"

    def __repr__(self) -> str:
        return self.__str__()

def create_route(route_data: list, related_district: str) -> Route:
    """
    Create a new route object and save it to local storage.
    """

    routes: dict[int, Route] = lib.get_data("routes.pkl")
    indexes = list(routes.keys())
    max_ind = max(indexes) if len(indexes) != 0 else 0

    route = Route(route_data, related_district)

    routes[max_ind + 1] = route

    lib.save_data("routes.pkl", routes)

    return route
