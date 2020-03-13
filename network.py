from typing import List

import os
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from itertools import permutations, groupby

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
        edge_df = read_node_df(cwd+'/data/edges.csv')
    
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
                'weight': row['frequency']
            }
            G.add_edge(edge_info['source'], edge_info['target'], weight=edge_info['weight'])
        
        # Centrality calculations
        G = _compute_centrality_measures(G)
        
        # Clustering coefficients
        G = _compute_clustering_coefficients(G)
    
    return G


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
def _generate_intracluster_strength(G:nx.Graph, nodes: List[int]):
    node_pairs = [sorted(pair) for pair in permutations(nodes, 2)]
    node_pairs.sort()
    node_pairs = list(k for k,_ in groupby(node_pairs))
    
    total_interactions = 0
    for pair in node_pairs:
        total_interactions += G[pair[0]][pair[1]]['weight']
    
    return total_interactions/len(nodes)    

def get_cliques_by_size(G:nx.Graph):
    maximal_cliques = list(nx.find_cliques(G))
    maximal_clique_sizes = [len(clique) for clique in list(nx.find_cliques(G))]
    
    maximal_cliques_dict = defaultdict(list)
    for idx in range(len(maximal_cliques)):
        maximal_cliques_dict[maximal_clique_sizes[idx]].append({'nodes': maximal_cliques[idx]})
    
    return maximal_cliques_dict

def generate_clique_metrics(G: nx.Graph):
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