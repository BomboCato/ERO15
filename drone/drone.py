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
# G = retrieveGraph(filename)

G = ox.graph_from_place('Verdun, Montreal', network_type='drive')

print("G.edges: ", G.edges(keys=True, data=True))
# print("G: ", G.edges(keys=True, data=True))
for u, v in G.edges():
    print("u: ", u)
    print("v: ", v)
    G[u][v][0]['snow'] = random.randint(0, 15)
ec = ['r' if (G[u][v][0]['snow'] >= 2.5 and G[u][v][0]['snow'] <= 15) else 'b' for u, v, k in G.edges(keys=True)]
ox.plot_graph(G, edge_color=ec)