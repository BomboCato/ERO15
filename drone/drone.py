import osmnx as ox
import networkx as nx
import random
import scipy as sp

filename = 'montreal.osm'

# Saves an undirected graph of Montreal in a .osm file
def saveMontrealGraph(file):
    G = ox.graph_from_place('Montreal, Canada', network_type='drive')
    G = ox.convert.to_undirected(G)
    ox.save_graphml(G, filepath='drone/' + file)

# Retrieve graph stored in a .osm file
def retrieveGraph(file):
    return ox.load_graphml('drone/' + file)

# saveMontrealGraph(filename)
G = retrieveGraph(filename)

G1 = ox.graph_from_place('Outremont, Montreal', network_type='drive')
G2 = ox.graph_from_place('Verdun, Montreal', network_type='drive')
G3 = ox.graph_from_place('Plateau Mont-Royal, Montreal', network_type='drive')
G4 = ox.graph_from_place('Rivière-des-Prairies–Pointe-aux-Trembles, Montreal', network_type='drive')
G5 = ox.graph_from_place('Anjou, Montreal', network_type='drive')
G6 = nx.compose_all([G1, G2, G3, G4, G5])

for u, v in G.edges():
    G[u][v][0]['snow'] = random.randint(0, 15)
ec = ['r' if (G[u][v][0]['snow'] >= 2.5 and G[u][v][0]['snow'] <= 15) else 'b' for u, v, k in G.edges(keys=True)]

# PARCOURS DRONE SUR G (AJOUTER UN ATTRIBUT POUR DIRE SI IL FAUT DENEIGER)


# FAIRE UNE FONCTION QUI RETOURNE LE GRAPHE G6 AVEC CE NOUVEL ATTRIBUT (retourner R quoi)
R=G.copy()
R.remove_nodes_from(n for n in G if n not in G6)


ox.plot_graph(R, edge_color=ec)