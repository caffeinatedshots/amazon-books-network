from typing import Dict
from typing import List

import os
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from itertools import permutations, groupby
from operator import itemgetter
import matplotlib.pyplot as plt

from app import app
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from helpers import *

cwd = os.getcwd()
"""
NetworkX Object generation
"""
def read_node_df(node_file:str, dtype:bool=False):
    node_df = pd.read_csv(node_file)
    node_df.rename(
        columns={
            "Genre": "genre",
            "Number of Pages": "num_pages",
            "Price": "price",
            "Sales Rank": "sales_rank",
            "Average Rating": "avg_rating",
            "Number of Reviews": "num_reviews"
        },
        inplace=True
    )
    return node_df

def read_edge_df(edge_file:str):
    edge_df = pd.read_csv(edge_file)
    edge_df.rename(
        columns={
            "Source": "source",
            "Target": "target",
            "Frequency": "weight"
        },
        inplace=True
    )
    return edge_df

def generate_graph(dataset:str='amazon'):
    G = nx.Graph()
    
    if dataset == 'amazon':
        node_df = read_node_df(cwd+'/data/nodes.csv')
        edge_df = read_edge_df(cwd+'/data/edges.csv')
    
        # Create Nodes
        for index, row in node_df.iterrows():
            node_info = {
                'id': row['id'],
                'genre': row['genre'],
                'num_pages': row['num_pages'],
                'price': row['price'],
                'sales_rank': row['sales_rank'],
                'avg_rating': row['avg_rating'],
                'num_reviews': row['num_reviews']
            }
            G.add_node(row['id'], id=node_info['id'])
            G.nodes[row['id']]['genre'] = node_info['genre']
            G.nodes[row['id']]['num_pages'] = node_info['num_pages']
            G.nodes[row['id']]['price'] = node_info['price']
            G.nodes[row['id']]['sales_rank'] = node_info['sales_rank']
            G.nodes[row['id']]['avg_rating'] = node_info['avg_rating']
            G.nodes[row['id']]['num_reviews'] = node_info['num_reviews']
        # Create edges
        for index, row in edge_df.iterrows():
            edge_info = {
                'source': row['source'],
                'target': row['target'],
                'weight': row['weight']
            }
            G.add_edge(edge_info['source'], edge_info['target'], weight=edge_info['weight'])
        
        # Centrality calculations
        G = _compute_centrality_measures(G)
        
        # Clustering coefficients
        G = _compute_clustering_coefficients(G)
    
    return G


def _compute_articulation_points(G: nx.Graph):
    """
    An articulation point or cut vertex is any node whose removal (along with all its incident edges) increases the number of connected components of a graph.
    """
    articulation_points = list(nx.articulation_points(G))
    
    return articulation_points

def _compute_biconnected_components_edges(G: nx.Graph):
    """
    Biconnected components are maximal subgraphs such that the removal of a node (and all edges incident on that node) will not disconnect the subgraph.
    ------------------
    Returns a list of lists of length 2: [Set, List of tuple pairs (edges)]
    """
    biconnected_components = list(nx.biconnected_components(G))
    biconnected_edges = list(nx.biconnected_component_edges(G))
    components_and_edges = [[biconnected_components[idx], biconnected_edges[idx]] for idx in range(len(biconnected_components))]

    return components_and_edges

def _compute_centrality_measures(G: nx.Graph):
    degree_centrality = list(nx.degree_centrality(G).values())
    betweenness_centrality = list(nx.betweenness_centrality(G).values())
    closeness_centrality = list(nx.closeness_centrality(G).values())
    
    for idx in range(len(G)):
        G.nodes[idx]['degree_centrality'] = degree_centrality[idx]
        G.nodes[idx]['betweenness_centrality'] = betweenness_centrality[idx]
        G.nodes[idx]['closeness_centrality'] = closeness_centrality[idx]
    
    return G

def _compute_clustering_coefficients(G: nx.Graph):
    clustering_coefficients = nx.clustering(G)
    
    for idx in range(len(G)):
        G.nodes[idx]['clustering_coefficient'] = clustering_coefficients[idx]
    
    return G


"""
Clique Analysis
"""
def _generate_intracluster_strength(G:nx.Graph, nodes: List[int]) -> int:
    node_pairs = [sorted(pair) for pair in permutations(nodes, 2)]
    node_pairs.sort()
    node_pairs = list(k for k,_ in groupby(node_pairs))
    
    total_interactions = 0
    for pair in node_pairs:
        total_interactions += G[pair[0]][pair[1]]['weight']
    
    return total_interactions/len(nodes)    

