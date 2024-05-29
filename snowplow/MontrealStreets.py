import osmnx as ox
import folium as flm

districts = [
    "Outremont, Montréal, Québec, Canada",
    "Verdun, Montréal, Québec, Canada",
    "Anjou, Montréal, Québec, Canada",
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montréal, Québec, Canada",
    "Plateau Mont-Royal, Montréal, Québec, Canada",
]

placeName = "Montréal, Québec, Canada"

# Graphe des routes
graph = ox.graph_from_place(placeName, network_type="drive")
nodes, edges = ox.graph_to_gdfs(graph)
center = (nodes["y"].mean(), nodes["x"].mean())
map = flm.Map(location=center, zoom_start=11)

# Récupère les arrètes du graphe principal:
for _, row in edges.iterrows():
    points = [(point[1], point[0]) for point in row["geometry"].coords]
    flm.PolyLine(points, color="white", weight=2.5, opacity=0.7).add_to(
        map
    )

# Récupère les noeuds du graphe principal:
for _, row in nodes.iterrows():
    flm.CircleMarker(
        location=(row["y"], row["x"]),
        radius=0.03,
        color="grey",
        fill=False,
    ).add_to(map)


def get_districtGraph(district_name):
    districtGraph = ox.graph_from_place(
        district_name, network_type="drive"
    )
    return districtGraph


# Colore les quartiers importants et extraction de leurs graphes:
districtsGraphs = []

for district in districts:
    districtGraph = get_districtGraph(district)
    districtsGraphs.append(districtGraph)
    districtNodes, districtEdges = ox.graph_to_gdfs(districtGraph)
    if "Outremont, Montréal, Québec, Canada" == district:
        districtColor = "orange"
    elif "Verdun, Montréal, Québec, Canada" == district:
        districtColor = "purple"
    elif (
        "Rivière-des-Prairies–Pointe-aux-Trembles, Montréal, Québec, Canada"
        == district
    ):
        districtColor = "blue"
    elif "Plateau Mont-Royal, Montréal, Québec, Canada" == district:
        districtColor = "yellow"
    else:
        districtColor = "green"
    for _, row in districtEdges.iterrows():
        points = [(point[1], point[0]) for point in row["geometry"].coords]
        flm.PolyLine(
            points, color=districtColor, weight=2, opacity=0.7
        ).add_to(map)

# Numérote tous les noeuds pour pouvoir les manipuler plus facilement:
nodeData = {}
nodeCounter = 0

for districtGraph in districtsGraphs:
    index_node_map = {}
    districtNodes, _ = ox.graph_to_gdfs(districtGraph)
    for _, row in districtNodes.iterrows():
        nodeID = nodeCounter
        index_node_map[nodeID] = row
        flm.CircleMarker(
            location=(row["y"], row["x"]),
            radius=0.01,
            color="white",
            fill=False,
            popup=nodeID,
        ).add_to(map)
        nodeData[nodeID] = {
            "coordinates": (row["y"], row["x"]),
            "attributes": row.to_dict(),
        }
        nodeCounter += 1

# Pour relier de noeuds selon leur ID (se fier aux ID sur la carte, ici pour l'example j'ai relié Anjou à Mont-Royal):
node1 = 582
node2 = 3645
graph.add_edge(node1, node2)
node1Coords = nodeData[node1]["coordinates"]
node2Coords = nodeData[node2]["coordinates"]
flm.PolyLine(
    [node1Coords, node2Coords], color="red", weight=2, opacity=0.7
).add_to(map)
node3 = 3224
node4 = 379
graph.add_edge(node3, node4)
node3Coords = nodeData[node3]["coordinates"]
node4Coords = nodeData[node4]["coordinates"]
flm.PolyLine(
    [node3Coords, node4Coords], color="red", weight=2, opacity=0.7
).add_to(map)
node5 = 34
node6 = 3715
graph.add_edge(node5, node6)
node5Coords = nodeData[node5]["coordinates"]
node6Coords = nodeData[node6]["coordinates"]
flm.PolyLine(
    [node5Coords, node6Coords], color="red", weight=2, opacity=0.7
).add_to(map)
node7 = 1074
node8 = 2725
graph.add_edge(node7, node8)
node7Coords = nodeData[node7]["coordinates"]
node8Coords = nodeData[node8]["coordinates"]
flm.PolyLine(
    [node7Coords, node8Coords], color="red", weight=2, opacity=0.7
).add_to(map)
node9 = 538
node10 = 3134
graph.add_edge(node9, node10)
node9Coords = nodeData[node9]["coordinates"]
node10Coords = nodeData[node10]["coordinates"]
flm.PolyLine(
    [node9Coords, node10Coords], color="red", weight=2, opacity=0.7
).add_to(map)


map.save("montreal_map_with_comeback.html")
