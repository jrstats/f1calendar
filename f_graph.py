import networkx as nx
from geopy import distance

def skip_edge(i, x, j, y, connection_col=None):
    # add all edges (but prevent double count)
    if connection_col is None:
        return i >= j

    # add edges only if y is sequentially after x in column `connection_col`
    return int(x[connection_col]) != int(y[connection_col]) - 1

def df_to_graph(df, connection_col=None):
    G = nx.Graph()
    pos = {}

    # add nodes
    for i, x in df.iterrows():
        G.add_node(i, name=x["Grand Prix"], round=x["Round"], date=x["Race date"], loc=x["Coordinates"])
        pos[i] = x["Coordinates"][1], x["Coordinates"][0]

    # add edges
    for i, x in df.iterrows():
        for j, y in df.iterrows():
            if skip_edge(i, x, j, y, connection_col):
                continue
            dist_km = distance.distance(G.nodes()[i]["loc"], G.nodes()[j]["loc"]).kilometers
            G.add_edge(i,j, dist_km=dist_km, track0=x["Grand Prix"], track1=y["Grand Prix"])

    return G, pos


def graph_to_distances(graph, key="dist_km"):
    distances = []
    for x in graph.edges():
        d = x[0], x[1], graph.edges()[x][key] 
        distances.append(d)

    return distances

def total_graph_distance(graph, key="dist_km"):
    return sum(graph.edges()[x][key] for x in graph.edges())