def get_cliques_by_size(G:nx.Graph) -> Dict[str,List[int]]:
    maximal_cliques = list(nx.find_cliques(G))
    maximal_clique_sizes = [len(clique) for clique in list(nx.find_cliques(G))]
    
    maximal_cliques_dict = defaultdict(list)
    for idx in range(len(maximal_cliques)):
        maximal_cliques_dict[maximal_clique_sizes[idx]].append({'nodes': maximal_cliques[idx]})
    
    return maximal_cliques_dict

def generate_clique_metrics(G: nx.Graph) -> Dict[str,List[int]]:
    maximal_cliques_dict = get_cliques_by_size(G)
    
    for k,v in maximal_cliques_dict.items():
        for clique_info in v:
            avg_price = np.mean([G.nodes[node]['price'] for node in clique_info['nodes']])
            avg_rating = np.mean([G.nodes[node]['avg_rating'] for node in clique_info['nodes']])
            avg_review = np.mean([G.nodes[node]['num_reviews'] for node in clique_info['nodes']])
            
            clique_info['avg_price'] = avg_price
            clique_info['avg_rating'] = avg_rating
            clique_info['avg_review'] = avg_review
            clique_info['intracluster_strength'] = _generate_intracluster_strength(G, clique_info['nodes'])
    
    return maximal_cliques_dict

def get_ego_network(G:nx.Graph, rank:int):
    """
    Returns information of nth rank ego-network.
    ------------------------
    ego_node: Ego node
    hub_ego: networkx.Graph
    pos: Dict[int, List[float, float]]

    pos: Key of represents node connected to ego_node and the values are x-y coordinates.
    """
    node_and_degree = G.degree()
    (ego_node, _) = sorted(node_and_degree, key=itemgetter(1))[-1*rank]

    hub_ego = nx.ego_graph(G, ego_node)
    pos = nx.spring_layout(hub_ego)

    return ego_node, hub_ego, pos

def get_node_edge_traces(G:nx.Graph, n_ranks:int):
    """
    Returns Plotly Graph objects for n ego-networks.
    """
    node_traces = []
    edge_traces = []

    for i in range(n_ranks):
        temp_node_x = []
        temp_node_y = []
        temp_edge_x = []
        temp_edge_y = []
        ego_node, hub_ego, pos = get_ego_network(G, i+1) # ego_node to be used to make it red

        for edge in hub_ego.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            temp_edge_x.append(x0)
            temp_edge_x.append(x1)
            temp_edge_x.append(None)
            temp_edge_y.append(y0)
            temp_edge_y.append(y1)
            temp_edge_y.append(None)

        edge_trace = go.Scatter(
            x=temp_edge_x, y=temp_edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        for node in hub_ego.nodes():
            x, y = pos[node]
            temp_node_x.append(x)
            temp_node_y.append(y)

        node_trace = go.Scatter(
            x=temp_node_x, y=temp_node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2
            )
        )

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(hub_ego.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(
                # Append all node information here
                f"<b>Node: {str(node)}</b><br /><b>Properties:</b><br />\
                    # of connections: {str(len(adjacencies[1]))}\
                "
            )

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        node_traces.append(node_trace)
        edge_traces.append(edge_trace)

    return node_traces, edge_traces

def generate_ego_network(G:nx.Graph, n_ranks:int):
    node_traces, edge_traces = get_node_edge_traces(G, n_ranks)

    plotly_figures = []

    for idx in range(len(node_traces)):
        fig = go.Figure(
            data=[node_traces[idx], edge_traces[idx]],
            layout=go.Layout(
                title={
                    "text":f"<br>Rank {idx+1} Ego Network"},
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                
            )
        )
        fig.update_layout(
            title=style_title(),
            font=style_font()
        )
        plotly_figures.append(fig)

    return plotly_figures


# Initialize NetworkX graph
networkGraph = generate_graph()
# Generate Plotly content
content = html.Section(
    children = [
        html.Div([
            html.H2("Network Analysis at a glance...", className="align-center"),
            html.Div([
                dcc.Input(id="ego_network_count", type="text", value="0", placeholder="Top-N Ego-networks"),
            ], style = {
                "textAlign": "center" 
            }),
            html.Div(id="ego_network")
        ])
    ]
)
@app.callback(
    Output("ego_network", "children"),
    [Input("ego_network_count", "value")],
)
def update_ego_network(ego_network_count):
    # To prevent callback error
    if ego_network_count == "":
        ego_network_count = 0

    ego_network_count = int(ego_network_count)
    children = [
        dcc.Graph(
            id = f'ego_network_{i}',
            figure = generate_ego_network(networkGraph, ego_network_count)[i],
            config = {"displayModeBar" : False}
        ) for i in range(ego_network_count)
    ]
    return children