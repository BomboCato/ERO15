import osmnx as ox

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
ox.plot_graph(G)