from typing import List
from typing import Dict
from typing import Set
from typing import Tuple

import networkx as nx


def _compute_articulation_points(G: nx.Graph) -> List[int]:
	"""
	An articulation point or cut vertex is any node whose removal (along with all its incident edges) increases the number of connected components of a graph.
    Source: https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/components/biconnected.html#articulation_points
	"""
	articulation_points = list(nx.articulation_points(G))
	
	return articulation_points

def _compute_biconnected_components_edges(G: nx.Graph) -> List[List[Tuple[int], Set[int]]]:
	"""
	Biconnected components are maximal subgraphs such that the removal of a node (and all edges incident on that node) will not disconnect the subgraph.
    Source: 
    - https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/components/biconnected.html#biconnected_components
    - https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/components/biconnected.html#biconnected_component_edges
	------------------
	Returns a list of lists of length 2: [Set, List of tuple pairs (edges)]
	"""
	biconnected_components = list(nx.biconnected_components(G))
	biconnected_edges = list(nx.biconnected_component_edges(G))
	components_and_edges = [[biconnected_components[idx], biconnected_edges[idx]] for idx in range(len(biconnected_components))]

	return components_and_edges

def _compute_degree_assortativity_coefficient(G: nx.Graph) -> float:
    """
    Source: https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/assortativity/correlation.html#degree_assortativity_coefficient
    """
    return nx.degree_assortativity_coefficient(G)

def _compute_rich_club_coefficient(G: nx.Graph) -> Dict[int,float]:
    """
    Source: https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/richclub.html#rich_club_coefficient
    """
    return nx.rich_club_coefficient(G)

def _compute_avg_degree_connectivity(G: nx.Graph) -> Dict[int,float]:
    """
    Source: https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.assortativity.k_nearest_neighbors.html#networkx.algorithms.assortativity.k_nearest_neighbors
    """
    return nx.k_nearest_neighbors(G)

def _compute_bridges(G: nx.Graph) -> List[Tuple[int]]:
    """
    Source: https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/bridges.html#bridges
    """
    return list(nx.bridges(G))

def _compute_shortest_path(G: nx.Graph) -> Dict[Dict[int,List[int]]]:
    """
    Source: https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/shortest_paths/generic.html#shortest_path
    """
    return nx.shortest_path(G)