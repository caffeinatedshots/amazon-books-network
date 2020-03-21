from typing import Dict, List

import plotly.graph_objs as go
import dash_table
import dash_core_components as dcc

import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from itertools import permutations, groupby
from operator import itemgetter

import helpers

NODES_FILE = 'data/nodes.csv'
EDGES_FILE = 'data/edges.csv'

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

NODE_DF = read_node_df(NODES_FILE)
EDGE_DF = read_edge_df(EDGES_FILE)

def get_nclique_options():
	G = generate_graph()
	clique_graph_table_info = get_cliques_by_size(G)

	return [str(i+1) for i in range(len(clique_graph_table_info))]

def get_unique_genres(df = NODE_DF):
	return sorted(df['genre'].unique())

def get_sales_rank_categories(df = NODE_DF):
	lowest = int(df['sales_rank'].min())
	q1 = int(df['sales_rank'].quantile(0.25))
	median = int(df['sales_rank'].quantile(0.5))
	q3 = int(df['sales_rank'].quantile(0.75))
	highest = int(df['sales_rank'].max())
	return [
		f"{lowest} - {q1}",
		f"{q1 + 1} - {median}",
		f"{median + 1} - {q3}",
		f"{q3 + 1} - {highest}"
	]

def get_unique_ratings(df = NODE_DF):
	return sorted(df['avg_rating'].unique())

def get_review_categories(df = NODE_DF):
	lowest = int(df['num_reviews'].min())
	q1 = int(df['num_reviews'].quantile(0.25))
	median = int(df['num_reviews'].quantile(0.5))
	q3 = int(df['num_reviews'].quantile(0.75))
	highest = int(df['num_reviews'].max())
	return [
		f"{lowest} - {q1}",
		f"{q1 + 1} - {median}",
		f"{median + 1} - {q3}",
		f"{q3 + 1} - {highest}"
	]

def get_num_pages_quantiles(df = NODE_DF):
	return [int(df['num_pages'].quantile(i * 0.1)) for i in range(0, 11)]

def get_price_quantiles(df = NODE_DF):
	return [round(df['price'].quantile(i * 0.1), 2) for i in range(0, 11)]

def get_generic_insights(data_df:pd.DataFrame = NODE_DF):
	most_common_genre = data_df['genre'].mode()[0]
	
	min_pages = data_df['num_pages'].min()
	max_pages = data_df['num_pages'].max()
	avg_pages = data_df['num_pages'].mean()

	min_price = data_df['price'].min()
	max_price = data_df['price'].max()
	avg_price = data_df['price'].mean()
	
	min_reviews = data_df['num_reviews'].min()
	max_reviews = data_df['num_reviews'].max()
	avg_reviews = round(data_df['num_reviews'].mean())
	
	avg_rating = round(data_df['avg_rating'].mean())
	

	figure = {
		'data' : [
			go.Indicator(
				domain = {'x': [0, 0.33], 'y': [0.5, 1]},
				value = avg_pages,
				mode = "gauge+number",
				title = {'text': "(Min, Max, Avg) Pages"},
				gauge = {
					'axis': {'range': [min_pages, max_pages]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_pages}
				}
			),
			go.Indicator(
				domain = {'x': [0.33, 0.66], 'y': [0.5, 1]},
				value = avg_price,
				mode = "gauge+number",
				number = {'prefix': "$"},
				title = {'text': "(Min, Max, Avg) Prices"},
				gauge = {
					'axis': {'range': [min_price, max_price]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_price}
				}
			),
			go.Indicator(
				domain = {'x': [0.66, 1], 'y': [0.5, 1]},
				value = avg_reviews,
				mode = "gauge+number",
				title = {'text': "(Min, Max, Avg) Reviews"},
				gauge = {
					'axis': {'range': [min_reviews, max_reviews]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_reviews}
				}
			),
			go.Indicator(
				domain = {'x': [0.5, 1], 'y': [0, 0.3]},
				value = avg_rating,
				mode = "number",
				title = {'text': "Avg Rating"},
				gauge = {
					'axis': {'range': [0, 5]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 5}
				}
			),
			go.Indicator(
				domain = {'x': [0, 0.5], 'y': [0, 0.3]},
				value = most_common_genre,
				mode = "number",
				title = {'text': "Top Genre"},
				gauge = {
					'axis': {'range': [0, 5]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 5}
				}
			)
		],
		'layout' : {
			"margin" : {"l": 0, "r" : 0, "t" : 50, "b" : 50}
		}
	}
	return figure


