import osmnx as ox
import networkx as nx
import random
import scipy as sp
import sys
from erolib import connect, euler
# from erolib_windows import connect, euler

filename = "montreal.osm"

def saveMontrealGraph(file):
    """
    Saves an undirected graph of Montreal in a .osm file
    """
    G = ox.graph_from_place("Montreal, Canada", network_type="drive")
    G = ox.convert.to_undirected(G)
    ox.save_graphml(G, filepath="drone/" + file)


# Retrieve graph stored in a .osm file
def retrieveMontrealGraph(file):
    """
    Returns the undirected graph of Montreal stored in the .osm file
    """
    return ox.load_graphml("drone/" + file)


# saveMontrealGraph(filename)
G = retrieveMontrealGraph(filename)

def saveDistrictsGraph():
    """
    Creates and saves a graph for each district in Montreal into a file in the districts/ folder
    """
    G1 = ox.graph_from_place('Ahuntsic-Cartierville, Montreal', network_type='drive').to_undirected()
    G2 = ox.graph_from_place('Anjou, Montreal', network_type='drive').to_undirected()
    G3 = ox.graph_from_place('Côte-des-Neiges–Notre-Dame-de-Grâce, Montreal', network_type='drive').to_undirected()
    G4 = ox.graph_from_place('Lachine, Montreal', network_type='drive').to_undirected()
    G5 = ox.graph_from_place('LaSalle, Montreal', network_type='drive').to_undirected()
    G6 = ox.graph_from_place('Plateau Mont-Royal, Montreal', network_type='drive').to_undirected()
    G7 = ox.graph_from_place('Le Sud-Ouest, Montreal', network_type='drive').to_undirected()
    G8 = ox.graph_from_place('Île-Bizard–Sainte-Geneviève, Montreal', network_type='drive').to_undirected()
    G9 = ox.graph_from_place('Mercier–Hochelaga-Maisonneuve, Montreal', network_type='drive').to_undirected()
    G10 = ox.graph_from_place('Montréal-Nord, Montreal', network_type='drive').to_undirected()
    G11 = ox.graph_from_place('Outremont, Montreal', network_type='drive').to_undirected()
    G12 = ox.graph_from_place('Pierrefonds-Roxboro, Montreal', network_type='drive').to_undirected()
    G13 = ox.graph_from_place('Rivière-des-Prairies–Pointe-aux-Trembles, Montreal', network_type='drive').to_undirected()
    G14 = ox.graph_from_place('Rosemont–La Petite-Patrie, Montreal', network_type='drive').to_undirected()
    G15 = ox.graph_from_place('Saint-Laurent, Montreal', network_type='drive').to_undirected()
    G16 = ox.graph_from_place('Saint-Léonard, Montreal', network_type='drive').to_undirected()
    G17 = ox.graph_from_place('Verdun, Montreal', network_type='drive').to_undirected()
    G18 = ox.graph_from_place('Ville-Marie, Montreal', network_type='drive').to_undirected()
    G19 = ox.graph_from_place('Villeray–Saint-Michel–Parc-Extension, Montreal', network_type='drive').to_undirected()   
    
    ox.save_graphml(G1, filepath="drone/districts/ahuntsic.osm")
    ox.save_graphml(G2, filepath="drone/districts/anjou.osm")
    ox.save_graphml(G3, filepath="drone/districts/cote_des_neiges.osm")
    ox.save_graphml(G4, filepath="drone/districts/lachine.osm")
    ox.save_graphml(G5, filepath="drone/districts/lasalle.osm")
    ox.save_graphml(G6, filepath="drone/districts/plateau_mont_royal.osm")
    ox.save_graphml(G7, filepath="drone/districts/sud_ouest.osm")
    ox.save_graphml(G8, filepath="drone/districts/ilebizard.osm")
    ox.save_graphml(G9, filepath="drone/districts/mercier.osm")
    ox.save_graphml(G10, filepath="drone/districts/montreal_nord.osm")
    ox.save_graphml(G11, filepath="drone/districts/outremont.osm")
    ox.save_graphml(G12, filepath="drone/districts/pierrefonds.osm")
    ox.save_graphml(G13, filepath="drone/districts/riviere.osm")
    ox.save_graphml(G14, filepath="drone/districts/rosemont.osm")
    ox.save_graphml(G15, filepath="drone/districts/saint_laurent.osm")
    ox.save_graphml(G16, filepath="drone/districts/saint_leonard.osm")
    ox.save_graphml(G17, filepath="drone/districts/verdun.osm")
    ox.save_graphml(G18, filepath="drone/districts/ville_marie.osm")
    ox.save_graphml(G19, filepath="drone/districts/villeray.osm")


