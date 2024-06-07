#
# drone/snow.py
#

import random

from lib.districts import District
from datetime import datetime


def gen_random_snow(district: District, min_snow: float, max_snow: float) -> District:
    """
    Return a district with edges having random snow attribute.
    """
    new_dist = district.copy()
    random.seed(datetime.now().timestamp())

    for u, v, k in new_dist.graph.edges(keys=True):
        new_dist.graph[u][v][k]["snow"] = round(random.uniform(min_snow, max_snow), 3)

    return new_dist