def get_stats_table(data_df: pd.DataFrame = NODE_DF):
	"""
	Returns filterable table
	"""
	stats_table = dash_table.DataTable(
		id = "stats_table",
		columns = [
			{"name": i, "id": i, "deletable": False, "selectable": True} for i in data_df
		],
		data = data_df.to_dict('records'),
		filter_action="custom",
		filter_query="",
		sort_action="native",
		sort_mode="multi",
		style_as_list_view = True,
		merge_duplicate_headers = True,
		page_size = 20,
		style_header = {
			'backgroundColor': 'white',
			'fontWeight': 'bold',
			'textAlign' : 'center'
		},
		style_table = {
			'overflowX': 'auto'
		},
		style_cell = {
			"padding" : "5px",
			"font-family" : "Source Sans Pro",
			"fontSize" : 16,
		},
		style_data={
			'height': 'auto'
		},
		style_data_conditional = [
			{
				'if': {'row_index': 'odd'},
				'backgroundColor': 'rgb(248, 248, 248)'
			}
		] + [{'if': {'column_id': c},'textAlign': 'center'} for c in data_df.columns]
		,
		css = [
			{"selector": ".cell-1-1", "rule": "width: 100%;"},
			{"selector": 'td.cell--selected, td.focused', "rule": 'background-color: #6cc091 !important; color: #ffffff !important'}
		]
	)
	return stats_table

def filter_stats_table(filter):
	filtering_expressions = filter.split(' && ')
	dff = NODE_DF
	for filter_part in filtering_expressions:
		col_name, operator, filter_value = helpers.split_filter_part(filter_part)

		if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
			# these operators match pandas series operator method names
			dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
		elif operator == 'contains':
			dff = dff.loc[dff[col_name].str.contains(filter_value)]
		elif operator == 'datestartswith':
			dff = dff.loc[dff[col_name].str.startswith(filter_value)]
	return dff

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