def retrieveDistrictsGraph():
    """
    Returns a list with the graphs of each district from the files saved in districts/ folder
    """
    res = []
    res.append(ox.load_graphml("drone/districts/ahuntsic.osm"))
    res.append(ox.load_graphml("drone/districts/anjou.osm"))
    res.append(ox.load_graphml("drone/districts/cote_des_neiges.osm"))
    res.append(ox.load_graphml("drone/districts/lachine.osm"))
    res.append(ox.load_graphml("drone/districts/lasalle.osm"))
    res.append(ox.load_graphml("drone/districts/plateau_mont_royal.osm"))
    res.append(ox.load_graphml("drone/districts/sud_ouest.osm"))
    res.append(ox.load_graphml("drone/districts/ilebizard.osm"))
    res.append(ox.load_graphml("drone/districts/mercier.osm"))
    res.append(ox.load_graphml("drone/districts/montreal_nord.osm"))
    res.append(ox.load_graphml("drone/districts/outremont.osm"))
    res.append(ox.load_graphml("drone/districts/pierrefonds.osm"))
    res.append(ox.load_graphml("drone/districts/riviere.osm"))
    res.append(ox.load_graphml("drone/districts/rosemont.osm"))
    res.append(ox.load_graphml("drone/districts/saint_laurent.osm"))
    res.append(ox.load_graphml("drone/districts/saint_leonard.osm"))
    res.append(ox.load_graphml("drone/districts/verdun.osm"))
    res.append(ox.load_graphml("drone/districts/ville_marie.osm"))
    res.append(ox.load_graphml("drone/districts/villeray.osm"))
    return res

def generateSnow(G):
    """
    This function adds an attribute 'snow' whose value is a random int between 0 and 15 to all edges
    """
    for u, v, k in G.edges(keys=True):
        G[u][v][k]["snow"] = random.randint(0, 15)


# saveDistrictsGraph()
l = retrieveDistrictsGraph()
G_all = nx.compose_all(l)
generateSnow(G_all)


def getDistrictGraphSnow(i):
    R = G_all.copy()
    R.remove_nodes_from(n for n in G_all if n not in l[i])
    R.remove_edges_from(e for e in G_all.edges if e not in l[i].edges)
    return R

ec = [
    (
        "r"
        if (G_all[u][v][k]["snow"] >= 2.5 and G_all[u][v][k]["snow"] <= 15)
        else "b"
    )
    for u, v, k in G_all.edges(keys=True)
]

# ox.plot_graph(G_all, edge_color=ec)


d1 = getDistrictGraphSnow(1)
# print(d1.edges(data=True))
ec = [
    (
        "r"
        if (d1[u][v][k]["snow"] >= 2.5 and d1[u][v][k]["snow"] <= 15)
        else "b"
    )
    for u, v, k in d1.edges(keys=True)
]
# ox.plot_graph(d1, edge_color=ec)

G_districts = nx.compose_all([getDistrictGraphSnow(1), getDistrictGraphSnow(5), getDistrictGraphSnow(10), getDistrictGraphSnow(12), getDistrictGraphSnow(16)]) # Graph containing all 5 districts to clear

generateSnow(G)
ec = [
    (
        "r"
        if (G[u][v][k]["snow"] >= 2.5 and G[u][v][k]["snow"] <= 15)
        else "b"
    )
    for u, v, k in G.edges(keys=True)
]

# PARCOURS DRONE SUR G (AJOUTER UN ATTRIBUT POUR DIRE SI IL FAUT DENEIGER)
def drone(G):
    """
    Returns a tuple (G, circuit) where G is the graph with attribute 'need_clear' added and circuit is path taken by the drone
    """
    G_conn = connect.connect(G, False)
    G_eul = euler.eulerize(G_conn, False)
    for u, v, k, data in G_eul.edges(keys=True, data=True):
        snow = data.get('snow', 0) # tries to get value of attribute 'snow', if not found returns 0
        if snow >= 2.5 and snow <= 15:
            G_eul[u][v][k]["need_clear"] = True
        else:
            G_eul[u][v][k]["need_clear"] = False
    circuit = nx.eulerian_circuit(G_eul)
    return (G_eul, circuit)

# Returns the graph containing the 5 districts
# To use after parcouring the graph with the drone
def districts_graph():
    R=G.copy()
    R.remove_nodes_from(n for n in G if n not in G_districts)
    return R


R = districts_graph()
generateSnow(l[16])
(G_eul, circuit) = drone(l[16])
ox.plot_graph(G_eul)
# ox.plot_graph(R, edge_color=ec) 

# G1_conn: nx.MultiGraph = connect.connect(l[0], False)
# G1_eul: nx.MultiGraph = euler.eulerize(G1_conn, False)

# ox.plot_graph(G1, edge_color=ec)
# ox.plot_graph(G1_conn, edge_color=ec)
# ox.plot_graph(G1_eul, edge_color=ec)
