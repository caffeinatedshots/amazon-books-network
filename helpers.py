import numpy as np

# Filtering functions
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value

    return [None] * 3


# Styling functions
def style_title():
    title_style = {
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
    return title_style

def style_font():
    font_style = {
        'family': "Raleway"
    }
    return font_style

def network_layout_options():
    layout_types = ["random", "grid", "circle", "concentric", "breadthfirst", "cose", "cose-bilkent", "cola", "euler", "spread", "dagre", "klay"]
    return layout_types

def clique_sizes():
    return [2, 3, 4, 5]

def data_attributes():
    return ['genre', 'avg_rating']

def colour_scheme():
    return ["#5FAD56", "#F2C14E", "#F78154", "#B4436C", "#2F4073", "#AA3939", "#764B8E"]

def generate_options(option_arr):
    return [{'label' : str(option).title(), 'value' : option} for option in option_arr]

def generate_range_values(value_arr):
    return {i : str(value_arr[i]) for i in range(len(value_arr))}

def _generate_node_edge_info(node_data, edge_data):
    para = """"""
    if node_data:
        para += f"""
            You recently hovered over the node: {node_data['label']}.
            Genre: {node_data['genre']}
            Sales Rank: {node_data['sales_rank']}
            Average Rating: {node_data['avg_rating']}
            No. of Reviews: {node_data['num_reviews']}
            No. of Pages: {node_data['num_pages']}
            Price: {node_data['price']}
            Degree Centrality: {node_data['degree_centrality']}
            Betweeness Centrality: {node_data['betweenness_centrality']}
            Closeness Centrality: {node_data['closeness_centrality']}
            """
    if edge_data:
        para += f"""
            You recently hovered over the edge:
            Source: {edge_data['source']}
            Target: {edge_data['target']}
            Frequency: {int(np.exp(edge_data['weight']))}
            """
    return para