def _compute_correlations_traces(corr_direction: str):
	"""
	Returns information about positive / negative correlated features
	Checks all the edges and removes some based on corr_direction.
	-------------------
	direction = positive: Only returns the positive correlations and delete the edges with weight smaller than 0
	direction = negative: Only returns the negative correlations and delete the edges with weight equal or larger than 0
	"""
	node_df = read_node_df(NODES_FILE)
	cor_matrix = node_df.iloc[:, 1:].corr()
	node_idx = cor_matrix.index.values

	cor_matrix = np.asmatrix(cor_matrix)
	cor_G = nx.from_numpy_matrix(cor_matrix)
	cor_G = nx.relabel_nodes(cor_G, lambda x: node_idx[x])
	
	cor_G_copy = cor_G.copy()
	for feature_1, feature_2, weight in cor_G.edges(data=True):
		if corr_direction == "Positive":
			if weight["weight"] < 0:
				cor_G_copy.remove_edge(feature_1, feature_2)
		else:
			if weight["weight"] >= 0:
				cor_G_copy.remove_edge(feature_1, feature_2)

	# Generate circular layout positions
	pos = nx.circular_layout(cor_G_copy)

	temp_node_x = []
	temp_node_y = []
	temp_edge_x = []
	temp_edge_y = []
	for edge in cor_G_copy.edges():
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
		mode='lines'
	)
	
	for node in cor_G_copy.nodes():
		x, y = pos[node]
		temp_node_x.append(x)
		temp_node_y.append(y)

	node_trace = go.Scatter(
		x=temp_node_x, y=temp_node_y,
		mode='markers',
		hoverinfo='text',
		marker=dict(
			color='#00c292',
			size=15,
			line_width=2
		)
	)

	node_adjacencies = []
	node_text = []
	for node, adjacencies in enumerate(cor_G_copy.adjacency()):
		node_adjacencies.append(len(adjacencies[1]))
		node_text.append(
			# Append all node information here
			f"<b>{adjacencies[0]}"
		)

	edge_adjacencies = []
	edge_text = []
	for edge_pair in cor_G_copy.edges():
		wanted_weights = _get_weights(cor_G_copy, edge_pair[0])
		if edge_pair[0] != edge_pair[1]: 
			cur_weight = wanted_weights[edge_pair[1]]['weight']

			edge_adjacencies.append(cur_weight)
			edge_text.append(
				# Append all node information here
				f"<b>Edge: {edge_pair}</b><br /><b>Properties:</b><br />\
					Weight: {cur_weight}\
				"
			)
	
	Xe=[]
	Ye=[]
	xt = []
	yt = []
	for e in cor_G_copy.edges():
		if e[0] != e[1]:
			mid_edge = 0.5*(pos[e[0]]+pos[e[1]])# mid point of the edge e
			xt.append(mid_edge[0])
			yt.append(mid_edge[1])
			Xe.extend([pos[e[0]][0], pos[e[1]][0], None])
			Ye.extend([pos[e[0]][1], pos[e[1]][1], None])
	
	trace_text = go.Scatter(
		x=xt, y=yt, 
		mode='text',
		text=edge_text,
		textposition='bottom center',
		hoverinfo='text'
	)
	node_trace.text = node_text

	return node_trace, edge_trace, trace_text

def _get_weights(G: nx.Graph, matching_col: str):
	adj_weights = list(G.adjacency())
	wanted_weights = None
	for col in adj_weights:
		if col[0] == matching_col:
			wanted_weights = col[1]
	return wanted_weights

def generate_correlation_network(corr_direction: str):
	"""
	Returns Plotly Graph object for correlation network.
	"""
	node_traces, edge_traces, trace_text = _compute_correlations_traces(corr_direction)

	fig = go.Figure(
		data=[node_traces, edge_traces, trace_text],
		layout=go.Layout(
			title={
				"text":f"<b>Correlation Network ({corr_direction})</b>"},
			titlefont_size=16,
			showlegend=False,
			hovermode='closest',
			margin=dict(b=20,l=5,r=5,t=40),
		)
	)
	fig.update_layout(
		title = helpers.style_title(),
		font = helpers.style_font()
	)

	return fig

def _compute_centrality_measures(G: nx.Graph):
	degree_centrality = list(nx.degree_centrality(G).values())
	betweenness_centrality = list(nx.betweenness_centrality(G).values())
	closeness_centrality = list(nx.closeness_centrality(G).values())

	for idx, node_id in enumerate(G.nodes()):
		G.nodes[node_id]['degree_centrality'] = degree_centrality[idx]
		G.nodes[node_id]['betweenness_centrality'] = betweenness_centrality[idx]
		G.nodes[node_id]['closeness_centrality'] = closeness_centrality[idx]

	return G

def _compute_clustering_coefficients(G: nx.Graph):
	clustering_coefficients = nx.clustering(G)
	
	for idx in G.nodes():
		G.nodes[idx]['clustering_coefficient'] = clustering_coefficients[idx]
	
	return G

def _compute_adjacencies(G: nx.Graph):    
	for idx in G.nodes():
		G.nodes[idx]['num_connections'] = len(G[idx])
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

