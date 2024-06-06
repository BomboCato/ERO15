#
# drone/snow.py
#

import random

from lib.districts import District


def gen_random_snow(district: District) -> District:
    """
    Return a district with edges having random snow attribute.
    """
    new_dist = district.copy()

    for u, v, k in new_dist.graph.edges(keys=True):
        new_dist.graph[u][v][k]["snow"] = random.randint(0, 30)

    return new_dist
