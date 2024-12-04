# pip install networkx, plotly, fa2, numpy, python-louvain
import json
import networkx as nx
import plotly.graph_objects as go
from fa2 import ForceAtlas2
import numpy as np
import community as community_louvain

def create_cooccurrence_matrix(file_name, threshold=1):
    print("Opening file...")
    f = open("data/" + file_name, "r", encoding="utf-8")
    data = json.loads(f.read())
    f.close()
    print("File loaded successfully.")

    cooccurrence = {}
    print("Processing data...")
    for year in data["data-all"]:
        for month in data["data-all"][year]:
            for day in data["data-all"][year][month]:
                print(f"Processing day: {day}/{month}/{year}")
                for article in data["data-all"][year][month][day]:
                    keywords = list(article['kws'].keys())
                    keywords = [kw for kw in keywords if article['kws'][kw] > threshold]
                    for i in range(len(keywords)):
                        for j in range(i + 1, len(keywords)):
                            pair = tuple(sorted([keywords[i], keywords[j]]))
                            if pair in cooccurrence:
                                cooccurrence[pair] += 1
                            else:
                                cooccurrence[pair] = 1
    print(f"Data processing completed. {len(cooccurrence)} pairs of keywords found.")
    return cooccurrence

def save_graph_to_graphml(cooccurrence, output_file, threshold=25):
    print("Creating graph...")
    G = nx.Graph()

    for (kw1, kw2), count in cooccurrence.items():
        if count < threshold:
            continue
        G.add_edge(kw1, kw2, weight=count)
    print("Saving graph to GraphML format...")
    nx.write_graphml(G, output_file)
    print(f"Graph saved to {output_file}")

def keep_largest_component_du_graphe_en_gros(G):
    largest_component = max(nx.connected_components(G), key=len)
    return G.subgraph(largest_component).copy()

def normalize_size(degree, min_degree, max_degree, min_size, max_size):
    if max_degree == min_degree:
        return min_size
    return ((degree - min_degree) / (max_degree - min_degree)) * (max_size - min_size) + min_size

def plot_graph(G, display_plot=True, output_file=None):
    min_size = 10
    max_size = 50
    scaling_ratio = 3.0
    gravity = 0.6
    edge_color = '#d2d2d2'

    degrees = dict(G.degree())
    min_degree = min(degrees.values())
    max_degree = max(degrees.values())

    print("Applying ForceAtlas2 layout...")
    forceatlas2 = ForceAtlas2(
        outboundAttractionDistribution=True,
        linLogMode=False,
        adjustSizes=False,
        edgeWeightInfluence=1.0,
        jitterTolerance=1.0,
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        scalingRatio=scaling_ratio,
        strongGravityMode=False,
        gravity=gravity,
        verbose=True
    )
    positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=2000)
    print("Layout applied successfully.")

    print("Keeping largest connected component and recalculating positions...")
    G = keep_largest_component_du_graphe_en_gros(G)
    positions = forceatlas2.forceatlas2_networkx_layout(G, pos=positions, iterations=1000)

    partition = community_louvain.best_partition(G)
    print(f"Number of communities (Louvain method): {len(set(partition.values()))}")

    print("Creating edge traces...")
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    print("Edge traces created.")

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color=edge_color),
        hoverinfo='none',
        mode='lines')

    print("Creating node traces...")
    node_x = []
    node_y = []
    node_color = []
    node_size = []
    node_text = []
    for node in G.nodes():
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(partition.get(node, 0))
        node_size.append(normalize_size(degrees[node], min_degree, max_degree, min_size, max_size))
        node_text.append(node)
    print("Node traces created.")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,  # Adding labels to nodes
        textposition='top center',
        marker=dict(
            showscale=False,  # Hiding the legend bar
            colorscale='YlGnBu',
            size=node_size,
            color=node_color,
            line_width=0))  # Removing node borders

    node_trace.marker.color = node_color
    node_trace.text = node_text

    print("Creating figure...")
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,  # Ensuring the legend is hidden
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    print("Figure created")
    
    if output_file:
        fig.write_html(output_file)
        print(f"Figure saved to {output_file}")
    if display_plot:
        fig.show()
        print("Graph displayed successfully.")

def all_files_graph(file_list, display_plot=True):
    """
    make one sigle graph with all cooccurrences from all files
    """
    cooccurrence = {}
    for output_name, file_name in file_list.items():
        cooccurrence.update(create_cooccurrence_matrix(file_name, threshold=0))
    save_graph_to_graphml(cooccurrence, f"graphes/output_all.graphml", threshold=25)
    G = nx.read_graphml(f"graphes/output_all.graphml")
    plot_graph(G, display_plot=True, output_file=f"graphes/graph_all.html")
    return G

# Usage

# # Génération du graphe pour le fichier et le nom suivant 
# file_name = "topaz-data732--france--www.fdesouche.com--20190101--20211231.json"
# output_name = "france_fdesouche"

# cooccurrence = create_cooccurrence_matrix(file_name)
# # Save graph to GraphML format (Gephi, plotly)
# save_graph_to_graphml(cooccurrence, f"graphes/output_{output_name}.graphml")
# # Load graph and plot via plotly
# G = nx.read_graphml(f"graphes/output_{output_name}.graphml")
# plot_graph(G, display_plot=True, output_file=f"graphes/graph_{output_name}.html")


file_list = {
    "france_fdesouche": "topaz-data732--france--www.fdesouche.com--20190101--20211231.json",
    "france_egalite": "topaz-data732--france--www.egaliteetreconciliation.fr--20190101--20211231.json",
    "france_sputnik": "topaz-data732--france--fr.sputniknews.africa--20190101--20211231.json",
    "france_presstv": "topaz-data732--france--french.presstv.ir--20190101--20211231.json",
    "mali_egalite": "topaz-data732--mali--www.egaliteetreconciliation.fr--20190101--20211231.json",
    "mali_sputnik": "topaz-data732--mali--fr.sputniknews.africa--20190101--20211231.json",
    "mali_presstv": "topaz-data732--mali--french.presstv.ir--20190101--20211231.json",
}

# Save graph to GraphML format (Gephi, plotly)
for output_name, file_name in file_list.items():
    cooccurrence = create_cooccurrence_matrix(file_name, threshold=0)
    save_graph_to_graphml(cooccurrence, f"graphes/output_{output_name}.graphml", threshold=25)
    
input("Press enter to continue...")
# Load graph and plot via plotly
for output_name, file_name in file_list.items():
    G = nx.read_graphml(f"graphes/output_{output_name}.graphml")
    plot_graph(G, display_plot=False, output_file=f"graphes/graph_{output_name}.html")
    
input("Press enter to continue...")
# Generate a graph with all cooccurrences from all files
G = all_files_graph(file_list, display_plot=True)