def generate_graph(dataset:str='amazon', filters = None, nodelist = None):
	G = nx.Graph()
	
	if dataset == 'amazon':
		node_df = NODE_DF
		edge_df = EDGE_DF
		
		if filters:
			filter_mapping = {
				'genre_filter' : 'genre',
				'sales_rank_filter' : 'sales_rank',
				'rating_filter' : 'avg_rating',
				'reviews_filter' : 'num_reviews',
				'page_filter' : 'num_pages',
				'price_filter' : 'price',
				'nclique_filter' : 'nclique'
			}

			filtered_df = node_df.copy()

			for filter_name, value in filters.items():
				column = filter_mapping[filter_name]
				if type(value) != list:
					value = [value]

				if column in ['genre', 'avg_rating']:
					filtered_df = filtered_df[filtered_df[column].isin(value)]

				elif column in ['sales_rank', 'num_reviews']:
					temp_df = pd.DataFrame()
					for value_range in value:
						low, high = value_range.split(" - ")
						df_slice = filtered_df[filtered_df[column].between(int(low), int(high))]
						temp_df = temp_df.append(df_slice)
					filtered_df = temp_df

				elif column in ['num_pages', 'price']:
					low, high = value
					low_quantile = filtered_df[column].quantile(low * 0.1)
					high_quantile = filtered_df[column].quantile(high * 0.1)
					filtered_df = filtered_df[filtered_df[column].between(low_quantile, high_quantile)]
			
			if nodelist:
				filtered_df = filtered_df[filtered_df['id'].isin(nodelist)]
			
			keep_nodes = filtered_df['id']

			node_df = filtered_df

			edge_df = edge_df[edge_df['source'].isin(keep_nodes) & edge_df['target'].isin(keep_nodes)]

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

		G = _compute_adjacencies(G)
	
	return G

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

# Initialize NetworkX graph
networkGraph = generate_graph()

def plot_graph(G = networkGraph, params = None):
	chart_type_option = 'spring'

	if params:
		chart_type_option = params.pop('chart_type_option')
		valid_params = {key : value for key, value in params.items() if value}
		G = generate_graph(filters = valid_params)

	layouts = {
		'circular' : lambda g : nx.circular_layout(g),
		'kamada-kawai' : lambda g : nx.kamada_kawai_layout(g),
		'random' : lambda g : nx.random_layout(g),
		'shell' : lambda g : nx.shell_layout(g),
		'spring' : lambda g : nx.spring_layout(g),
		'spectral' : lambda g : nx.spectral_layout(g)
	}

	pos = layouts[chart_type_option](G)

	edge_x = []
	edge_y = []

	edge_traces = []

	for edge in G.edges(data = True):
		start, end, data = edge
		x0, y0 = pos[start]
		x1, y1 = pos[end]

		edge_trace = go.Scatter(
			x=[x0, x1, None], y=[y0, y1, None],
			line=dict(width=np.log(data['weight']), color='#888'),
			hoverinfo='none',
			mode='lines'
		)
		edge_traces.append(edge_trace)
	

	node_x = []
	node_y = []
	for node in G.nodes():
		x, y = pos[node]
		node_x.append(x)
		node_y.append(y)

	node_trace = go.Scatter(
		x=node_x, y=node_y,
		mode='markers',
		hoverinfo='text',
		marker=dict(
			showscale=False,
			# colorscale options
			#'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
			#'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
			#'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
			colorscale='YlGnBu',
			reversescale=True,
			color=[],
			size=10,
			line_width=2))

	node_text = []

	for node in G.nodes():
		node_info = G.nodes()[node]
		node_text.append("<br>".join([f"<b>{key}:</b> {value}" for key, value in node_info.items()]))

	node_adjacencies = [G.nodes()[node]['num_connections'] for node in G]
	node_trace.marker.color = node_adjacencies
	node_trace.text = node_text

	fig = go.Figure(data=edge_traces + [node_trace],
			 layout=go.Layout(
				showlegend=False,
				hovermode='closest',
				xaxis = {
					'visible' : False
				},
				yaxis = {
					'visible' : False
				},
				paper_bgcolor='rgba(0,0,0,0)',
				plot_bgcolor='rgba(0,0,0,0)',
				margin=dict(b=20,l=5,r=5,t=40)
			)
		)
	return fig

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

