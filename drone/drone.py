import osmnx as ox
import networkx as nx
import random
import scipy as sp
import sys
from erolib import connect, euler


filename = "montreal.osm"


# Saves an undirected graph of Montreal in a .osm file
def saveMontrealGraph(file):
    G = ox.graph_from_place("Montreal, Canada", network_type="drive")
    G = ox.convert.to_undirected(G)
    ox.save_graphml(G, filepath="drone/" + file)


# Retrieve graph stored in a .osm file
def retrieveMontrealGraph(file):
    return ox.load_graphml("drone/" + file)


# saveMontrealGraph(filename)
G = retrieveMontrealGraph(filename)

G1 = ox.graph_from_place(
    "Outremont, Montreal", network_type="drive"
).to_undirected()
G2 = ox.graph_from_place(
    "Verdun, Montreal", network_type="drive"
).to_undirected()
G3 = ox.graph_from_place(
    "Plateau Mont-Royal, Montreal", network_type="drive"
).to_undirected()
G4 = ox.graph_from_place(
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal",
    network_type="drive",
).to_undirected()
G5 = ox.graph_from_place(
    "Anjou, Montreal", network_type="drive"
).to_undirected()
G6 = nx.compose_all([G1, G2, G3, G4, G5])

for u, v in G.edges():
    for key in G[u][v]:
        G[u][v][key]["snow"] = random.randint(0, 15)
ec = [
    (
        "r"
        if (G[u][v][k]["snow"] >= 2.5 and G[u][v][k]["snow"] <= 15)
        else "b"
    )
    for u, v, k in G.edges(keys=True)
]

# PARCOURS DRONE SUR G (AJOUTER UN ATTRIBUT POUR DIRE SI IL FAUT DENEIGER)


# Returns the graph containing the 5 districts
# To use after parcouring the graph with the drone
def districts_graph():
    R = G.copy()
    R.remove_nodes_from(n for n in G if n not in G6)
    return R


R = districts_graph()
G1_conn: nx.MultiGraph = connect.connect(G1, False)
G1_eul: nx.MultiGraph = euler.eulerize(G1_conn, False)

# ox.plot_graph(G1, edge_color=ec)
# ox.plot_graph(G1_conn, edge_color=ec)
# ox.plot_graph(G1_eul, edge_color=ec)