def generate_cyto_ego_networks(G:nx.Graph, n_ranks:int) -> List[nx.Graph]:
	ego_networks = []
	for i in range(n_ranks):
		ego_node, hub_ego, _ = get_ego_network(G, i+1)

		for node in hub_ego.nodes():
			if node == ego_node:
				hub_ego.nodes[node]['is_ego'] = True
			else:
				hub_ego.nodes[node]['is_ego'] = False
		
		ego_networks.append(hub_ego)

	return ego_networks

def get_ego_node_edge_traces(G:nx.Graph, n_ranks:int):
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

def generate_ego_network(n_ranks:int, G:nx.Graph = networkGraph):
	node_traces, edge_traces = get_ego_node_edge_traces(G, n_ranks)

	plotly_figures = []

	for idx in range(len(node_traces)):
		fig = go.Figure(
			data=[node_traces[idx], edge_traces[idx]],
			layout=go.Layout(
				title={
					"text":f"<b>Rank {idx+1} Ego Network</b>"},
				titlefont_size=16,
				showlegend=False,
				hovermode='closest',
				margin=dict(b=20,l=5,r=5,t=40),
				
			)
		)
		fig.update_layout(
			title = helpers.style_title(),
			font = helpers.style_font()
		)
		plotly_figures.append(fig)

	return plotly_figures

def plot_cyto_graph(G = networkGraph, params = None):
	if params:
		valid_params = {key : value for key, value in params.items() if value}
		G = generate_graph(filters = valid_params)

	elements = [{'data': {'id': str(int(node_id)), 'label': str(int(node_id))}} for node_id in G.nodes()]
	edges = [{'data' : {'source' : str(int(source)), 'target' : str(int(target)), 'weight' : np.log(weight)}} for source, target, weight in G.edges.data("weight")]
	
	return elements + edges

def plot_cyto_ego_graphs(G = networkGraph, params = None):
	if params:
		valid_params = {key : value for key, value in params.items() if value}
		G = generate_graph(filters = valid_params)

	ego_graph_list = generate_cyto_ego_networks(G, 3)
	# To update to show 3

	graph_elements = []
	for eg_graph in ego_graph_list:

		elements = [{'data': {'id': str(int(node_id)), 'label': str(int(node_id)), 'is_ego': eg_graph.nodes[node_id]['is_ego']}} for node_id in eg_graph.nodes()]
		edges = [{'data' : {'source' : str(int(source)), 'target' : str(int(target)), 'weight' : np.log(weight)}} for source, target, weight in eg_graph.edges.data("weight")]

		graph_elements.append(elements + edges)

	return graph_elements

def plot_cyto_nclique_graph(G = networkGraph, params = None):
	nclique_value = 3
	valid_params = {}
	if params:
		if 'nclique_filter' in params:
			nclique_value = helpers.clique_sizes()[int(params.pop('nclique_filter'))]
		valid_params = {key : value for key, value in params.items() if value}
		G = generate_graph(filters = valid_params)

	# Dictionary with information of each maximal clique based on value of n in n-clique
	clique_graph_table_info = generate_clique_metrics(G)

	clique_nodes_list = [item['nodes'] for item in get_cliques_by_size(G)[nclique_value]]
	flatten_node_list = list(set([node for clique in clique_nodes_list for node in clique]))
	G = generate_graph(filters = valid_params, nodelist = flatten_node_list)

	elements = [{'data': {'id': str(int(node_id)), 'label': str(int(node_id))}} for node_id in G.nodes()]
	edges = [{'data' : {'source' : str(int(source)), 'target' : str(int(target)), 'weight' : np.log(weight)}} for source, target, weight in G.edges.data("weight")]

	return elements + edges

def include_loader(graph_component):
	return dcc.Loading(type = "cube", color = "#36454f", children = [graph_component])